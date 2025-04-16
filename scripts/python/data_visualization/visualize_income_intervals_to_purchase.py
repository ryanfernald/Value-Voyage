from plotly.graph_objects import Figure, Scatter
from src.functions.db.fetch import fetch_income_intervals_to_purchase

def plot_income_intervals_to_purchase(
    db_path, year_range, goods_list, regions,
    income_data_source, salary_interval, output_format
):
    df = fetch_income_intervals_to_purchase(
        db_path=db_path,
        year_range=year_range,
        goods_list=goods_list,
        regions=regions,
        income_data_source=income_data_source,
        salary_interval=salary_interval,
        output_format=output_format
    )

    fig = Figure()

    if df['year'].nunique() == 1:
        # Single year: Bar chart using scatter
        labels = [f"{name} ({unit})" for name, unit in zip(df['name'], df['good_unit'])]
        fig.add_trace(Scatter(
            x=labels,
            y=df['income_intervals_to_purchase'].astype(float).tolist(),
            mode='markers',
            name='Income Intervals'
        ))
        fig.update_layout(
            title=f"Income Intervals Needed in {df['year'].iloc[0]}",
            xaxis_title="Good (Unit)",
            yaxis_title="Income Intervals to Purchase"
        )
    else:
        # Multiple years: Line chart
        for (good, unit), group in df.groupby(['name', 'good_unit']):
            fig.add_trace(Scatter(
                x=group['year'],
                y=group['income_intervals_to_purchase'],
                mode='lines+markers',
                name=f"{good} ({unit})"
            ))
        fig.update_layout(
            title=f"Income Intervals to Purchase Over Years ({income_data_source} Incomes)",
            xaxis_title="Year",
            yaxis_title="Income Intervals",
            legend_title="Goods",
            hovermode="x unified",
            showlegend=True
        )

    return fig


if __name__ == "__main__":
    fig = plot_income_intervals_to_purchase(
        db_path='../../../data/db/sqlite/database.sqlite',
        year_range=(1953, 2024),
        # goods_list=['house'],
        goods_list=['Private 4-Year Tuition', 'Public 4-Year Tuition'],
        regions=['united states'],
        income_data_source='FRED',
        salary_interval='monthly',
        output_format='df'
    )
    fig.show()
    fig.write_html("goods_prices.html")

