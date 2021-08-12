import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go
from flask_caching import Cache
from ..model import Model
from ..version import VERSION

def horiz_space(pixels):
    return html.Span("", style={'width': pixels, 'display': 'inline-block'})

def pulldown_style(width=200):
    style = {'width': width,
             'textAlign': 'center',
             'vertical-align': 'middle',
             'display': 'inline-block'
             }
    return style

#
# def get_pp_scatter(county=None):
#     gdf = pp_gdf.query("County == @county") if county else pp_gdf
#
#     trace = go.Scattergeo(name='Power Plants',
#                           lat=gdf.geometry.y,
#                           lon=gdf.geometry.x,
#                           mode='markers',
#                           opacity=0.6,
#                           hovertext=gdf.hover_text,
#                           hoverinfo='text',     # eliminates (lat,lon) from hover text
#                           marker={'color': 'red',
#                                   'size': gdf['Capacity_Latest'],
#                                   'sizemin': 1,
#                                   'sizemode': 'area',   # vs 'diameter'
#                                   # 'sizeref': 10,      # scale factor
#                                   }
#                         )
#     return trace

def app_layout(app, model):
    layout = html.Div([
        dcc.Store(id='some-data', storage_type='session'),

        html.Div([
            html.H1(app.title),
            ],
            style={'textAlign': 'center'}
        ),

        html.Div([
            dcc.Tabs(
                id="tabs",
                value='inputs',
                parent_className='custom-tabs',
                className='custom-tabs-container',
                children=[
                    dcc.Tab(
                        children=[],    # see inputs_layout()
                        label='Inputs',
                        value='inputs',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                    ),
                    dcc.Tab(
                        children=[],  # see settings_layout()
                        label='Settings',
                        value='settings',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                    ),
                    dcc.Tab(
                        children=[],  # see results_layout()
                        label='Results',
                        value='results',
                        className='custom-tab',
                        selected_className='custom-tab--selected'
                    ),
                ]
            ),
            html.Div(inputs_layout(model), id='tab-content')
        ])
    ])
    return layout

def cap_selector_options(model, select_all=False):
    options = [html.Option(name, value=name, selected=select_all) for name in model.cap_names]
    return options

def tac_selector_options(model, select_all=False):
    options = [html.Option(name, value=name, selected=select_all) for name in model.tac_names]
    return options

def sector_selector_options(model, select_all=False):
    options = [html.Option(name, value=name, selected=select_all) for name in model.emission_sectors]
    return options


