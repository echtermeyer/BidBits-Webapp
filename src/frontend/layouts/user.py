import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

from backend.dashboard import generate_add_bids, generate_wishlist


def user_layout():
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.Div([
            dcc.Link(
                html.I(className="fas fa-arrow-left fa-2x"), href='/dashboard', style={"margin-left": "2rem", "color": "black"}
            )
        ], style={"position": "absolute", "display": "flex", "padding-top": "1rem", "align-items": "top", "height": "100%"}),

        html.H1("User Profile", style={"font-family": "Roboto", "text-align": "center", "font-size": "3rem", "font-weight": "bold", "margin-top": "3rem", "margin-bottom": "1rem", "color": "black"}),
        
        html.Div([
            dbc.Button("Personal Data", id="personal-data", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("Won Auctions", id="won-auctions", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("Feedback", id="feedback", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("Payments", id="payments", className="mr-2", n_clicks=0, color="link", style={"border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
        ], style={"text-align": "center", "margin-top": "3rem"}),

        html.Div(style={"height": "70vh", "overflow": "auto", "margin-top": "2rem"},
                 children=[
                    html.Div(id="personal-data-content", children=personal_data_layout()),
                    html.Div(id="won-auctions-content", style={'display': 'none'}),
                    html.Div(id="feedback-content", style={'display': 'none'}),
                    html.Div(id="payments-content", style={'display': 'none'})
                 ]),
    ])


def personal_data_layout():
    return html.Div(
        style={"margin-left": "10%", "margin-right": "10%"},
        children=[
            html.H2("Personal Data", style={"font-family": "Roboto", "text-align": "center"}),

            html.Div(
                style={"width": "60%", "margin-left": "auto", "margin-right": "auto"},
                children=[
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Username", style={"font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-username",
                                type="text",
                                placeholder="TerminatorTobi",
                                disabled=True
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Email", style={"font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-email",
                                type="email",
                                placeholder="elaspix-sucks@hotmail.de"
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("First Name", style={"font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-firstname",
                                type="text",
                                placeholder="Tobias"
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Last Name", style={"font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-lastname",
                                type="text",
                                placeholder="Günther"
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Address", style={"font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-address",
                                type="text",
                                placeholder="Meerfeldstraße 63, 68163 Mannheim"
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Phone Number", style={"font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-phone",
                                type="text",
                                placeholder="015168414878"
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.Button(
                        "Update",
                        id="update-submit",
                        color="primary",
                        style={"font-family": "Roboto", "width": "100%", "margin-top": "1rem"}
                    )
                ]
            )
        ]
    )
