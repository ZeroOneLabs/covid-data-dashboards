import pandas as pd

states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")

print(states_totals_df.loc[states_totals_df["state"] == "Alabama"]["deaths"].values[0])