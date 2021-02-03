import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
from Pages.model import get_recomendations
from app import app



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
                        html.Table([
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
                        ])
                        # html.Div(id="match-content", className="lead")
                    ]
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
    Input('submit_song_name', 'n_clicks'),
    State('song_name', 'value')
)
def matches(value, n_clicks):
    song_dict = get_recomendations(value)
    song_list = []
    for song in song_dict:
        song = '{} by {}'.format(song['name'], song['artists'])
        song_list.append(song)
        
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
'''def matches(value, n_clicks):
    if value is None:
        return 'Please type in a song'
    else:
        song_dict = get_recomendations(value)
        song_list = []
        for song in song_dict:
            song = '{} by {}'.format(song['name'], song['artists'])
            song_list.append(song)
        
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
        
        return song1, song2, song3, song4, song5, song6, song7, song8, song9, song10 '''

layout = row