import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


from backend.dashboard import generate_add_bids, generate_wishlist


def dashboard_layout():
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.H1("Dashboard", style={"font-family": "Roboto", "text-align": "center", "font-size": "3rem", "font-weight": "bold", "margin-top": "3rem", "margin-bottom": "1rem", "color": "black"}),
        
        html.Div([
            dbc.Button("All Bids", id="all-bids", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black", "text-decoration": "underline"}),
            dbc.Button("Watchlist", id="watchlist", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
        ], style={"text-align": "center", "margin-top": "3rem"}),

        html.Div(style={"height": "70vh", "overflow": "auto", "margin-top": "2rem"},
                 children=[
                     html.Div(id="all-bids-content", children=generate_add_bids()),
                     html.Div(id="watchlist-content", children=generate_wishlist(), style={'display': 'none'})
                 ]),

        dbc.NavLink(
            dbc.NavItem(dbc.NavLink("User", active=True, href="#")),
            style={"position": "absolute", "right": "10px", "top": "10px", "color": "black", "margin": "1rem"}
        )
    ])
