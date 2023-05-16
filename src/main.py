import base64
import datetime

from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash import html
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate

from frontend.layouts.home import home_layout
from frontend.layouts.serve import serve_layout
from frontend.layouts.dashboard import dashboard_layout
from frontend.layouts.user import user_layout
from frontend.layouts.create import create_bid_layout

from frontend.checks import check_valid_login, check_valid_registration

from backend.database import Database
from backend.dashboard import add_bid_to_wishlist, remove_bid_from_whishlist

file_path = Path(__file__)

db = Database()

app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap"], suppress_callback_exceptions=True)
app.layout = serve_layout


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname is None:
        return home_layout()
    elif pathname == '/dashboard':
        return dashboard_layout(db.get_active_items, db.get_watchlist_items)
    elif pathname == '/user':
        return user_layout(
            db.get_personal_data,
            db.get_feedback,
            db.get_payments,
            db.get_won_auctions,
            db.get_agg_total_paid,
            db.get_agg_user_rating,
            db.get_agg_won_auctions,
            db.get_agg_participated_auctions
        )
    elif pathname == '/create':
        return create_bid_layout()
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
def navigate_to_dashboard(login_clicks, register_clicks, close_clicks, login_username, login_password, register_username, register_email, register_firstname, register_lastname, register_address, register_phone, register_password, register_confirm_password, is_open):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]

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
    [Output("all-bids", "style"),
     Output("watchlist", "style"),
     Output("user", "style"),
     Output("create-item", "style"),
     Output("all-bids-content", "style"),
     Output("watchlist-content", "style")],
    [Input("all-bids", "n_clicks_timestamp"),
     Input("watchlist", "n_clicks_timestamp"),
     Input("user", "n_clicks_timestamp"),
     Input("create-item", "n_clicks_timestamp")],
    [State("all-bids", "n_clicks"),
     State("watchlist", "n_clicks"),
     State("user", "n_clicks"),
     State("create-item", "n_clicks")],
    prevent_initial_call=True
)
def switch_tab(n1, n2, n3, n4, clicks1, clicks2, clicks3, clicks4):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, {"display": "block"}, {"display": "none"}
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    base_style = {"border": "none", "background": "none",
                  "outline": "none", "box-shadow": "none", "color": "black"}
    active_style = {**base_style, "text-decoration": "underline"}

    if button_id == "all-bids" and (clicks1 is None or clicks1 >= clicks2):
        return active_style, base_style, base_style, base_style, {"display": "block"}, {"display": "none"}
    elif button_id == "watchlist" and (clicks2 is None or clicks2 > clicks1):
        return base_style, active_style, base_style, base_style, {"display": "none"}, {"display": "block"}
    elif button_id == "user":
        return base_style, base_style, active_style, base_style, {"display": "none"}, {"display": "none"}
    elif button_id == "create-item":
        return base_style, base_style, base_style, active_style, {"display": "none"}, {"display": "none"}
    else:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, {"display": "block"}, {"display": "none"}


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
    [Output({'type': 'bid-button', 'index': MATCH}, "disabled"),
     Output({'type': 'bidder-text', 'index': MATCH}, "hidden")],
    [Input({'type': 'bid-button', 'index': MATCH}, "n_clicks")],
    [State({'type': 'title-text', 'index': MATCH}, 'children'),
     # get item_id from hidden Div
     State({'type': 'item_id', 'index': MATCH}, 'children'),
     State({'type': 'bid-input', 'index': MATCH}, 'value')],  # get bid amount from input field
    prevent_initial_call=True,
)
def on_confirm_bid(n_clicks, title, item_id, bid_amount):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate()

    worked, message = db.place_bid(bid_amount, item_id)
    if worked:
        return True, False
    else:
        raise dash.exceptions.PreventUpdate()


@app.callback(
    [
        Output("personal-data-content", "style"),
        Output("won-auctions-content", "style"),
        Output("feedback-content", "style"),
        Output("payments-content", "style")
    ],
    [
        Input("personal-data", "n_clicks"),
        Input("won-auctions", "n_clicks"),
        Input("feedback", "n_clicks"),
        Input("payments", "n_clicks")
    ]
)
def update_content_visibility(personal_data_clicks, won_auctions_clicks, feedback_clicks, payments_clicks):
    ctx = dash.callback_context
    button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "personal-data":
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}
    elif button_id == "won-auctions":
        return {"display": "none"}, {"display": "block"}, {"display": "none"}, {"display": "none"}
    elif button_id == "feedback":
        return {"display": "none"}, {"display": "none"}, {"display": "block"}, {"display": "none"}
    elif button_id == "payments":
        return {"display": "none"}, {"display": "none"}, {"display": "none"}, {"display": "block"}
    else:
        return {"display": "block"}, {"display": "none"}, {"display": "none"}, {"display": "none"}


@app.callback(
    Output('update-message', 'children'),
    [Input('update-submit', 'n_clicks')],
    [State('update-email', 'value'),
     State('update-firstname', 'value'),
     State('update-lastname', 'value'),
     State('update-address', 'value'),
     State('update-phone', 'value')]
)
def update_user(n, email, firstname, lastname, address, phone):
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
def update_uploaded_file_name(list_of_names):
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
def on_button_click(n, title, description, category, start_price, auction_duration, image_data):
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


if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=8051)
