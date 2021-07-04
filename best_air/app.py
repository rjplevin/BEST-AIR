import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np
#import pandas as pd
import geopandas as gpd
import plotly.express as px

counties_shapefile = '//Volumes/Plevin1TB/BEST-AIR/data/California_Counties/geo_export_9a3f5450-65c6-4f9a-93fc-bc6807b18507.shp'

geo_df = gpd.read_file(counties_shapefile).set_index('name')

num_counties = len(geo_df)
geo_df['random1'] = np.random.standard_normal(num_counties)
geo_df['random2'] = np.random.standard_exponential(num_counties)

app = dash.Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id="dropdown",
        options=[{"label": x, "value": x}
                 for x in ('latitude', 'longitude', 'random1', 'random2')],
        value='latitude',
        multi=False
    ),
    dcc.Graph(id="geoplot"),
])

@app.callback(
    Output("geoplot", "figure"),
    [Input("dropdown", "value")])
def update_bar_chart(colname):
    fig = px.choropleth(geo_df,
                        geojson=geo_df.geometry,
                        locations=geo_df.index,
                        color=colname,
                        # labels={'random': 'Random number'},
                        # hover_name="index",
                        projection="albers usa",
                        # projection="mercator",
                        )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
    return fig

app.run_server(debug=True)
