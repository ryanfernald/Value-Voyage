import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

from dash import Dash, dcc, html, Input, Output, callback, dash
import dash_bootstrap_components as dbc
from components import navbar
from pages import landing, objectives, analysis, findings, stats_analysis
import os

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# # # Define the app layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content", style={'width': '100%'}),
])

@callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)

def display_page(pathname):
    if pathname == "/":
        return landing.layout
    elif pathname == "/objectives":
        return objectives.layout
    elif pathname == "/analysis":
        return analysis.layout
    elif pathname == "/findings":
        return findings.layout
    elif pathname == "/stat_analysis":
        return stats_analysis.layout
    elif pathname == "/housing_visualization":
        return html.Div()
    else:
        return html.Div([
            html.H1("404: Page Not Found"),
            html.P("The page you are looking for does not exist.")
        ])

# Callback to toggle the navigation menu visibility
@app.callback(
    [Output("topNav", "className"),
     Output("topBar", "className"),
     Output("menuToggle", "className")],
    [Input("menuToggle", "n_clicks")],
    prevent_initial_call=True
)
def toggle_menu(n_clicks):
    if n_clicks % 2 == 1:
        return "top-nav open", "top-bar with-background", "menu-toggle active"
    else:
        return "top-nav", "top-bar", "menu-toggle"

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
