import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


def user_layout():
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.H1("Dashboard", style={"font-family": "Roboto", "text-align": "center", "font-size": "3rem", "font-weight": "bold", "margin-top": "3rem", "margin-bottom": "1rem", "color": "black"}),
        
        dcc.Link('Go back to main page', href='/dashboard')
    ])