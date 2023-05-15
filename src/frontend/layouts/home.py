from dash import html
import dash_bootstrap_components as dbc


def home_layout():
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "hidden"}, children=[
        html.H1("BidBits", style={"font-family": "Roboto", "text-align": "center", "font-size": "3rem", "font-weight": "bold", "margin-top": "3rem"}),

        dbc.Row([
            dbc.Col([
                html.H2("Registration", style={"font-family": "Roboto", "text-align": "left", "padding-left": "20%"}),

                html.Label("Username", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-username", type="text", style={"width": "60%", "margin-left": "20%"}),

                html.Label("Email", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-email", type="email", style={"width": "60%", "margin-left": "20%"}),

                html.Label("First Name", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-firstname", type="text", style={"width": "60%", "margin-left": "20%"}),

                html.Label("Last Name", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-lastname", type="text", style={"width": "60%", "margin-left": "20%"}),

                html.Label("Address", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-address", type="text", style={"width": "60%", "margin-left": "20%"}),

                html.Label("Phone Number", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-phone", type="text", style={"width": "60%", "margin-left": "20%"}),

                html.Label("Password", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-password", type="password", style={"width": "60%", "margin-left": "20%"}),

                html.Label("Confirm Password", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="register-confirm-password", type="password", style={"width": "60%", "margin-left": "20%"}),

                dbc.Button("Register", id="register-submit", color="primary", style={"font-family": "Roboto", "width": "60%", "margin-top": "1rem", "margin-left": "20%"})
            ], width=6),

            dbc.Col([
                html.H2("Login", style={"font-family": "Roboto", "text-align": "left", "padding-left": "20%"}),

                html.Label("Username", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="login-username", type="text", style={"width": "60%", "margin-left": "20%"}),

                html.Label("Password", style={"font-family": "Roboto", "padding-left": "20%"}),
                dbc.Input(id="login-password", type="password", style={"width": "60%", "margin-left": "20%"}),

                dbc.Button("Submit", id="login-submit", color="primary", style={"font-family": "Roboto", "width": "60%", "margin-top": "1rem", "margin-left": "20%"})
            ], width=6),
        ], style={"height": "100vh", "margin-top": "5%"}),

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