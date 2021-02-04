import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from Pages.model import get_recommendations, graph_against
from app import app
import matplotlib as plt
from plotly.tools import mpl_to_plotly
import pandas as pd

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dcc.Markdown('## Enter the Song of your choice!'),
                            dcc.Markdown('### Song Name'),
                            dcc.Input(
                                id='song_name',
                                type='text',
                            ),
                            html.Button(id='submit_button_state', children='Match!'),
                            dcc.Markdown('## Matched Songs'),
                            html.Div(id='match-content', className='lead')
                        ]
                    )
                 )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            dcc.Markdown('### Compare your song to a song in the list'),
                            dcc.Markdown('Enter Song Number from List'),
                            dcc.Input(
                                id='song_number',
                                placeholder='Song Number',
                                type='text'
                            ),
                            html.Button(id='submit_button_graph', children='Graph!')
                        ]
                    )
                ),
                dbc.Col(
                    html.Div(id='graph-content', children='component')
                )
            ]
        )    
    ]
)


# adding callback
@app.callback(
    Output('match-content', component_property='children'),
    Input('submit_button_state', 'n_clicks'),
    State('song_name', 'value')
)
def matches(n_clicks, value):
    if n_clicks is None:
        raise PreventUpdate 
    else:
        song_dict = get_recommendations(value)
        song_list = []
        for i, song in enumerate(song_dict):
            song_item = '{}: {} by {}\n'.format(i+1, song['name'], song['artists'])
            song_list.append(song_item)
        return song_list

@app.callback(
    Output('graph-content', component_property='children'),
    Input('submit_button_graph', 'n_clicks'),
    State('song_name', 'value'),
    State('song_number', 'value')
)
def graph_output(n_clicks, value, number):
    if n_clicks is None:
        return PreventUpdate
    else:
        # plotly_figure = mpl_to_plotly(graph_against(value, int(float(number))))
        # graph = plotly_figure.show()
        graph = graph_against(value, int(float(number)))
        return dcc.Graph(fig=graph)