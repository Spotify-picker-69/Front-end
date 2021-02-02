# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Imports from this application
from app import app

homepage_text = """

                ## What's your next favorite song?

                Spotify Picker will be able to choose at least 10 songs that matches your favorite song.

                Perfect for building playlists for your high school crush, or identifying songs to remix together.

                Possiblities are endless for the Spotify Picker.

                """

# 2 column layout. 1st column width = 4/12
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/layout
column1 = dbc.Col(
    [
        dcc.Markdown(homepage_text),
        dcc.Link(dbc.Button(
                            'Find your song matches now!',
                            color='success', size='lg'), href='/picker')
    ],
    md=4,
)

column2 = dbc.Col(
    [
        html.Img(src='assets\Couple_listening.png', className='img-fluid'),
    ]
)

layout = dbc.Row([column1, column2])
