import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
from Pages.model import get_recommendations, graph_against, plot_plotly
from app import app
import matplotlib as plt
from plotly.tools import mpl_to_plotly
import pandas as pd
import sqlalchemy as db



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
                            dbc.Button('Match!', id='submit_button_state', size='lg', color='success')
                            # html.Button(id='submit_button_state', children='Match!')
                            
                        ]
                    )
                 ),
                dbc.Col(
                    html.Div(
                        [
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
                            dbc.Button('Graph!', id='submit_button_graph', size='lg', color='success')
                            # html.Button(id='submit_button_graph', children='Graph!')
                        ]
                    )
                ),
                dbc.Col(
                    html.Div(id='graph-content')
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
        engine = db.create_engine('sqlite:///Song_Match_db.sqlite3')
        song_dict = get_recommendations(value)
        conn = engine.connect()
        metadata = db.MetaData(conn)
        Song_matches = db.Table('Song_matches', metadata,
                            db.Column('Id', db.Integer, primary_key=True),
                            db.Column('Song', db.String(500), nullable=False),
                            db.Column('Artists', db.String(500), nullable=False),
                            sqlite_autoincrement=True
                        )
        Fav_song = db.Table("Fav_song", metadata,
                            db.Column('Id', db.Integer, primary_key=True),
                            db.Column('Matching_Song_Name', db.String(500), nullable=False),
                            sqlite_autoincrement=True                    
                    )
        metadata.create_all(engine)
        conn.begin()
        query = db.insert(Fav_song).values(Matching_Song_Name=value)
        song_list = []
        for i, song in enumerate(song_dict):
            fav_song=value
            song_item = '{}: {} by {}\n'.format(i+1, song['name'], song['artists'])
            song_list.append(song_item)
            query = db.insert(Song_matches).values(
                                            Song='{}'.format(song['name']),
                                            Artists='{}'.format(song['artists'])
                                        )
            conn.execute(query)
        conn.close()
        return song_list

@app.callback(
    Output('graph-content', component_property='children'),
    Input('submit_button_graph', 'n_clicks'),
    State('song_name', 'value'),
    State('song_number', 'value')
)
def graph_output(n_clicks, value, number):
    if n_clicks == 0:
        raise PreventUpdate
    else:
        if number is None:
            raise PreventUpdate
        else:
            fig = plot_plotly(value, int(float(number)))
            return dcc.Graph(figure=fig)