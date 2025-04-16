from plotly.graph_objects import Figure, Scatter
from src.functions.db.fetch import fetch_incomes
from plotly.io import to_html


def compare_income_data_sources(db_path, start_year, end_year, regions, sources, markers, output_format, output_file=None, y_scale='log'):
    fig = Figure()

    for source, marker in zip(sources, markers):
        df = fetch_incomes(
            db_path=db_path,
            year_range=(start_year, end_year),
            data_source_name=source,
            regions=regions,
            output_format=output_format
        )
        if not df.empty:
            fig.add_trace(Scatter(
                x=df['year'],
                y=df['average_income_unadjusted'],
                mode='lines+markers',
                marker=dict(symbol=marker),
                name=source
            ))
        else:
            print(f"No data found for {source} between {start_year} and {end_year}.")

    fig.update_layout(
        title="United States Incomes",
        xaxis_title="Year",
        yaxis_title="Average Income Unadjusted",
        yaxis_type=y_scale,
        legend_title="Data Source",
        hovermode="x unified"
    )

    if output_file:
        fig.write_image(output_file)

    return fig


if __name__ == "__main__":
    db_path = '../../../data/db/sqlite/database.sqlite'
    start_year = 1900
    end_year = 2024
    regions = ['united states']
    sources = ['IRS', 'BEA', 'FRED']
    markers = ['circle', 'x', 'cross']
    output_format = 'df'
    output_file = f"../../../doc/figures/compare_income_data_sources_{start_year}_{end_year}.png"
    y_scale = 'log'  # or 'linear'

    fig = compare_income_data_sources(
        db_path, start_year, end_year, regions, sources,
        markers, output_format, output_file, y_scale
    )
    fig.show()

    # Save figure as HTML file
    html_file = "incomes_plotly.html"
    fig_html = to_html(fig, full_html=True)

    with open(html_file, "w") as f:
        f.write(fig_html)

    print(f"HTML file saved as {html_file}")
