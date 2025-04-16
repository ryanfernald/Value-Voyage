import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

from dash import Dash, dcc, html, Input, Output, callback, dash
import dash_bootstrap_components as dbc
from components import navbar
from pages import landing, objectives, analysis, findings, stats_analysis
# from flask import Flask, request
import os


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
server = app.server

# Define the app layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar.create_navbar(),
    html.Div(id="page-content", style={"padding": "20px"}),
    dash.page_container

])

# Define the callback to update the page content
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
    else:
        return html.Div([
            html.H1("404: Page Not Found"),
            html.P("The page you are looking for does not exist.")
        ])

# Define a readiness check endpoint
@app.server.route('/readiness_check')
def readiness_check():
    if app.is_ready():
        return "App is ready", 200
    else:
        return "App is not ready", 503
    
@app.server.route("/debug-db")
def debug_db():
    test_path = os.path.join(os.path.dirname(__file__), 'data', 'db', 'sqlite', 'database.sqlite')
    try:
        exists = os.path.exists(test_path)
        return f"File exists: {exists}, Path: {test_path}"
    except Exception as e:
        return str(e), 500
    

@app.server.route("/list-db-dir")
def list_db_dir():
    try:
        base_dir = os.path.dirname(__file__)
        full_path = os.path.join(base_dir, 'data', 'db', 'sqlite')
        files = os.listdir(full_path)
        return "<br>".join(files)
    except Exception as e:
        return f"Failed to read directory: {str(e)}"

if __name__ == "__main__":
    app.run_server(debug=True, port=8080 if os.environ.get('SERVER_SOFTWARE') else 8050)
    warnings.filterwarnings("ignore", category=UserWarning, module='pandas')