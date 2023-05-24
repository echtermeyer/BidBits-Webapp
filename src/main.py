import base64
import hashlib
import datetime

from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate

from frontend.home import home_layout
from frontend.serve import serve_layout
from frontend.dashboard import dashboard_layout
from frontend.user import user_layout

from frontend.dashboard import generate_items, create_listing
from frontend.user import personal_data_layout, won_auctions_layout, feedback_layout, payments_layout

from backend.database import Database

file_path = Path(__file__)

db = Database()

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap"], suppress_callback_exceptions=True)
app.layout = serve_layout


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def navigation(pathname):
    if pathname == '/' or pathname is None:
        return home_layout()
    elif pathname == '/dashboard':
        return dashboard_layout(db.get_active_items, db.get_watchlist_items, db.get_categories)
    elif pathname == '/user':
        return user_layout(
            db.get_personal_data,
            db.get_feedback,
            db.get_payments,
            db.get_my_auctions,
            db.get_user_stats()[0]
        )
    else:
        return '404'


@app.callback(
    [Output('error-message', 'children'),
     Output('url', 'pathname'),
     Output('error-modal', 'is_open')],
    [Input('login-submit', 'n_clicks'),
     Input('register-submit', 'n_clicks'),
     Input('close-error-modal', 'n_clicks')],
    [State('login-username', 'value'),
     State('login-password', 'value'),
     State("register-username", "value"),
     State("register-email", "value"),
     State("register-firstname", "value"),
     State("register-lastname", "value"),
     State("register-address", "value"),
     State("register-phone", "value"),
     State("register-password", "value"),
     State("register-confirm-password", "value"),
     State('error-modal', 'is_open')]
)
def login_register(login_clicks, register_clicks, close_clicks, login_username, login_password, register_username, register_email, register_firstname, register_lastname, register_address, register_phone, register_password, register_confirm_password, is_open):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    hash_object = hashlib.sha256()

    if triggered_id == 'login-submit':
        if login_clicks:
            worked, message = db.login(login_username, login_password)
            if worked:
                return "", '/dashboard', False
            else:
                return message, dash.no_update, True
        else:
            raise PreventUpdate

    elif triggered_id == 'register-submit':
        if register_clicks:
            worked, message = db.register(register_username, register_email, register_lastname, register_firstname,
                                          register_address, register_phone, register_password, register_confirm_password)

            if worked:
                return "", '/dashboard', False
            else:
                return message, dash.no_update, True

        else:
            raise PreventUpdate

    elif triggered_id == 'close-error-modal':
        if close_clicks:
            return dash.no_update, dash.no_update, not is_open
        else:
            raise PreventUpdate

    else:
        raise PreventUpdate


@app.callback(
    [
        Output("all-bids-content", "children"),
        Output("watchlist-content", "children"),
        Output("create-listing-content", "children"),
        Output("all-bids-content", "style"),
        Output("watchlist-content", "style"),
        Output("create-listing-content", "style"),
        Output("all-bids", "style"),
        Output("watchlist", "style"),
        Output("user", "style"),
        Output("create-item", "style"),
    ],
    [
        Input("all-bids", "n_clicks_timestamp"),
        Input("watchlist", "n_clicks_timestamp"),
        Input("user", "n_clicks_timestamp"),
        Input("create-item", "n_clicks_timestamp"),
    ],
    [
        State("all-bids", "n_clicks"),
        State("watchlist", "n_clicks"),
        State("user", "n_clicks"),
        State("create-item", "n_clicks"),
    ],
    prevent_initial_call=True
)
def dashboard_switch_tabs(n1, n2, n3, n4, clicks1, clicks2, clicks3, clicks4):
    ctx = dash.callback_context

    base_style = {"border": "none", "background": "none",
                  "outline": "none", "boxShadow": "none", "color": "black"}
    active_style = {**base_style, "text-decoration": "underline"}

    if not ctx.triggered:
        return generate_items(db.get_active_items(), "All Listings"), html.Div(), html.Div(), {"display": "block"}, {"display": "none"}, {"display": "none"}, active_style, base_style, base_style, base_style
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "all-bids" and (clicks1 is None or clicks1 >= clicks2):
        return generate_items(db.get_active_items(), "All Listings"), html.Div(), html.Div(), {"display": "block"}, {"display": "none"}, {"display": "none"}, active_style, base_style, base_style, base_style
    elif button_id == "watchlist" and (clicks2 is None or clicks2 > clicks1):
        return html.Div(), generate_items(db.get_watchlist_items(), "My Watchlist"), html.Div(), {"display": "none"}, {"display": "block"}, {"display": "none"}, base_style, active_style, base_style, base_style
    elif button_id == "user":
        return html.Div(), html.Div(), html.Div(), {"display": "none"}, {"display": "none"}, {"display": "none"}, base_style, base_style, active_style, base_style
    elif button_id == "create-item":
        return html.Div(), html.Div(), create_listing(db.get_categories, "Create Item for Auction"), {"display": "none"}, {"display": "none"}, {"display": "block"}, base_style, base_style, base_style, active_style
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


@app.callback(
    Output({'type': 'wishlist-button', 'index': MATCH}, 'children'),
    [Input({'type': 'wishlist-button', 'index': MATCH}, 'n_clicks')],
    [State({'type': 'wishlist-button', 'index': MATCH}, 'children'),
     State({'type': 'item_id', 'index': MATCH}, 'children')],  # get item_id from hidden Div
    prevent_initial_call=True,
)
def update_watchlist(n_clicks, current_state, item_id):
    print(
        f"Button clicked. n_clicks = {n_clicks}, current_state = {current_state}")
    if n_clicks == 0:
        return current_state
    elif current_state == "Add to Watchlist":
        db.add_to_watchlist(item_id)
        return "Remove from Watchlist"
    else:
        db.remove_from_watchlist(item_id)
        return "Add to Watchlist"


