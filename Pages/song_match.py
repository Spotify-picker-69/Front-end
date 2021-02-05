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
                            dcc.Markdown(
                                    '## Enter the Song of your choice!'
                                    ),
                            dcc.Markdown('### Song Name'),
                            dcc.Input(
                                id='song_name',
                                type='text',
                            ),
                            dbc.Button(
                                        'Match!',
                                        id='submit_button_state',
                                        size='lg',
                                        color='success')
                        ]
                    )
                 ),
                dbc.Col(
                    html.Div(
                        [
                            dcc.Markdown('## Matched Songs'),
                            html.Table(
                                [
                                    html.Tr(html.Td(id='song_1')),
                                    html.Tr(html.Td(id='song_2')),
                                    html.Tr(html.Td(id='song_3')),
                                    html.Tr(html.Td(id='song_4')),
                                    html.Tr(html.Td(id='song_5')),
                                    html.Tr(html.Td(id='song_6')),
                                    html.Tr(html.Td(id='song_7')),
                                    html.Tr(html.Td(id='song_8')),
                                    html.Tr(html.Td(id='song_9')),
                                    html.Tr(html.Td(id='song_10'))
                                ]
                            )
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
                            dcc.Markdown(
                                '### Compare your song to a song in the list'
                                    ),
                            dcc.Markdown(
                                    'Enter Song Number from List'
                                    ),
                            dcc.Input(
                                id='song_number',
                                placeholder='Song Number',
                                type='text'
                            ),
                            dbc.Button(
                                    'Graph!',
                                    id='submit_button_graph',
                                    size='lg',
                                    color='success'),
                            dcc.Markdown(
                                        '''

                                        \nValence: 0-1 Describes the musical positivness
                                        \nTempo: The estimated Track Tempo
                                        \nSpeechiness: 0-1 Detects the presence of spoken words
                                        \nPopularity: How popular the song is
                                        \nMode: Indicates the modality (major or minor) of a track
                                        \nLoudness: How loud the song is in decibels(dB)
                                        \nLiveness: 0-1 Probabliity the song is a live recording
                                        \nKey: What musical key the song is in
                                        \nInstrumentalness: 0-1 How much the track lacks vocals
                                        \nExplicit: Whether the track has explicit words
                                        \nEnergy: 0-1 Measures how energetic the song feels
                                        \nDuration_ms: How long the song is in milliseconds
                                        \nDanceability: 0-1 How suitable the song is for dancing
                                        \nAcousticness: 0-1 Probablity the song is acoustic
                                        '''
                            )
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
    Output('song_1', component_property='children'),
    Output('song_2', component_property='children'),
    Output('song_3', component_property='children'),
    Output('song_4', component_property='children'),
    Output('song_5', component_property='children'),
    Output('song_6', component_property='children'),
    Output('song_7', component_property='children'),
    Output('song_8', component_property='children'),
    Output('song_9', component_property='children'),
    Output('song_10', component_property='children'),
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
        Song_matches = db.Table(
                            'Song_matches', metadata,
                            db.Column(
                                    'Id',
                                    db.Integer,
                                    primary_key=True
                                    ),
                            db.Column(
                                    'Song',
                                    db.String(500),
                                    nullable=False
                                    ),
                            db.Column(
                                'Artists',
                                db.String(500),
                                nullable=False
                                    ),
                            sqlite_autoincrement=True
                        )
        Fav_song = db.Table(
                            "Fav_song", metadata,
                            db.Column(
                                    'Id',
                                    db.Integer,
                                    primary_key=True
                                    ),
                            db.Column(
                                    'Matching_Song_Name',
                                    db.String(500),
                                    nullable=False
                                    ),
                            sqlite_autoincrement=True
                    )
        metadata.create_all(engine)
        conn.begin()
        query = db.insert(Fav_song).values(Matching_Song_Name=value)
        song_list = []
        for i, song in enumerate(song_dict):
            fav_song = value
            song_item = '{}: {} by {}\n'.format(
                                                i+1,
                                                song['name'],
                                                song['artists']
                                                )
            song_list.append(song_item)
            query = db.insert(Song_matches).values(
                                            Song='{}'.format(
                                                            song['name']
                                                            ),
                                            Artists='{}'.format(
                                                            song['artists']
                                                            )
                                        )
            conn.execute(query)
        conn.close()
        song1 = song_list[0]
        song2 = song_list[1]
        song3 = song_list[2]
        song4 = song_list[3]
        song5 = song_list[4]
        song6 = song_list[5]
        song7 = song_list[6]
        song8 = song_list[7]
        song9 = song_list[8]
        song10 = song_list[9]
        return song1, song2, song3, song4, song5, song6, song7, song8, song9, song10


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
