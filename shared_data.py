import data_downloader as dd
import pandas as pd

try:
    dd.download_nyt_data()
    us_totals_df = pd.read_csv("data/NYT/us-latest.csv")
    states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")
except Exception as e:
    print(e)


# Variables
pie_legend_font_config = dict(family="Courier", size=24)
pie_graph_margins = dict(t=10, b=10, l=10, r=10)
bar_legend_font_config = dict(family="Helvetica", size=18, color="Black")
bar_graph_margins = dict(r=10)