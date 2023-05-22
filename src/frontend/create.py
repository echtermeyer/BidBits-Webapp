from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

def create_bid_layout(fn_get_categories):
    return html.Div(style={"height": "100vh", "background": "linear-gradient(to right, yellow, orange)", "overflow": "auto"}, children=[
        html.Div([
            dcc.Link(
                html.I(className="fas fa-arrow-left fa-2x"), href='/dashboard', style={"marginLeft": "2rem", "color": "black"}
            )
        ], style={"position": "absolute", "display": "flex", "padding-top": "1rem", "align-items": "top", "height": "100%"}),

        html.H1("Create Item for Auction", style={"fontFamily": "Roboto", "textAlign": "center", "fontSize": "3rem", "fontWeight": "bold", "marginTop": "3rem", "marginBottom": "1rem", "color": "black"}),
        
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Title"),
                    dbc.Input(type="text", id="item-title", placeholder="Enter item title"),
                ]),
            ], style={'marginBottom': '1rem'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Description"),
                    dbc.Textarea(id="item-description", placeholder="Enter item description", style={'height': '120px'}),
                ]),
            ], style={'marginBottom': '1rem'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Category"),
                    dbc.Select(id="item-category", options=[{'label': category, 'value': category} for category in fn_get_categories()]),
                ]),
            ], style={'marginBottom': '1rem'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Start Price (€)"),
                    dbc.Input(type="number", id="item-start-price", placeholder="Enter start price"),
                ]),
            ], style={'marginBottom': '1rem'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Auction Duration (Days)"),
                    dbc.Input(type="number", id="item-auction-duration", placeholder="Enter auction duration in days"),
                ]),
            ], style={'marginBottom': '1rem'}),
            dbc.Row([
                dbc.Col([
                    dbc.Label("Item Image"),
                    dcc.Upload(
                        id="item-image", 
                        children=html.Div(['Drag and Drop or ', html.A('Select Files')]), 
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        multiple=False
                    ),
                    html.Div(id='uploaded-file-name')
                ]),
            ], style={'marginBottom': '1rem'}),
            dbc.Row([
                dbc.Col([
                    dbc.Button("Start Auction", id="start-auction", color="primary", style={'width': '100%',}),
                ])
            ]),
            dbc.Container(id="alert-container", style={"width": "100%", "textAlign": "center", "marginTop": "1rem"})
        ], style={"max-width": "500px", "margin": "1rem auto", "padding": "2rem", "background": "white", "border-radius": "15px"}),
    ])
