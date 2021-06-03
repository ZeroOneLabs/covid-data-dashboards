import pandas as pd
import json
import sys

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px


## Resources
#
## CDC definitions on mortality rates: 
#+ https://wwwn.cdc.gov/eworld/Appendix/Mortality
#
#



## Initialize Dash app
# app = dash.Dash(__name__, assets_folder='assets')
# server = app.server

with open("data/state_info.json") as jfile:
    us_state_dict = json.load(jfile)

print(us_state_dict)
sys.exit()

## TODO - include total population into above dict? Have it as item zero?
total_us_population = 331814684
us_stats_dict = {
    'population': 331814684, 'short_name': "US", 'long': 'United States of America', 'file': 'national-history.csv'
}
data_path = "data/covidtracking.com/"
us_csv = pd.read_csv(data_path + us_stats_dict['file'])


# print(us_csv.columns)


us_deaths = us_csv['death'][0]
us_cases = us_csv['positive'][0]
# print(us_cases)
us_covid_mortality_rate = round((us_deaths / us_cases) * 100, 3) # ~1.791
print(f"US COVID mortality rate: {us_covid_mortality_rate}")

states_dict = {}
for code, state in us_state_dict.items():
    state_data = pd.read_csv(data_path + state['file'])
    state_longname = state['long_name']
    state_deaths = state_data['death'][0]
    state_cases = state_data['positive'][0]
    state_mortality_rate = round((state_deaths / state_cases) * 100,3)
    states_dict[code]['mortality_rate'] = state_mortality_rate

states_pd = pd.DataFrame(states_dict)
print(states_pd)




# states_pd.to_excel('/Users/zan/Desktop/COVID-mortality-rates-per-state.xlsx', index=False)