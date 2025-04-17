from dash import html

layout = html.Div([
    # Link to CSS files in the static folder
    html.Link(rel='stylesheet', href='/static/css/global-styles.css'),
    html.Link(rel='stylesheet', href='/static/css/homepage-styles.css'),
    html.Link(rel='stylesheet', href='/static/css/top-bar-styles.css'),

    # Main container
    html.Div([
        # Slide 1 - Top Bar + Hero Section
        html.Div(className="section-slide", children=[
            # Top Bar with Hamburger and Nav
            html.Div(id="topBar", className="top-bar", children=[
                html.Div(id="menuToggle", className="menu-toggle", n_clicks=0, children=[
                    html.Div(), html.Div(), html.Div()
                ]),
                html.Div(id="topNav", className="top-nav", children=[
                    html.A('Objectives', href='/objectives'),
                    html.A('Methods', href='/stat_analysis'),
                    html.A('Major Findings', href='/findings'),
                    html.A('Data', href='/data')
                ])
            ]),

            # Hero Section
            html.Div(className="hero", children=[
                html.Div(className="overlay", children=[
                    html.Div(className="overlay-content", children=[
                        html.H1("Value Voyage"),
                        html.H2("A journey through decades of prices")
                    ]),
                    html.Div(className="overlay-footer", children=[
                        html.H3("by Max Dokukin and Ryan Fernald")
                    ])
                ]),
                html.Div(className="scroll-hint", children="↓")
            ])
        ]),

        # Slide 2 - Question Section
        html.Div(className="section-slide", children=[
            html.H2("We had one question"),
            html.H3("Does an average consumer today can afford to buy more than one in 1920s?")
        ]),

        # Slide 3 - Data Collection Section
        html.Div(className="section-slide", children=[
            html.H2("So we collected some data"),
            html.H3("1. The average price of goods from 1900 - 2020"),
            html.H3("2. The average incomes from 1900 - 2020")
        ])
    ], className="container-slide"),

    # Link to JavaScript file in the static folder
    html.Script(src='/static/js/scroll-activate.js')
])