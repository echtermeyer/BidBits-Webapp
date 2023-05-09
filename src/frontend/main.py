import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

from layouts.home import home_layout
from layouts.serve import serve_layout
from layouts.dashboard import dashboard_layout

from checks import check_valid_login, check_valid_registration


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
     Output("dashboard-content", "children")],
    [Input("all-bids", "n_clicks_timestamp"),
     Input("watchlist", "n_clicks_timestamp")],
    [State("all-bids", "n_clicks"),
     State("watchlist", "n_clicks")],
     prevent_initial_call=True
)
def switch_tab(n1, n2, clicks1, clicks2):
    ctx = dash.callback_context

    if not ctx.triggered:
        return dash.no_update, dash.no_update, dash.no_update
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    base_style = {"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}
    active_style = {**base_style, "text-decoration": "underline"}

    if button_id == "all-bids" and (clicks1 is None or clicks1 >= clicks2):
        return active_style, base_style, "All bids are displayed here"
    elif button_id == "watchlist" and (clicks2 is None or clicks2 > clicks1):
        return base_style, active_style, "Your watchlist"
    else:
        return dash.no_update, dash.no_update, dash.no_update


if __name__ == "__main__":
    app.run_server(debug=True)
