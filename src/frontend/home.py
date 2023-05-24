from dash import html
import dash_bootstrap_components as dbc


def home_layout():
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.H1("BidBits", style={"fontFamily": "Roboto", "textAlign": "center", "fontSize": "3rem", "fontWeight": "bold", "marginTop": "3rem"}),

        dbc.Row([
            dbc.Col([
                html.H2("Registration", style={"fontFamily": "Roboto", "textAlign": "left", "paddingLeft": "20%"}),

                html.Label("Username", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-username", type="text", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("Email", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-email", type="email", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("First Name", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-firstname", type="text", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("Last Name", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-lastname", type="text", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("Address", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-address", type="text", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("Phone Number", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-phone", type="text", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("Password", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-password", type="password", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("Confirm Password", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="register-confirm-password", type="password", style={"width": "60%", "marginLeft": "20%"}),

                dbc.Button("Register", id="register-submit", color="primary", style={"fontFamily": "Roboto", "width": "60%", "marginTop": "1rem", "marginLeft": "20%"})
            ], width=6),

            dbc.Col([
                html.H2("Login", style={"fontFamily": "Roboto", "textAlign": "left", "paddingLeft": "20%"}),

                html.Label("Username", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="login-username", type="text", style={"width": "60%", "marginLeft": "20%"}),

                html.Label("Password", style={"fontFamily": "Roboto", "paddingLeft": "20%"}),
                dbc.Input(id="login-password", type="password", style={"width": "60%", "marginLeft": "20%"}),

                dbc.Button("Submit", id="login-submit", color="primary", style={"fontFamily": "Roboto", "width": "60%", "marginTop": "1rem", "marginLeft": "20%"})
            ], width=6),
        ], style={"height": "100vh", "marginTop": "5%"}),

        dbc.Modal(
            [
                dbc.ModalHeader("Error"),
                dbc.ModalBody(id="error-message"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close-error-modal", className="ml-auto")
                ),
            ],
            id="error-modal",
        )
    ])