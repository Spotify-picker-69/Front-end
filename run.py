# Imports from 3rd party libraries
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Imports from this application
from app import app, server
from Pages import song_match, index


# Navbar docs
# https://dash-bootstrap-components.opensource.faculty.ai/l/components/navbar
navbar = dbc.NavbarSimple(
    brand='Spotify Picker',
    brand_href='/',
    children=[
        dbc.NavItem(dcc.Link(
            'Song Match',
            href='/song_match',
            className='nav-link')
            )
    ],
    sticky='top',
    color='#1DB954',
    light=True,
    dark=False
)


footer = dbc.Container(
    dbc.Row(
        dbc.Col(
            html.P(
                [
                    html.Span('Track Team 69', className='Track Team 69'),
                    # html.A(html.I(className='fas fa-envelope-square mr-1'),
                    # href='mailto:johncarlopez.88@gmail.com'),
                    html.A(html.I(
                        className='fab fa-github-square mr-1'),
                        href='https://github.com/Lopez-John/Spotify-picker-69'),
                    # html.A(html.I(className='fab fa-linkedin mr-1'),
                    # href='https://www.linkedin.com/in/<you>/'),
                    html.A(html.I(
                        className='fab fa-twitter-square mr-1'),
                        href='https://twitter.com/ds_lad'),
                ],
                className='lead'
            )
        )
    )
)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    dbc.Container(id='page-content', className='mt-4'),
    html.Hr(),
    footer
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return index.layout
    elif pathname == '/song_match':
        return song_match.layout
    else:
        return dcc.Markdown('## Page not found')


if __name__ == '__main__':
    app.run_server(debug=True)
