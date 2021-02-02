import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
# TODO - import for recommend_songs function
from app import app


column1 = (
    [
        dcc.Markdown('## Enter a song followed by the year it came out!', className='mb-5'),
        dcc.Markdown('### Song Name'),
        dcc.Input(
            id='song_name',
            placeholder='Song',
            type='text',
            value=''
        ),
        dcc.Markdown('### Year'),
        dcc.Input(
            id='year',
            placeholder='Year',
            type='text',
            value=''
        ),
        dbc.Button("Match!", id='match-content', color='success', size='lg', className='mr-2')
    ],
    #md=4
)

column2 = dbc.Col(
    [
        html.H2('Here are your Top 10 matched songs', className='mb-5'),
        html.Div(id='match-content', className='lead')
    ]
)

# adding callback
@app.callback(
    Output('match-content', 'children'),
    [Input('song_name', 'value'), Input('year', 'value')],
)
def matches(song, year):
    input_dict = {'name': song,
                    'year': year}
    match_songs_dict = recommend_songs([input_dict])
    matched_songs = []
    for match in match_songs:
        song = '{}, by {}, relased in: {}'.format(match['name'], match['artists'], match['year'])
        return song

layout = dbc.Row([column1, column2])