def inputs_layout(model, year_range=None):
    first = (year_range and year_range[0]) or model.first_year
    last  = (year_range and year_range[1]) or model.last_year
    first_decade = first + 5 - first % 5  # first mark after 2017 => 2020

    marks = {y: str(y) for y in range(first_decade, last, 5)}
    marks[first] = str(first)
    marks[last]  = str(last)

    layout = html.Div([
        html.Div([
            html.H3(f"Years of Analysis ({first}-{last})", id="years-of-analysis"),
            dcc.RangeSlider(
                id='analysis-years-slider',
                min=first,
                max=last,
                step=1,
                value=[first, last],
                marks=marks
            ),

        ]),

        html.Div([
            html.H3("Criteria Pollutants"),

            dcc.Checklist(
                id='cap-selection-checklist',
                options=[
                    {'label': 'Select all', 'value': 'select'},
                ],
                value=[]
            ),

            html.Select(cap_selector_options(model),
                        id='cap-selector', multiple=True, size=len(model.cap_names))
            ],
            style={
                'display': 'inline-block',
                'vertical-align': 'top',
            },
            className="four columns",
        ),

        horiz_space(30),

        html.Div([
            html.H3("Toxic Air Contaminants"),

            dcc.Checklist(
                id='tac-selection-checklist',
                options=[
                    {'label': 'Select all', 'value': 'select'},
                ],
                value=[]
            ),

            html.Select(tac_selector_options(model),
                        id='tac-selector', multiple=True, size=30)
            ],
            style={
                'display': 'inline-block',
                'vertical-align': 'top',
            },
            className="four columns",
        ),

        horiz_space(30),

        html.Div([
            html.H3("Emission Sectors"),

            dcc.Checklist(
                id='sector-selection-checklist',
                options=[
                    {'label': 'Select all', 'value': 'select'},
                ],
                value=[],
                persistence=True,
            ),

            html.Select(sector_selector_options(model),
                        id='sector-selector',
                        multiple=True,
                        size=30,
                        )
        ],
            style={
                'display': 'inline-block',
                'vertical-align': 'top',
            },
            className="four columns",
        ),

        horiz_space(30),

        html.Div([
            html.H3("Health impacts"),
            dcc.RadioItems(id='impacts-radio',
                           options=[{'label': 'DALYs', 'value': 'dalys'},
                                    {'label': 'Health endpoints', 'value': 'health-endpoints'}],
                           value='dalys',
                           persistence=True,
                           ),

                           html.Br(),

            html.H3("Discount rate"),
            dcc.RadioItems(id='discount-rate-radio',
                           options=[{'label': 'Internal function', 'value': 'internal'},
                                    {'label': 'User provided', 'value': 'user-supplied'}],
                           value='internal',
                           persistence=True,
                           ),
            html.Div(dcc.Input(id='discount-rate-input', type='number', debounce=True,
                               value=model.default_discount_rate,
                               step=0.01,
                               persistence=True,
                               )
                     ),
            html.Br(),

            html.H3("Presentation of results"),
            html.Div(dcc.Checklist(
                id='results-presentation-checklist',
                options=[{'label': value, 'value': value.lower()} for value in ('Map', 'Graph', 'Tables')],
                persistence=True,
            )),
        ],
        style={
            'display': 'inline-block',
            'vertical-align': 'top',
        },
        className='three columns')
    ],
    className="twelve columns")
    return layout

def settings_layout():
    return html.H2('SETTINGS')

def results_layout():
    return html.H2('RESULTS')


def main(args):
    model = Model()

    app = dash.Dash(__name__, suppress_callback_exceptions = True)
    app.config.suppress_callback_exceptions = True
    app.title = "BEST-AIR v" + VERSION
    app.layout = app_layout(app, model)

    # How many seconds to allow the item to be cached. Default is 300 (5 min); we set it to an hour.
    # CACHE_TIMEOUT = 60 * 60
    CACHE_TIMEOUT = 10

    cache = Cache(app.server,
                  config={
                      'CACHE_TYPE': 'FileSystemCache',
                      'CACHE_DIR': '/Volumes/Plevin1TB/BEST-AIR/app-cache'
                  })

    @app.callback(
        Output('cap-selector', 'children'),
        Input('cap-selection-checklist', 'value'),
    )
    def select_all_caps(value):
        select_all = 'select' in value
        return cap_selector_options(model, select_all=select_all)

    @app.callback(
        Output('tac-selector', 'children'),
        Input('tac-selection-checklist', 'value'),
    )
    def select_all_tacs(value):
        select_all = 'select' in value
        return tac_selector_options(model, select_all=select_all)

    @app.callback(
        Output('sector-selector', 'children'),
        Input('sector-selection-checklist', 'value'),
    )
    def select_all_sectors(value):
        select_all = 'select' in value
        return sector_selector_options(model, select_all=select_all)

    @app.callback(
        Output('discount-rate-input', 'disabled'),
        Input('discount-rate-radio', 'value'),
    )
    def disable_discount_rate_entry(value):
        disabled = (value and value == 'internal')
        return disabled

    @app.callback(
        Output('years-of-analysis', 'children'),
        Input('analysis-years-slider', 'value'),
    )
    def show_analysis_years(year_range):
        if year_range:
            first, last = year_range
        else:
            first = model.first_year
            last = model.last_year

        return f"Years of Analysis ({first}-{last})"

    @app.callback(
        Output('tab-content', 'children'),
        Input('tabs', 'value'),
        State('analysis-years-slider', 'value')
    )
    def render_content(tab, year_range):
        if tab == 'inputs':
            return inputs_layout(model, year_range)

        elif tab == 'settings':
            return settings_layout()

        elif tab == 'results':
            return results_layout()

    app.run_server(debug=True)
