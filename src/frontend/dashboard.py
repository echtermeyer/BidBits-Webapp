import dash_bootstrap_components as dbc
from dash import html


def dashboard_layout(fn_get_all_items, fn_get_watchlist_items):
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.H1("Dashboard", style={"fontFamily": "Roboto", "textAlign": "center", "fontSize": "3rem", "fontWeight": "bold", "marginTop": "3rem", "marginBottom": "1rem", "color": "black"}),
        
        html.Div([
            dbc.Button("Create Item", id="create-item", href="/create", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "boxShadow": "none", "color": "black"}),
            dbc.Button("All Listings", id="all-bids", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "boxShadow": "none", "color": "black"}),
            dbc.Button("My Watchlist", id="watchlist", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "boxShadow": "none", "color": "black"}),
            dbc.Button("User", id="user", href="/user", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "boxShadow": "none", "color": "black"}),
        ], style={"textAlign": "center", "marginTop": "3rem"}),

        html.Div(style={"height": "70vh", "overflow": "auto", "marginTop": "2rem"},
                 children=[
                     html.Div(id="all-bids-content", children=generate_items(fn_get_all_items(), "All Listings")),
                     html.Div(id="watchlist-content", children=generate_items(fn_get_watchlist_items(), "My Watchlist"), style={'display': 'none'})
                 ]),
    ])


def generate_items(items, title):
    elements = [
        html.H2(title, style={"fontFamily": "Roboto", "textAlign": "center"}),
    ]

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
                    html.H6(f"Item Code: #{item['item_id']}", className="card-text"),
                    html.P(item["description"], className="card-text"),
                    html.H6(f"Seller: {item['seller']}", className="card-text"),
                    html.H6(f"Highest Bidder: {item['highest_bidder']}", className="card-text"),
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
                    html.Div("You are the highest bidder", id={'type': 'bidder-text', 'index': i}, hidden=True, style={"color": "green", "marginTop": "1rem"}),
                    html.Div("Error. Try again later", id={'type': 'bidder-text-error', 'index': i}, hidden=True, style={"color": "red", "marginTop": "1rem"}),
                    dbc.Button(watchlist_text, id={'type': 'wishlist-button', 'index': i}, n_clicks=0, color="secondary", style={"marginTop": "2rem"}),
                    html.Div(style={"flexGrow": "1"}),  
                    html.Div(item['item_id'], id={'type': 'item_id', 'index': i}, style={'display': 'none'})
                ], className="d-flex flex-column"), width=6)
            ])
        ], style={"width": "50%", "margin": "1rem auto"})
        elements.append(item)
    return elements