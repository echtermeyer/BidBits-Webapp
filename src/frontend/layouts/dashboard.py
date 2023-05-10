import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


def dashboard_layout():
    items = []

    for i in range(1, 4):
        item = dbc.Card([
            dbc.Row([
                dbc.Col(dbc.CardImg(src=f"/assets/item{i}.jpg", top=True), width=6),
                dbc.Col(dbc.CardBody([
                    html.H4(f"Item {i} Title", className="card-title"),
                    html.P(f"Some detailed description about Item {i}.", className="card-text"),
                    html.H6(f"Highest Bid: ${500 * i}", className="card-text"),
                    html.H6(f"Time left: {2 * i} days", className="card-text"),
                    dbc.Button("Add to Wishlist", id={'type': 'wishlist-button', 'index': i}, n_clicks=0, color="secondary", className="mt-auto")  
                ]), width=6)
            ])
        ], style={"width": "40%", "margin": "1rem auto"})
        items.append(item)

    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.H1("Dashboard", style={"font-family": "Roboto", "text-align": "center", "font-size": "3rem", "font-weight": "bold", "margin-top": "3rem", "margin-bottom": "1rem", "color": "black"}),
        
        html.Div([
            dbc.Button("All Bids", id="all-bids", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black", "text-decoration": "underline"}),
            dbc.Button("Watchlist", id="watchlist", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
        ], style={"text-align": "center", "margin-top": "3rem"}),

        html.Div(style={"height": "70vh", "overflow": "auto", "margin-top": "2rem"},
                 children=[
                     html.Div(id="all-bids-content", children=items),
                     html.Div(id="watchlist-content", children=items, style={'display': 'none'})
                 ]),

        dbc.NavLink(
            dbc.NavItem(dbc.NavLink("User", active=True, href="#")),
            style={"position": "absolute", "right": "10px", "top": "10px", "color": "black", "margin": "1rem"}
        )
    ])
