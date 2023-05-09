import dash_html_components as html
import dash_core_components as dcc

from layouts.home import home_layout


def serve_layout():
    return html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content', children=home_layout())
    ])