@app.callback(
    [Output({'type': 'bidder-text', 'index': MATCH}, "hidden"),
     Output({'type': 'bidder-text-error', 'index': MATCH}, "hidden"),
     Output({'type': 'bidder-text-error', 'index': MATCH}, "children")],
    [Input({'type': 'bid-button', 'index': MATCH}, "n_clicks")],
    [State({'type': 'title-text', 'index': MATCH}, 'children'),
     State({'type': 'item_id', 'index': MATCH}, 'children'),
     State({'type': 'bid-input', 'index': MATCH}, 'value')],
    prevent_initial_call=True,
)
def place_bid(n_clicks, title, item_id, bid_amount):
    if n_clicks == 0:
        raise dash.exceptions.PreventUpdate()

    worked, message = db.place_bid(bid_amount, item_id)
    if worked:
        return False, True, ""
    else:
        return True, False, message
    

@app.callback(
    [
        Output("personal-data-content", "children"),
        Output("won-auctions-content", "children"),
        Output("feedback-content", "children"),
        Output("payments-content", "children"),
        Output("personal-data-content", "style"),
        Output("won-auctions-content", "style"),
        Output("feedback-content", "style"),
        Output("payments-content", "style")
    ],
    [
        Input("personal-data", "n_clicks"),
        Input("won-auctions", "n_clicks"),
        Input("feedback", "n_clicks"),
        Input("payments", "n_clicks"),
    ]
)
def user_switch_Tabs(personal_data_clicks, won_auctions_clicks, feedback_clicks, payments_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "personal-data" or button_id == 'interval-component':
        return personal_data_layout(db.get_personal_data), None, None, None, {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif button_id == "won-auctions" or button_id == 'interval-component':
        return None, won_auctions_layout(db.get_my_auctions, db.get_user_stats()[0]), None, None, {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
    elif button_id == "feedback" or button_id == 'interval-component':
        return None, None, feedback_layout(db.get_feedback, db.get_user_stats()[0]), None, {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}
    elif button_id == "payments" or button_id == 'interval-component':
        return None, None, None, payments_layout(db.get_payments, db.get_user_stats()[0]), {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}
    else:
        return personal_data_layout(db.get_personal_data), None, None, None, {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}


@app.callback(
    Output('update-message', 'children'),
    [Input('update-submit', 'n_clicks')],
    [State('update-email', 'value'),
     State('update-firstname', 'value'),
     State('update-lastname', 'value'),
     State('update-address', 'value'),
     State('update-phone', 'value')]
)
def update_user_information(n, email, firstname, lastname, address, phone):
    if n is None or n == 0:
        raise dash.exceptions.PreventUpdate()

    print(email, firstname, lastname, address, phone)
    worked, message = db.update_userdata(
        email, firstname, lastname, address, phone)
    if worked:
        return dbc.Alert("Your data was updated successfully!", color="success")
    else:
        return dbc.Alert(message, color="danger")


@app.callback(Output('uploaded-file-name', 'children'),
              Input('item-image', 'filename'))
def upload_file(list_of_names):
    if list_of_names is not None:
        return html.P(f"Uploaded file: {list_of_names}")
    else:
        return html.P("No file uploaded yet.")


@app.callback(
    Output('alert-container', 'children'),
    [Input('start-auction', 'n_clicks')],
    [State('item-title', 'value'),
     State('item-description', 'value'),
     State('item-category', 'value'),
     State('item-start-price', 'value'),
     State('item-auction-duration', 'value'),
     State('item-image', 'contents')]
)
def list_item_for_auction(n, title, description, category, start_price, auction_duration, image_data):
    if n is None:
        return dash.no_update

    if None in (title, description, category, start_price, auction_duration, image_data):
        return dbc.Alert("All fields must be filled in!", color="danger")

    _, content_string = image_data.split(',')
    decoded = base64.b64decode(content_string)

    image_path = (file_path.parent / "assets") / \
        f'upload-{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg'
    with open(image_path, 'wb') as f:
        f.write(decoded)

    worked, message = db.create_item(
        title, description, category, start_price, auction_duration, image_path)

    if worked:
        return dbc.Alert("Created new item successfully!", color="success")
    else:
        return dbc.Alert(message, color="danger")


@app.callback(
    Output({'type': 'dynamic-button', 'index': 'delete-user-submit'}, 'children'),
    Input({'type': 'dynamic-button', 'index': 'delete-user-submit'}, 'n_clicks')
)
def delete_user(n_clicks):
    if n_clicks is None:
        raise PreventUpdate

    db.delete_userdata()

    return "Button clicked {} times".format(n_clicks)


@app.callback(
    [Output({"type": "feedback-input", "index": MATCH}, "value"),
     Output({"type": "feedback-success", "index": MATCH}, "children"),
     Output({"type": "submit-button", "index": MATCH}, "disabled")],  # Add this line
    Input({"type": "submit-button", "index": MATCH}, "n_clicks"),
    [State({"type": "feedback-input", "index": MATCH}, "value"),
     State({"type": "rating-slider", "index": MATCH}, "value"),
     State({"type": "item-id", "index": MATCH}, "children")],
)
def give_feedback(n_clicks, feedback, rating, item_id):
    if n_clicks is None:
        raise PreventUpdate
    
    item_id = item_id.split('#')[1]
    db.give_feedback(item_id, rating, feedback)
        
    return "", html.Span("Feedback sent!", style={"color": "green"}), True  # Return True to disable the button




if __name__ == "__main__":
    app.run_server(debug=False, host='0.0.0.0', port=8051)
