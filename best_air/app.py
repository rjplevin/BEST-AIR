import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import numpy as np
#import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from flask_caching import Cache

class GeoData:

    def __init__(self, shapefile_path, index_col=None):
        self.gdf = gpd.read_file(shapefile_path)
        self.index_col = index_col
        if index_col is not None:
            self.gdf.set_index(index_col, inplace=True)

data_dir = '/Volumes/Plevin1TB/BEST-AIR/data/'

data_dict = {
    # 9129 rows, 13 cols: 'STATEFP', 'COUNTYFP', 'TRACTCE', 'GEOID', 'NAME', 'NAMELSAD', 'MTFCC', 'FUNCSTAT', 'ALAND', 'AWATER', 'INTPTLAT', 'INTPTLON', 'geometry'
    'Census Tract' : GeoData(data_dir + 'CA-census-tracts/tl_2020_06_tract/tl_2020_06_tract.shp', 'GEOID'),
    'County'       : GeoData(data_dir + 'California_Counties/geo_export_9a3f5450-65c6-4f9a-93fc-bc6807b18507.shp', 'name'),
    'Power Plant'  : GeoData(data_dir + 'power-plants/California_Power_Plants/Power_Plants.shp')
}

# trim down the power plant data to the useful set (still 1766 rows...)
pp = data_dict['Power Plant']
pp_gdf = pp.gdf[['Plant_ID', 'PlantName', 'State', 'County', 'Capacity_L', 'geometry']].copy()
pp_gdf['Capacity_L'].fillna(0, inplace=True)
pp_gdf = pp_gdf.query("Capacity_L > 0 and State == 'CA'") # TBD: decide whether to show neighboring states

app = dash.Dash(__name__)

# choices = ('Counties', 'Census Tracts')
county_choices = ('latitude', 'longitude')
tract_choices = ('ALAND', 'AWATER')

resolution_choices = ('County', 'Census Tract')

# How many seconds to allow the item to be cached. Default is 300 (5 min); we set it to an hour.
CACHE_TIMEOUT = 60 * 60

cache = Cache(app.server,
              config={
                  'CACHE_TYPE': 'FileSystemCache',
                  'CACHE_DIR': '/Volumes/Plevin1TB/BEST-AIR/app-cache'
              })

app.layout = html.Div([
    html.H3("Example Choropleths"),
    dcc.RadioItems(
        id='resolution_choices',
        options=[{'value': x, 'label': x} for x in resolution_choices],
        value=resolution_choices[0],
        labelStyle={'display': 'inline-block'}
    ),
    dcc.RadioItems(
        id='column_choices',
        labelStyle={'display': 'inline-block'}
    ),
    # html.Span("Show power plants:"),
    dcc.RadioItems(
        id='show_power_plants',
        options=[{'value': x, 'label': x} for x in ('Yes', 'No')],
        value='No',
        labelStyle={'display': 'inline-block'}),
    dcc.Graph(id="map", style={'height': '900px'}), # width is adjusted since ratio is fixed
])

@app.callback(Output("column_choices", "options"),
              Output("column_choices", "value"),
              Input("resolution_choices", "value"))
def set_radio_buttons(resolution):
    chosen_choices = tract_choices if resolution == 'Census Tract' else county_choices
    options = [{'value': x, 'label': x} for x in chosen_choices]
    return options, chosen_choices[0]

@app.callback(
    Output("map", "figure"),
    Input("column_choices", "value"),
    Input("resolution_choices", "value"),

    # For some reason, adding this results in a tiny map being drawn
    # Input("show_power_plants", "value")
)
@cache.memoize(timeout=CACHE_TIMEOUT)
def show_map(colname, resolution): #, power_plants):
    gdf = data_dict[resolution].gdf

    fig = px.choropleth(
        gdf,
        geojson=gdf.geometry,
        locations=gdf.index,
        color=colname,
        projection="mercator"
    )

    #if power_plants:
    fig.add_trace(go.Scattergeo(pp_gdf,
                                lat=pp_gdf.geometry.y,
                                lon=pp_gdf.geometry.x,
                                # hover_name="PlantName"
                                ))

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

app.run_server(debug=True)
