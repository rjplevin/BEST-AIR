import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from flask_caching import Cache
from best_air.model import Model
from best_air.version import VERSION

class GeoData:

    def __init__(self, pathname, index_col=None):
        """
        Create a GeoData instance.

        :param pathname: (str) pathname of a .shp or .geojson file.
        :param index_col: (str or None) column name to set as index
        """
        self.pathname = pathname
        self.gdf = gpd.read_file(pathname)
        self.index_col = index_col

        if index_col is not None:
            self.gdf.set_index(index_col, inplace=True)

projection = 'mercator'

data_dir = '/Volumes/Plevin1TB/BEST-AIR/data/'

data_dict = {
    # 9129 rows, 13 cols: 'STATEFP', 'COUNTYFP', 'TRACTCE', 'GEOID', 'NAME', 'NAMELSAD', 'MTFCC', 'FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry'
    'Census Tract': GeoData(data_dir + 'CA-census-tracts/tl_2020_06_tract/tl_2020_06_tract.shp', 'GEOID'),

    'County': GeoData(data_dir + 'California_Counties/geo_export_9a3f5450-65c6-4f9a-93fc-bc6807b18507.shp', 'name'),

    # The geojson version is in lat/lon; the shapefile uses some other coordinate system
    'Power Plant': GeoData(data_dir + 'power-plants/California_Power_Plants.geojson')
}

# trim down the power plant data to the useful set (still 1766 rows...)
pp = data_dict['Power Plant']
pp_gdf = pp.gdf[['Plant_ID', 'PlantName', 'State', 'County', 'Capacity_Latest', 'PriEnergySource', 'geometry']].copy()
pp_gdf['Capacity_Latest'].fillna(0, inplace=True)

# Non-combustion energy sources
non_combustion = (
    'BAT',  # battery
    'GEO',  # geothermal
    'NUC',  # nuclear
    'SUN',  # solar
    'WAT',  # hydro
    'WND',  # wind
)

# TBD: decide whether to show neighboring states
pp_gdf = pp_gdf.query("Capacity_Latest > 0 and State == 'CA' and PriEnergySource not in @non_combustion")

fips_df = pd.read_csv(data_dir + 'CA-county-fips.csv', skiprows=1, index_col='name', dtype={'fips': str})
countyfp = fips_df.fips.str[-3:] # the last 3 digits are the county code (string)

# Generate contents of pulldown menu of county names, and a dict to translate to COUNTYFP
county_items = [{'value': name, 'label': name} for name in fips_df.index]
countyfp_dict = {name: code for name, code in countyfp.items()}

pp_gdf['hover_text'] = pp_gdf.PlantName + '<br>Capacity: ' + pp_gdf.Capacity_Latest.astype(str) + ' MW'

# population by census tract (2010). There are 8057 rows for CA, vs the Census Tract gdf, which has 9129 rows. Can there be > 1000 additional tracts?
pop_csv = data_dir + 'pop-by-tract/censustract-CA-2010.csv'
pop_df = pd.read_csv(pop_csv, index_col=None, dtype={'GEOID': str, 'ST10': str})

# We do all this because setting the index_col in read_csv converts strings to int
pop_df = pop_df.set_index(pop_df.GEOID).drop('GEOID', axis='columns')

# Add population to census gdf. Note that this results in some NaNs.
census_tract_gdf = data_dict['Census Tract'].gdf
census_tract_gdf['POP2010'] = pop_df['POP2010']
# TBD: ? census_tract_gdf['POP2010'].fillna(0, inplace=True)

# income and population data by county
county_stats_df = pd.read_csv(data_dir + 'income-tax-stats-by-county/B-6__Comparison_By_County.csv', index_col=None,
                              usecols=('County', 'Population', 'Taxable Year', 'AGI', 'Median Income'))
county_stats_df.rename({'Taxable Year': 'Year', 'Median Income': 'Median_Income'}, axis='columns', inplace=True)
county_stats_df = county_stats_df.query('Year == 2018 and County not in ("Nonresident", "Resident Out-of-State", "Unallocated")').set_index('County')
county_stats_df.drop('Year', axis='columns', inplace=True)

