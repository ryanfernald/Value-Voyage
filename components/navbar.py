import dash_bootstrap_components as dbc
from dash import dcc, html

def create_navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Objectives", href="/objectives")),
            dbc.NavItem(dbc.NavLink("Exploratory Data Analysis", href="/analysis")),
            dbc.NavItem(dbc.NavLink("Findings", href="/findings")),
            dbc.NavItem(dbc.NavLink("Statistical Analysis", href="/stat_analysis")),
            dbc.DropdownMenu(
                children = [
                    dbc.DropdownMenuItem("Housing Visualization", href="/housing_visualization"),
                    dbc.DropdownMenuItem("Pay - Productivity Gap", href="/pay_productivity_gap"),
                    dbc.DropdownMenuItem("Gini Testing with Variation", href="/gini_testing"),
                    dbc.DropdownMenuItem("Data", href="/data")
                    ],
                    nav=True,
                    in_navbar=True,
                    label="More",
                    align_end=True,
                    direction="left"
            ),
        ],
        brand="Value Voyage - A Journey Through Decades of Prices",
        brand_href="/",
        color="darkcyan",
        dark=True,
        fluid=True,
    )
    return navbar
