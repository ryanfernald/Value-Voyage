from plotly.graph_objects import Figure, Scatter
from src.functions.db.fetch import fetch_goods_prices



def plot_goods_prices(db_path, year_range, goods_list, output_format):
    df = fetch_goods_prices(
        db_path=db_path,
        year_range=year_range,
        goods_list=goods_list,
        output_format=output_format
    )

    fig = Figure()

    if df['year'].nunique() == 1:
        # If only one year, create a bar chart
        labels = [f"{name} ({unit})" for name, unit in zip(df['name'], df['good_unit'])]
        fig.add_trace(Scatter(x=labels,
                              y=df['price'].astype(float).tolist(),
                              mode='markers',
                              name='Price'))
        fig.update_layout(
            title=f"Goods Prices in {df['year'].iloc[0]}",
            xaxis_title="Good (Unit)",
            yaxis_title="Price (USD)"
        )
    else:
        # If multiple years, create a line chart
        for (good, unit), group in df.groupby(['name', 'good_unit']):
            fig.add_trace(Scatter(x=group['year'], y=group['price'], mode='lines+markers', name=f"{good} ({unit})"))
        fig.update_layout(
            title=f"Goods Prices Over Years",
            xaxis_title="Year",
            yaxis_title="Price (USD)",
            legend_title="Goods",
            hovermode="x unified"
        )

    return fig


if __name__ == "__main__":
    # Specify the database path and parameters
    fig = plot_goods_prices(
        db_path='../../../data/db/sqlite/database.sqlite',
        year_range=(1900, 2020),
        goods_list=['bacon', 'bread', 'butter', 'coffee', 'eggs', 'flour', 'milk', 'pork chop', 'round steak', 'sugar',
                    'gas'],
        output_format='df'
    )

    # Save the figure to an HTML file
    fig.write_html("goods_prices.html")

    # Optionally, show the plot
    fig.show()
