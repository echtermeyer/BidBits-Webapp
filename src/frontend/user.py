from dash import html
from dash import dcc
import dash_bootstrap_components as dbc


def user_layout(
        fn_get_user_information,
        fn_get_feedback_information,
        fn_get_payment_information,
        fn_get_won_auctions_information,
        stats
):
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.Div([
            dcc.Link(
                html.I(className="fas fa-arrow-left fa-2x"), href='/dashboard', style={"margin-left": "2rem", "color": "black"}
            )
        ], style={"position": "absolute", "display": "flex", "padding-top": "1rem", "align-items": "top", "height": "100%"}),

        html.H1("User Profile", style={"font-family": "Roboto", "text-align": "center", "font-size": "3rem",
                "font-weight": "bold", "margin-top": "3rem", "margin-bottom": "1rem", "color": "black"}),

        html.Div([
            dbc.Button("Personal Data", id="personal-data", className="mr-2", n_clicks=0, color="link", style={
                       "border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("Finished Auctions", id="won-auctions", className="mr-2", n_clicks=0, color="link", style={
                       "border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("Feedback", id="feedback", className="mr-2", n_clicks=0, color="link", style={
                       "border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
            dbc.Button("Payments", id="payments", className="mr-2", n_clicks=0, color="link", style={
                       "border": "none", "background": "none", "outline": "none", "box-shadow": "none", "color": "black"}),
        ], style={"text-align": "center", "margin-top": "3rem"}),

        html.Div(style={"height": "70vh", "overflow": "auto", "margin-top": "2rem"},
                 children=[
            html.Div(id="personal-data-content", children=personal_data_layout(
                        fn_get_user_information
            )),
            html.Div(id="won-auctions-content", children=won_auctions_layout(
                        fn_get_won_auctions_information,
                        stats
            ), style={'display': 'none'}),
            html.Div(id="feedback-content", children=feedback_layout(
                        fn_get_feedback_information,
                        stats
            ), style={'display': 'none'}),
            html.Div(id="payments-content", children=payments_layout(
                        fn_get_payment_information,
                        stats
            ), style={'display': 'none'})
        ]),
    ])


