import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from Pages.model import get_recommendations, graph_against
from app import app
import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
from plotly.tools import mpl_to_plotly



row = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [
                        dcc.Markdown('## Enter the Song of Your Choice!', className='mb-5'),
                        dcc.Markdown('### Song Name'),
                        dcc.Input(
                                id='song_name',
                                #placeholder='Song',
                                type='text',
                                value=''
                            ),
                        dbc.Button(
                                "Match",
                                id="submit_song_name",
                                color="success",
                                size="lg",
                                className="mr-2"
                        )
                        
                    ]
                )),
                dbc.Col(
                    [
                        html.H2('Matched songs', className='mb-5'),
                        html.Div(id="match-content", className="lead")
                    ]
                )
            ]
        ),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    [
                        dcc.Markdown('### Compare your song to a song in the list'),
                        dcc.Input(
                            id='song_number',
                            placeholder='Song Number',
                            type='number',
                            value=''
                            ),
                        dbc.Button(
                                'Graph!',
                                id='graph_name',
                                color='success',
                                size='lg',
                                className='mr-2'
                            )
                        ]
                    )
                )
            ]
        ),
        dbc.Row(
            html.Div(id='graph-content'
                )
                )
        
    ]
)



# adding callback
@app.callback(
    Output('match-content', component_property='children'),
    Input('submit_song_name', 'n_clicks'),
    State('song_name', 'value')
)
def matches(value, n_clicks):
    if value is None:
        return 'Please type in a song'
    else:
        song_dict = get_recommendations(value)
        song_list = []
        for i, song in enumerate(song_dict):
            song_item = '{}: {} by {}\n'.format(i+1, song['name'], song['artists'])
            song_list.append(song_item)
        return song_list


@app.callback(
    Output('graph-content', component_property='children'),
    Input('song_name', 'value'),
    State('song_number', 'number')
)
def graph_output(number, value):
    if value is None:
        value = 1
        plotly_figure = graph_against(number, int(float(value)))
        return plotly_figure
    else:
        plotly_figure = graph_against(number, int(float(value)))
        return plotly_figure


layout = row