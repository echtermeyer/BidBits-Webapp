import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH
from dash.exceptions import PreventUpdate

from frontend.layouts.home import home_layout
from frontend.layouts.serve import serve_layout
from frontend.layouts.dashboard import dashboard_layout
from frontend.layouts.user import user_layout
from frontend.layouts.create import create_bid_layout

from frontend.checks import check_valid_login, check_valid_registration

from backend.user import login_user, register_user
from backend.dashboard import generate_add_bids, generate_wishlist
from backend.dashboard import add_bid_to_wishlist, remove_bid_from_whishlist


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, "https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap"], suppress_callback_exceptions=True)
app.layout = serve_layout


@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/' or pathname is None:
        return home_layout()
    elif pathname == '/dashboard':
        return dashboard_layout()
    elif pathname == '/user':
        return user_layout()
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
            message, failed = check_valid_login(login_username, login_password)
            if failed:
                return message, dash.no_update, True
            else:
                return "", '/dashboard', False
        else:
            raise PreventUpdate

    elif triggered_id == 'register-submit':
        if register_clicks:
            message, failed = check_valid_registration(register_username, register_email, register_firstname, register_lastname, register_address, register_phone, register_password, register_confirm_password)
            if failed:
                return message, dash.no_update, True
            else:
                return "", '/dashboard', False
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

    base_style = {"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}
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
    [State({'type': 'wishlist-button', 'index': MATCH}, 'children')],
    prevent_initial_call=True,
)
def update_wishlist_button(n_clicks, current_state):
    print(f"Button clicked. n_clicks = {n_clicks}, current_state = {current_state}")
    if n_clicks == 0:
        return current_state
    elif current_state == "Add to Watchlist":
        print("Adding bid to wishlist")
        add_bid_to_wishlist()
        return "Remove from Watchlist"
    else:
        print("Removing bid from wishlist")
        remove_bid_from_whishlist()
        return "Add to Watchlist"
    

@app.callback(
    [Output({'type': 'bid-button', 'index': MATCH}, "disabled"),
     Output({'type': 'bidder-text', 'index': MATCH}, "hidden")],
    [Input({'type': 'bid-button', 'index': MATCH}, "n_clicks")],
    [State({'type': 'title-text', 'index': MATCH}, 'children')],
    prevent_initial_call=True,
)
def on_confirm_bid(n_clicks, title):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate()
    print(title) 
    return True, False 



if __name__ == "__main__":
    app.run_server(debug=True)
