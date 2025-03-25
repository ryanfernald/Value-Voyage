import pandas as pd
import sqlite3
import json
from src.functions.db.fetch import fetch_goods_prices
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.colors as mcolors

def calculate_goods_inflation(
    db_path,
    year_range=(1990, 2000),
    goods_list=None,
    use_year_averages=True,
    output_format='df'
):
    prices_df = fetch_goods_prices(
        db_path=db_path,
        year_range=year_range,
        goods_list=goods_list,
        use_year_averages=use_year_averages,
        output_format='df'
    )

    # Ensure correct types and sorting
    prices_df = prices_df.sort_values(['name', 'year'])

    # Calculate inflation per good
    prices_df['inflation'] = prices_df.groupby('name')['price'].transform(lambda x: (x / x.shift(1) - 1) * 100)

    # Drop rows where inflation couldn't be calculated (first year per good)
    prices_df = prices_df.dropna(subset=['inflation'])

    # Keep relevant columns
    result_df = prices_df[['name', 'year', 'price', 'inflation', 'good_unit', 'date', 'data_source']]

    if output_format == 'df':
        return result_df.reset_index(drop=True)
    else:
        return result_df.to_json(orient='records', date_format='iso')


def create_inflation_matrix(df):
    """
    Pivot inflation data to create a matrix of goods (columns) vs. years (rows).
    """
    matrix = df.pivot(index='year', columns='name', values='inflation')
    return matrix


def plot_inflation_heatmap(matrix, output_file):
    matrix = matrix.replace([float('inf'), float('-inf')], pd.NA).dropna(how='all', axis=0).dropna(how='all', axis=1)

    plt.figure(figsize=(40, 15))

    # Define new bounds and colors
    bounds = [-100, -5, -2, 0, 2, 5, 100]
    colors = ['darkgreen', 'mediumseagreen', 'lightgreen', 'mistyrose', 'salmon', 'darkred']
    cmap = mcolors.ListedColormap(colors)
    norm = mcolors.BoundaryNorm(bounds, cmap.N)

    sns.heatmap(
        matrix.T,
        cmap=cmap,
        norm=norm,
        linewidths=0.5,
        linecolor="gray",
        annot=True,
        fmt="1.1f",
        annot_kws={"size": 6},
        cbar_kws={
            'ticks': bounds,
            'label': 'Inflation % (YoY)'
        },
        square=True
    )

    plt.xlabel("Year")
    plt.ylabel("Good Name")
    plt.title("Year-over-Year Goods Inflation Heatmap")
    plt.xticks(rotation=90, ha="center")
    plt.yticks(rotation=0)
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.show()
    print(f"Inflation heatmap saved as {output_file}")




if __name__ == "__main__":
    year_range = (1929, 2024)

    inflation_df = calculate_goods_inflation(
        db_path='../../../data/db/sqlite/database.sqlite',
        year_range=year_range,
        goods_list=None,
        use_year_averages=True,
        output_format='df'
    )

    inflation_df.to_csv("ahan.csv", index=False)

    output_file = f"../../../doc/diagrams/inflation_heatmap_{year_range[0]}_{year_range[1]}.png"

    matrix = create_inflation_matrix(inflation_df)
    plot_inflation_heatmap(matrix, output_file)
