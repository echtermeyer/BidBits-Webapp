import dash_bootstrap_components as dbc
import dash_html_components as html


def generate_add_bids():
    items = []
    for i in range(1, 5):
        item = dbc.Card([
            dbc.Row([
                dbc.Col(dbc.CardImg(src=f"/assets/item{i}.jpg", top=True), width=6),
                dbc.Col(dbc.CardBody([
                    html.H4(f"Item {i} Title", className="card-title", id={'type': 'title-text', 'index': i}),
                    html.P(f"Some detailed description about Item {i}.", className="card-text"),
                    html.H6(f"Highest Bid: ${500 * i}", className="card-text"),
                    html.H6(f"Time left: {2 * i} days", className="card-text"),
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Place Bid"),
                            dbc.Input(id={'type': 'bid-input', 'index': i}, type="number", placeholder="Amount"),
                            dbc.Button("Confirm Bid", id={'type': 'bid-button', 'index': i}, n_clicks=0, color="secondary", className="mt-auto")
                        ],
                        className="mt-3",
                    ),
                    html.Div("You are the highest bidder", id={'type': 'bidder-text', 'index': i}, hidden=True, style={"color": "green", "margin-top": "1rem"}),
                    dbc.Button("Add to Watchlist", id={'type': 'wishlist-button', 'index': i}, n_clicks=0, color="secondary", style={"margin-top": "2rem"}),
                    html.Div(style={"flex-grow": "1"}),  # Spacer
                ], className="d-flex flex-column"), width=6)
            ])
        ], style={"width": "50%", "margin": "1rem auto"})
        items.append(item)
    return items



def generate_wishlist():
    items = []
    for i in range(1, 3):
        item = dbc.Card([
            dbc.Row([
                dbc.Col(dbc.CardImg(src=f"/assets/item{i}.jpg", top=True), width=6),
                dbc.Col(dbc.CardBody([
                    html.H4(f"Whishlist {i} Title", className="card-title"),
                    html.P(f"Some detailed description about Item {i}.", className="card-text"),
                    html.H6(f"Highest Bid: ${500 * i}", className="card-text"),
                    html.H6(f"Time left: {2 * i} days", className="card-text"),
                    dbc.Button("Remove from Wishlist", id={'type': 'wishlist-button', 'index': i}, n_clicks=0, color="secondary", className="mt-auto")
                ]), width=6)
            ])
        ], style={"width": "50%", "margin": "1rem auto"})
        items.append(item)
    return items


def add_bid_to_wishlist():
    pass


def remove_bid_from_whishlist():
    pass
