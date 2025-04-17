import warnings

from components import navbar

warnings.filterwarnings("ignore", category=UserWarning, module='pandas')

from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR, '..', 'data', 'csv')

############################################
############# Graph Call Backs #############
############################################

####### Gini Coefficient and Lorenz Curve #######
def fetch_gini_samples():
    csv_path = os.path.join(csv_dir, 'gamma_resampling.csv')
    return pd.read_csv(csv_path)

gini_df = fetch_gini_samples()
available_years = sorted(gini_df["Year"].unique())

@callback(
    Output("lorenz-curve-plot", "figure"),
    Input("year-slider", "value")
)
def update_lorenz_plot(selected_year):
    df = fetch_gini_samples()
    incomes = df[df["Year"] == selected_year]["Income Sample"].sort_values().values

    if len(incomes) == 0:
        return px.line(title="No data available for selected year.")

    cumulative_income = np.cumsum(incomes)
    cumulative_income = np.insert(cumulative_income, 0, 0)
    cumulative_income = cumulative_income / cumulative_income[-1]
    population_share = np.linspace(0, 1, len(cumulative_income))

    equality_x = [0, 1]
    equality_y = [0, 1]
    fill_x = list(population_share) + equality_x[::-1]
    fill_y = list(cumulative_income) + equality_y[::-1]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fill_x, y=fill_y, fill="toself", fillcolor="rgba(255, 0, 0, 0.2)",
                             line=dict(color="rgba(255,255,255,0)"), hoverinfo="skip", showlegend=False))
    fig.add_trace(go.Scatter(x=population_share.tolist(), y=cumulative_income.tolist(), mode="lines", name="Lorenz Curve",
                             line=dict(color="blue", width=2)))
    fig.add_trace(go.Scatter(x=equality_x, y=equality_y, mode="lines", name="Line of Equality",
                             line=dict(dash="dash", color="gray")))

    gini = 1 - 2 * np.trapz(cumulative_income, population_share)

    fig.update_layout(
        title=f"Lorenz Curve - {selected_year} — Gini Coefficient: {gini:.4f}",
        xaxis_title="Cumulative Population",
        yaxis_title="Cumulative Income",
        xaxis=dict(range=[0, 1]),
        yaxis=dict(range=[0, 1]),
        showlegend=True,
        hovermode="x",

    )

    return fig

######### Gini Coefficient Over Time #########
def fetch_gini_over_time():
    csv_path = os.path.join(csv_dir, 'gini_year.csv')
    return pd.read_csv(csv_path)

gini_trend_df = fetch_gini_over_time()

gini_trend_fig = go.Figure(
    data=go.Scatter(
        x=gini_trend_df["Year"].astype(str).tolist(),
        y=gini_trend_df["Gini Coefficient"].astype(float).tolist(),
        mode="lines+markers",
        line=dict(color="orange", width=2),
        marker=dict(size=4),
        name="Gini Coefficient"
    )
)

gini_trend_fig.update_layout(
    title="Gini Coefficient (inequality coefficient) Over Time",
    xaxis_title="Year",
    yaxis_title="Gini Coefficient",
    xaxis=dict(
        tickangle=50
    ),
    yaxis=dict(
        autorange=False,
        range=[
            gini_trend_df["Gini Coefficient"].min() - 0.02,
            gini_trend_df["Gini Coefficient"].max() + 0.02
        ]
    ),
    template="plotly_white",
    hovermode="x",
)

######## Income Inequality Metrics ########
def fetch_analysis_metrics():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    return pd.read_csv(csv_path)

def fetch_normalized_analysis_metrics():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    return pd.read_csv(csv_path)

analysis_df = fetch_analysis_metrics()
metrics_fig = go.Figure()
metrics_fig.add_trace(go.Scatter(x=analysis_df["Year"].astype(str).tolist(), y=analysis_df["Palma Ratio"].astype(float).tolist(), mode="lines", name="Palma Ratio"))
metrics_fig.add_trace(go.Scatter(x=analysis_df["Year"].astype(str).tolist(), y=analysis_df["Housing Affordability Delta"].astype(float).tolist(), mode="lines", name="Housing Affordability Delta"))
metrics_fig.add_trace(go.Scatter(x=analysis_df["Year"].astype(str).tolist(), y=analysis_df["Productivity Gap Delta"].astype(float).tolist(), mode="lines", name="Productivity Gap Delta"))
metrics_fig.update_layout(
    title="Income Inequality Metrics Over Time",
    xaxis_title="Year",
    yaxis_title="Value",
    yaxis=dict(range=[0, 6]),
    template="plotly_white",
    hovermode="x"
)

