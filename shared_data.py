import data_downloader as dd
import pandas as pd

try:
    dd.download_nyt_data()
    us_totals_df = pd.read_csv("data/NYT/us-latest.csv")
    states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")
except Exception as e:
    print(e)


# Variables
pie_graph_margins = dict(t=10, b=10, l=10, r=10)
pie_legend_font_config = dict(size=24)
bar_legend_font_config = dict(family="Helvetica", size=24)
bar_graph_margins = dict(r=10)
line_legend_font_config = dict(size=24)

if __name__ == "__main__":
    pass
