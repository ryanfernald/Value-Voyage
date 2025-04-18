import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_dir = os.path.join(BASE_DIR,'..','..', 'data', 'csv')


def build_income_distribution_pyramid():
    csv_path = os.path.join(csv_dir, 'quintile_historical.csv')
    df = pd.read_csv(csv_path)

    df = df.sort_values("Year", ascending=True)
    quintiles = [
        ("Lowest fifth", "blue"),
        ("Second fifth", "firebrick"),
        ("Middle fifth", "gold"),
        ("Fourth fifth", "forestgreen"),
        ("Highest fifth", "darkorange"),
        ("Top 5 percent", "lightblue")
    ]
    for quintile, _ in quintiles:
        df[quintile] = df[quintile].replace(',', '', regex=True).astype(float).astype(int).tolist()

    fig = go.Figure()

    for quintile, color in quintiles:
        fig.add_trace(go.Bar(
            y=df["Year"].astype(str),
            x=df[quintile],
            name=quintile,
            orientation='h',
            marker=dict(color=color)
        ))

    fig.update_layout(
        barmode='stack',
        title="Income Distribution by Population Group (Mean Income per Group)",
        xaxis_title="Mean Income for Each Group",
        yaxis_title="Year",
        template="plotly_white",
        height=900,
        margin=dict(l=80, r=20, t=60, b=60),
        legend=dict(title="Income Groups"),
        hovermode="x unified",
    )

    return fig