# To create a radio button array indicating which statistic to display
county_stats_items = [{'value': name, 'label': name} for name in county_stats_df.columns]
county_gdf = data_dict['County'].gdf

for name in county_stats_df.columns:
    county_gdf[name] = county_stats_df[name]


def get_pp_scatter(county=None):
    gdf = pp_gdf.query("County == @county") if county else pp_gdf

    trace = go.Scattergeo(name='Power Plants',
                          lat=gdf.geometry.y,
                          lon=gdf.geometry.x,
                          mode='markers',
                          opacity=0.6,
                          hovertext=gdf.hover_text,
                          hoverinfo='text',     # eliminates (lat,lon) from hover text
                          marker={'color': 'red',
                                  'size': gdf['Capacity_Latest'],
                                  'sizemin': 1,
                                  'sizemode': 'area',   # vs 'diameter'
                                  # 'sizeref': 10,      # scale factor
                                  }
                        )
    return trace

def main(args):
    # TBD: use __name__ once this is not the main program
    app = dash.Dash('app')
    # app.config['suppress_callback_exceptions'] = True
    app.title = "BEST-AIR v" + VERSION

    model = Model()

    # How many seconds to allow the item to be cached. Default is 300 (5 min); we set it to an hour.
    # CACHE_TIMEOUT = 60 * 60
    CACHE_TIMEOUT = 10

    cache = Cache(app.server,
                  config={
                      'CACHE_TYPE': 'FileSystemCache',
                      'CACHE_DIR': '/Volumes/Plevin1TB/BEST-AIR/app-cache'
                  })

    # noinspection PyCallingNonCallable
    app.layout = html.Div([
        html.H3("Example Choropleths"),
        dcc.Dropdown(
            id='county',
            placeholder='Select county...',
            options=county_items,
            style={'width': '200px'}
            #value=
        ),
        html.Div([
            html.Span("Color counties by:"),
            dcc.RadioItems(
                id='county_stats_radio',
                options=county_stats_items,
                value='Population',
                labelStyle={'display': 'inline'}),
            ]),
        html.Div([
            html.Span("Show power plants:"),
            dcc.RadioItems(
                id='show_power_plants',
                options=[{'value': x, 'label': x} for x in ('Yes', 'No')],
                value='No',
                labelStyle={'display': 'inline'}),
            ]),
        dcc.Graph(id="map", style={'height': '900px'}), # width is adjusted since ratio is fixed
    ]) #, style={})


    @app.callback(
        [Output("map", "figure"),
         Output("county", "value")],
        [Input("county", "value"),
         Input("show_power_plants", "value"),
         Input("county_stats_radio", "value"),
         Input("map", "clickData"),
         ],
    )
    @cache.memoize(timeout=CACHE_TIMEOUT)
    def show_map(county, power_plants, county_stat, click_data):
        ctx = dash.callback_context

        # clear clickData if not triggered in this call
        triggered = ctx.triggered[0]
        if triggered['prop_id'] != 'map.clickData':
            click_data = None

        if county is None and click_data is not None:
            location = click_data['points'][0]['location']
            # county map locations are numeric (strings) of GEOID
            county = None if (location and location.isdigit()) else location

        if county:
            countyfp = countyfp_dict[county]
            # show detail for the selected county
            gdf = census_tract_gdf.query('COUNTYFP == @countyfp')
            title = county + ' County'
            color = 'POP2010'
        else:
            # show all counties
            gdf = data_dict['County'].gdf
            title = 'California'
            color = county_stat

        fig = px.choropleth(
            gdf,
            geojson=gdf.geometry,
            locations=gdf.index,
            color=color,
            projection=projection,
            title=title,
            # clickmode='event+select',
        )

        if power_plants == 'Yes':
            # if county_name is None, adds all plants in the state
            trace = get_pp_scatter(county)
            fig.add_trace(trace)

        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 20, "l": 0, "b": 0},
                          title={'text': title,
                                 'xanchor': 'center',
                                 'yanchor': 'top',
                                 'x': 0.5})

        return fig, county

    app.run_server(debug=True)