normalized_df = fetch_normalized_analysis_metrics()
norm_fig = go.Figure()
norm_fig.add_trace(go.Scatter(x=normalized_df["Year"].astype(str).tolist(), y=normalized_df["Normalized Palma Ratio"].astype(float).tolist(), mode="lines", name="Normalized Palma Ratio"))
norm_fig.add_trace(go.Scatter(x=normalized_df["Year"].astype(str).tolist(), y=normalized_df["Normalized Housing Affordability Delta"].astype(float).tolist(), mode="lines", name="Normalized Housing Affordability Delta"))
norm_fig.add_trace(go.Scatter(x=normalized_df["Year"].astype(str).tolist(), y=normalized_df["Normalized Productivity Gap Delta"].astype(float).tolist(), mode="lines", name="Normalized Productivity Gap Delta"))
norm_fig.update_layout(
    title="Normalized Income Inequality Metrics",
    xaxis_title="Year",
    yaxis_title="Normalized Value",
    yaxis=dict(range=[0, 1]),
    template="plotly_white",
    showlegend=False,
    hovermode="x"
)

######### Alpha and Beta Parameters #########
def fetch_alpha_beta_trend():
    csv_path = os.path.join(csv_dir, 'analysis.csv')
    return pd.read_csv(csv_path)

alpha_beta_df = fetch_alpha_beta_trend()

alpha_beta_fig = go.Figure()
alpha_beta_fig.add_trace(go.Scatter(
    x=alpha_beta_df["Year"].astype(str).tolist(),
    y=alpha_beta_df["Alpha"].astype(float).tolist(),
    mode="lines",
    name="Alpha",
    line=dict(color="blue")
))
alpha_beta_fig.add_trace(go.Scatter(
    x=alpha_beta_df["Year"].astype(str).tolist(),
    y=alpha_beta_df["Beta"].astype(float).tolist(),
    mode="lines",
    name="Beta",
    line=dict(color="red")
))

alpha_beta_fig.update_layout(
    title="Gamma Distribution Parameters Over Time",
    xaxis_title="Year",
    yaxis_title="Parameter Value",
    yaxis=dict(range=[0, 9]),
    template="plotly_white",
    hovermode="x"
)


############################################
################# Layout ###################
############################################


