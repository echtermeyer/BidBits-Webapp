import dash_bootstrap_components as dbc
import dash_html_components as html


def generate_add_bids():
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
                    html.H4(f"Item {i} Title", className="card-title"),
                    html.P(f"Some detailed description about Item {i}.", className="card-text"),
                    html.H6(f"Highest Bid: ${500 * i}", className="card-text"),
                    html.H6(f"Time left: {2 * i} days", className="card-text"),
                    dbc.Button("Add to Wishlist", id={'type': 'wishlist-button', 'index': i}, n_clicks=0, color="secondary", className="mt-auto")
                ]), width=6)
            ])
        ], style={"width": "50%", "margin": "1rem auto"})
        items.append(item)
    return items