def personal_data_layout(fn_get_user_information):
    user = fn_get_user_information()[0]

    return html.Div(
        style={"margin-left": "10%", "margin-right": "10%"},
        children=[
            html.H2("Personal Data", style={
                    "font-family": "Roboto", "text-align": "center"}),

            html.Div(
                style={"width": "60%", "margin-left": "auto",
                       "margin-right": "auto"},
                children=[
                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Username", style={
                                               "font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-username",
                                type="text",
                                placeholder=user["username"],
                                disabled=True
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText(
                                "Email", style={"font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-email",
                                type="email",
                                placeholder=user["email"]
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("First Name", style={
                                               "font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-firstname",
                                type="text",
                                placeholder=user["firstname"]
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Last Name", style={
                                               "font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-lastname",
                                type="text",
                                placeholder=user["lastname"]
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Address", style={
                                               "font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-address",
                                type="text",
                                placeholder=user["address"]
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.InputGroup(
                        [
                            dbc.InputGroupText("Phone Number", style={
                                               "font-family": "Roboto", "width": "30%"}),
                            dbc.Input(
                                id="update-phone",
                                type="text",
                                placeholder=user["phone"]
                            )
                        ],
                        className="mb-3"
                    ),

                    dbc.Button(
                        "Update",
                        id="update-submit",
                        color="primary",
                        style={"font-family": "Roboto",
                               "width": "100%", "margin-top": "1rem"}
                    ),

                    dbc.Button(
                        "Delete User",
                        id={"type": "dynamic-button", "index": "delete-user-submit"},
                        href="/",
                        color="danger",
                        style={"font-family": "Roboto",
                               "width": "100%", "margin-top": "1rem"}
                    ),

                    html.Div(id='update-message',
                             style={"text-align": "center", "margin-top": "1rem"})
                ]
            )
        ]
    )


def won_auctions_layout(get_won_auctions_information, stats):
    elements = [
        html.H2("Finished Auctions", style={
                "font-family": "Roboto", "text-align": "center"}),
        html.H5(f"Won Auctions: {stats['won_auctions']}  |  Participated Auctions: {stats['participated_auctions']}",
                style={"font-family": "Roboto", "text-align": "center"})
    ]

    for i, auction in enumerate(get_won_auctions_information()):
        item = dbc.Card([
        dbc.Row([
            dbc.Col(dbc.CardImg(
                src=f"/assets/{auction['image_path']}", top=True), width=6),
            dbc.Col(dbc.CardBody([
                html.H4(auction['title'], className="card-title",
                        id={'type': 'title-text', 'index': i}),
                html.P(auction['description'], className="card-text"),
                html.H6(
                    f"Role: {auction['role'].capitalize()}", className="card-text"),
                html.H6(
                    f"Amount: ${auction['amount']:.2f}", className="card-text"),
                html.H6(
                    f"Item Code: #{auction['item_id']}", className="card-text", id={'type': 'item-id', 'index': i}),
                html.H6(
                    f"Rate your experience:", className="card-text"
                ),
                dcc.Slider(
                    id={'type': 'rating-slider', 'index': i},
                    min=1,
                    max=5,
                    marks={i: str(i) for i in range(1, 6)},
                    value=3,
                ),
                dbc.Input(
                    id={"type": "feedback-input", "index": i}, 
                    placeholder="Write your feedback here...",
                    style={"height": "4rem", "text-align": "top"},
                ),
                dbc.Button(
                    "Submit feedback",
                    id={"type": "submit-button", "index": i},
                    color="primary",
                    style={"font-family": "Roboto", "width": "100%", "margin-top": "1rem"}
                ),
                html.Div(id={"type": "feedback-success", "index": i})
            ], className="d-flex flex-column"), width=6)
        ])], style={"width": "50%", "margin": "1rem auto"})
        elements.append(item)

    return html.Div(
        style={"margin-left": "10%", "margin-right": "10%"},
        children=elements
    )


def feedback_layout(fn_get_feedback_information, stats):
    elements = [
        html.H2("Buyer Feedback", style={
                "font-family": "Roboto", "text-align": "center"}),
        html.H5(f"User Rating: {stats['average_rating']:.1f}/5.0 stars",
                style={"font-family": "Roboto", "text-align": "center"})
    ]

    for i, review in enumerate(fn_get_feedback_information()):
        print(review)
        item = dbc.Card([
            dbc.Row([
                dbc.Col(dbc.CardBody([
                    html.H4(f"Feedback from {review['sender']}", className="card-title", id={
                            'type': 'title-text', 'index': i}),
                    html.P(review['comment'], className="card-text"),
                    html.H6(
                        f"Rating: {review['rating']}/5 stars", className="card-text"),
                    # TODO: Add again
                    # html.H6(f"Date: {review['date']}", className="card-text"),
                ], className="d-flex flex-column"), width=6)
            ])
        ], style={"width": "50%", "margin": "1rem auto"})
        elements.append(item)

    return html.Div(
        style={"margin-left": "10%", "margin-right": "10%"},
        children=elements
    )


def payments_layout(fn_get_payment_information, stats):
    elements = [
        html.H2("Payment History", style={
                "font-family": "Roboto", "text-align": "center"}),
        html.H5(f"Total income: ${stats['total_income']:.2f}", style={
                "font-family": "Roboto", "text-align": "center"}),
        html.H5(f"Total paid: ${stats['total_expenses']:.2f}", style={
                "font-family": "Roboto", "text-align": "center"})
    ]

    for i, payment in enumerate(fn_get_payment_information()):
        print(payment)
        item = dbc.Card([
            dbc.Row([
                dbc.Col(dbc.CardBody([
                    # TODO: Add again
                    # html.H4(f"Payment for: {payment['title']}", className="card-title", id={'type': 'title-text', 'index': i}),
                    # html.P(
                    #     f"Item Code: #{payment['item_id']}", className="card-text"),
                    html.P(
                        f"Payment Method: {payment['type']}", className="card-text"),
                    html.P(
                        f"Payment Date: {payment['date']}", className="card-text"),
                    html.H6(
                        f"Paid amount: ${payment['amount']:.2f}", className="card-text"),
                ], className="d-flex flex-column"), width=6)
            ])
        ], style={"width": "50%", "margin": "1rem auto"})
        elements.append(item)

    return html.Div(
        style={"margin-left": "10%", "margin-right": "10%"},
        children=elements
    )