layout = dbc.Container(fluid=True, children=[
    navbar.create_navbar(),

    # Section: Header / Introduction
    dbc.Row([
        dbc.Col(html.H2("Understanding Income Inequality Through Statistical Modeling"), width=12),
        dbc.Col(html.P("""
            This page summarizes the methodology and metrics used to quantify income inequality over time.
            Using the Palma Ratio, Housing Affordability Delta, and the Productivity Gap, we normalized each metric and derived Alpha and Beta parameters
            to simulate income distributions via a Gamma distribution. Gini coefficients and Lorenz curves offer visual and numeric validation of inequality over time.
        """), width=12)
    ], className="my-4"),
    
    # Section: Lorenz Curve Interactive Plot
    dbc.Row([
        dbc.Col([
            html.H4("Lorenz Curve by Year"),
            dcc.Slider(
                id="year-slider",
                min=min(available_years),
                max=max(available_years),
                value=min(available_years),
                step=1,  # or None if your years are not continuous integers
                marks={
                    int(year): {
                        "label": str(year),
                        "style": {
                            "transform": "rotate(45deg)",
                            "font-size": "10px"
                        }
                    }
                    for year in available_years if int(year) % 5 == 0
                },
                tooltip={"placement": "bottom", "always_visible": True}
            ),
            dcc.Graph(id="lorenz-curve-plot")
        ])
    ]),

    # Section: Gini Coefficients Text + Visual Pair
    dbc.Row([
    dbc.Col([
        html.H3("Interpreting Gini Coefficients"),
        html.P("""
            The Gini coefficient summarizes income inequality on a scale from 0 (perfect equality) to 1 (maximum inequality).
            It is derived from the Lorenz Curve and provides a snapshot of income concentration across a population.
            Here we analyze Gini trends using bootstrapped income samples across time.
        """),
        dcc.Markdown("""
        ### PDF (Probability Density Function) of the Gamma Distribution

        The probability density function (PDF) of the Gamma distribution is defined as:

        $$
        f(x; \\alpha, \\beta) = \\frac{1}{\\Gamma(\\alpha) \\beta^\\alpha} x^{\\alpha - 1} e^{-x / \\beta}
        $$

        Where:
        - $$\\alpha$$ is the shape parameter  
        - $$\\beta$$ is the scale parameter  
        - $$\\Gamma(\\alpha)$$ is the Gamma function
        """, mathjax=True)
    ], width=6),

    dbc.Col([
        dcc.Graph(id="gini-trend-plot", figure=gini_trend_fig)
    ], width=6)
], className="mb-4"),

    # Section: Expressing Income Inequality
    dbc.Row([
    dbc.Col([
        html.H3("Expressing Income Inequality"),
        html.H5("Income Inequality Metrics"),
        html.P("""
            To help understand the purchasing power of the dollar we wanted to better understand what it means for income inequality to be expressed in a few specific metrics. 
            To model and quantify income inequality in a dynamic and interpretable way, we developed a composite framework that utilizes three parameters: 
            The Palma Ratio, along with two delta values related to Housing Affordability and Productivity. The overall goal is to express these metrics as the hyperparameters in a Gamma distribution.
        """),
        html.H5("Here's a brief summary and explanation as to why we used these parameters:"),
        html.P("✤ Palma Ratio: This is a widely accepted measure of income inequality, defined as the ratio of the income share of the top 10% to that of the bottom 40%. It is a direct expression of income concentration and wealth disparity."),
        html.P("✤ Housing Affordability Delta: This metric measures the gap between what median-income individuals can afford and the actual cost of home ownership, including mortgage payments, insurance, and property taxes. This represents how economic inequality manifests in housing access and financial pressure, particularly for middle and lower-income earners."),
        html.P("✤ Productivity-Pay Gap: This captures the divergence between labor productivity and real wage growth. It reflects structural trends in wage stagnation, capital-labor imbalance, and broader systemic inequality that may not appear immediately in direct income ratios."),
        html.P("""
            A small note about the Pay Gap Delta: The data we have only goes back to 1948, so we set pay and performance equivalent for years before 1948. 
            This ensures their values represent equal pay for equal productivity and do not skew our Alpha or Beta values. 
            We thought it was an important metric to include as it represents overall economic inequality in the US.
        """)
    ], width=12)
], className="mb-4"),

    # Section: Income Indquality Metrics Graphs
    dbc.Row([
    dbc.Col([
        dcc.Graph(id="income_inequality_metrics", figure=metrics_fig)
    ], width=6),
    dbc.Col([
        dcc.Graph(id="normalized_income_inequality_metrics", figure=norm_fig)
    ], width=6)
], className="mb-4"),

    # Section: Alpha and Beta Parameter Visualization
    dbc.Row([
        dbc.Col([
            html.H3("Gamma Distribution Parameters, Alpha and Beta"),
            html.P("An income distribution is always skewed like a Gamma Distribution — this has been consistent throughout history. We wanted to find out just how skewed and how spread the data should be using a bootstrap resampling method. As a result, we chose our Gamma parameters: Alpha and Beta, each designated with special weights according to their relevance."),

            html.H4("Alpha (Shape Parameter)"),
            html.H5("Represents inequality skew. Lower alpha values create more right-skewed distributions (i.e., higher inequality), while higher values create more symmetric distributions (i.e., more equitable)."),
            html.P("We weighted the inputs for Alpha as follows:"),
            html.P("✤ Palma Ratio: 50% — it directly measures inequality concentration"),
            html.P("✤ Housing Delta: 30% — reflects local volatility and financial pressure"),
            html.P("✤ Productivity Gap: 20% — reflects slow-moving but systemic divergence"),

            html.H4("Beta (Scale Parameter)"),
            html.H5("Represents the breadth or variance of the distribution. It reflects how spread out the income distribution is, with higher values indicating greater dispersion."),
            html.P("We weighted the inputs for Beta as follows:"),
            html.P("✤ Productivity Gap: 50% — systemic wage divergence creates long-term spread"),
            html.P("✤ Housing Delta: 30% — affordability shocks influence volatility"),
            html.P("✤ Palma Ratio: 20% — still relevant, but more focused on distribution extremes"),
        ], width=6),
        dbc.Col([
            dcc.Graph(id="beta-trend-plot", figure=alpha_beta_fig)
        ], width=6)
    ], className="mb-5"),
])

exprort_layout = layout