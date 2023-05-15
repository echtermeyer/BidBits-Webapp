from dash import html
from dash import dcc

from .home import home_layout

def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', children=home_layout())
    ])