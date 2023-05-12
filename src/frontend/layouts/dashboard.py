import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc


from backend.dashboard import retrieve_all_items, retrieve_watchlist


def dashboard_layout():
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.H1("Dashboard", style={"font-family": "Roboto", "text-align": "center", "font-size": "3rem", "font-weight": "bold", "margin-top": "3rem", "margin-bottom": "1rem", "color": "black"}),
        
        html.Div([
            dbc.Button("Create Item", id="create-item", href="/create", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("All Listings", id="all-bids", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("My Watchlist", id="watchlist", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("User", id="user", href="/user", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
        ], style={"text-align": "center", "margin-top": "3rem"}),

        html.Div(style={"height": "70vh", "overflow": "auto", "margin-top": "2rem"},
                 children=[
                     html.Div(id="all-bids-content", children=generate_items(retrieve_all_items())),
                     html.Div(id="watchlist-content", children=generate_items(retrieve_watchlist()), style={'display': 'none'})
                 ]),
    ])


def generate_items(items):
    elements = []
    for i, item in enumerate(items):
        if item["is_watchlist"]:
            watchlist_text = "Remove from Watchlist"
        else:
            watchlist_text = "Add to Watchlist"

        item = dbc.Card([
            dbc.Row([
                dbc.Col(dbc.CardImg(src=f"/assets/{item['image_path']}", top=True), width=6),
                dbc.Col(dbc.CardBody([
                    html.H4(item["title"], className="card-title", id={'type': 'title-text', 'index': i}),
                    html.P(item["description"], className="card-text"),
                    html.H6(f"Highest Bid: ${item['highest_bid']}", className="card-text"),
                    html.H6(f"Time left: {item['time_left']} days", className="card-text"),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Place Bid"),
                            dbc.Input(id={'type': 'bid-input', 'index': i}, type="number", placeholder="Amount"),
                            dbc.Button("Confirm Bid", id={'type': 'bid-button', 'index': i}, n_clicks=0, color="secondary", className="mt-auto")
                        ],
                        className="mt-3",
                    ),
                    html.Div("You are the highest bidder", id={'type': 'bidder-text', 'index': i}, hidden=True, style={"color": "green", "margin-top": "1rem"}),
                    dbc.Button(watchlist_text, id={'type': 'wishlist-button', 'index': i}, n_clicks=0, color="secondary", style={"margin-top": "2rem"}),
                    html.Div(style={"flex-grow": "1"}),  # Spacer
                ], className="d-flex flex-column"), width=6)
            ])
        ], style={"width": "50%", "margin": "1rem auto"})
        elements.append(item)
    return elements
