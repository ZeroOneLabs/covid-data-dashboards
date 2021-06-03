#!/usr/bin/env python3
# Import some standard libraries to handle file checks, directory creation, custom exit messages, etc.
import os
import json
import sys
# pathlib for getting file creation statistics
import pathlib
from datetime import datetime
import urllib.request
#
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd


base_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(base_dir, "data/NYT")


## TODO:
# use sqlite3 and (from sqlalchemy import create_engine) to use SQL commands
# to be able to search through historical data quickly. 
# Reference: https://www.youtube.com/watch?v=71zkSuzkJrw "How to use SQL with Excel using Python"
## TODO - put this data in a separate file to reduce code complexity/density?
## TODO - if stored locally, add API to update the population?

us_state_dict = { 
    '0': {  'population': 4932000, 'short_name': "AL" , 'long_name': 'Alabama'},
    '1': {  'population': 728903, 'short_name': "AK" , 'long_name': 'Alaska'},
    '2': {  'population': 7278717, 'short_name': "AZ" , 'long_name': 'Arizona'},
    '3': {  'population': 3017825, 'short_name': "AR" , 'long_name': 'Arkansas'},
    '4': {  'population': 39512223, 'short_name': "CA" , 'long_name': 'California'},
    '5': {  'population': 5758736, 'short_name': "CO" , 'long_name': 'Colorado'},
    '6': {  'population': 3565287, 'short_name': "CT" , 'long_name': 'Connecticut'},
    '7': {  'population': 973764, 'short_name': "DE" , 'long_name': 'Delaware'},
    '8': {  'population': 705749, 'short_name': "DC" , 'long_name': 'District of Columbia'},
    '9': {  'population': 21477737, 'short_name': "FL" , 'long_name': 'Florida'},
    '10': {  'population': 10617423, 'short_name': "GA" , 'long_name': 'Georgia'},
    '12': {  'population': 1415872, 'short_name': "HI", 'long_name': 'Hawaii'},
    '13': {  'population': 1787065, 'short_name': "ID", 'long_name': 'Idaho'},
    '14': {  'population': 12671821, 'short_name': "IL", 'long_name': 'Illinois'},
    '15': {  'population': 6732219, 'short_name': "IN", 'long_name': 'Indiana'},
    '16': {  'population': 3155070, 'short_name': "IA", 'long_name': 'Iowa'},
    '17': {  'population': 2913314, 'short_name': "KS", 'long_name': 'Kansas'},
    '18': {  'population': 4467673, 'short_name': "KY", 'long_name': 'Kentucky'},
    '19': {  'population': 4648794, 'short_name': "LA", 'long_name': 'Louisiana'},
    '20': {  'population': 1344212, 'short_name': "ME", 'long_name': 'Maine'},
    '21': {  'population': 6045680, 'short_name': "MD", 'long_name': 'Maryland'},
    '22': {  'population': 6949503, 'short_name': "MA", 'long_name': 'Massachusetts'},
    '23': {  'population': 9986857, 'short_name': "MI", 'long_name': 'Michigan'},
    '24': {  'population': 5639632, 'short_name': "MN", 'long_name': 'Minnesota'},
    '25': {  'population': 2976149, 'short_name': "MS", 'long_name': 'Mississippi'},
    '26': {  'population': 6137428, 'short_name': "MO", 'long_name': 'Missouri'},
    '27': {  'population': 1068778, 'short_name': "MT", 'long_name': 'Montana'},
    '28': {  'population': 1934408, 'short_name': "NE", 'long_name': 'Nebraska'},
    '29': {  'population': 3080156, 'short_name': "NV", 'long_name': 'Nevada'},
    '30': {  'population': 1359711, 'short_name': "NH", 'long_name': 'New Hampshire'},
    '31': {  'population': 8882190, 'short_name': "NJ", 'long_name': 'New Jersey'},
    '32': {  'population': 2096829, 'short_name': "NM", 'long_name': 'New Mexico'},
    '33': {  'population': 19453561, 'short_name': "NY", 'long_name': 'New York'},
    '34': {  'population': 10488084, 'short_name': "NC", 'long_name': 'North Carolina'},
    '35': {  'population': 762062, 'short_name': "ND", 'long_name': 'North Dakota'},
    '36': {  'population': 55194, 'short_name': "NI", 'long_name': 'Northern Mariana Islands'},
    '37': {  'population': 11689100, 'short_name': "OH", 'long_name': 'Ohio'},
    '38': {  'population': 3956971, 'short_name': "OK", 'long_name': 'Oklahoma'},
    '39': {  'population': 4217737, 'short_name': "OR", 'long_name': 'Oregon'},
    '40': {  'population': 12801989, 'short_name': "PA", 'long_name': 'Pennsylvania'},
    '41': {  'population': 3193694, 'short_name': "PR", 'long_name': 'Puerto Rico'},
    '42': {  'population': 1059361, 'short_name': "RI", 'long_name': 'Rhode Island'},
    '43': {  'population': 5148714, 'short_name': "SC", 'long_name': 'South Carolina'},
    '44': {  'population': 884659, 'short_name': "SD", 'long_name': 'South Dakota'},
    '45': {  'population': 6833174, 'short_name': "TN", 'long_name': 'Tennessee'},
    '46': {  'population': 28995881, 'short_name': "TX", 'long_name': 'Texas'},
    '47': {  'population': 3205958, 'short_name': "UT", 'long_name': 'Utah'},
    '48': {  'population': 623989, 'short_name': "VT", 'long_name': 'Vermont'},
    '49': {  'population': 8535519, 'short_name': "VA", 'long_name': 'Virginia'},
    '50': {  'population': 104914, 'short_name': "VI", 'long_name': 'Virgin Islands'},
    '51': {  'population': 7614893, 'short_name': "WA", 'long_name': 'Washington'},
    '52': {  'population': 1792147, 'short_name': "WV", 'long_name': 'West Virginia'},
    '53': {  'population': 5822434, 'short_name': "WI", 'long_name': 'Wisconsin'},
    '54': {  'population': 578759, 'short_name': "WY", 'long_name': 'Wyoming'},
}
## TODO - include total population into above dict? Have it as item zero?
total_us_population = 331814684


## Create list of dicts, which contain each State's long name and short name
## This is to automatically populate the dropdown lists without needing to reuse 
## these definitions. I must've spent 2 hours looking up how to structure this. /facepalm
state_dropdown_list = []
for k, v in us_state_dict.items():
    # Exclude DC, Northern Islands, Puerto Rico, and Virgin Islands
    # because I don't have polygon data for these territories
    # and they aren't shown on my choropleth graph.
    # TODO - Update choropleth graph to show these territories?
    if v['short_name'] in [ "DC", "NI", "PR", "VI"]:
        continue
    # Will be picking data from the 'state' colum by long_name, not short_name. Oops.
    # state_dropdown_list.append({'label': v['long_name'], 'value': v['short_name']})
    state_dropdown_list.append({'label': v['long_name'], 'value': v['long_name']})


## Initialize Dash app
app = dash.Dash(__name__, assets_folder='assets')
server = app.server

# Create data frames

## DATAFRAME - US Nationwise    - Latest
# And add new column with the US total population
df_us_latest = pd.read_csv(os.path.join(data_dir, data_file_dict['us-nationwide']['local_name_latest']))
df_us_latest.insert(3, "total_population", [total_us_population], True)
# DATAFRAME - US States         - Latest
df_us_states_latest = pd.read_csv(os.path.join(data_dir, data_file_dict['us-states']['local_name_latest']))
# DATAFRAME - US Counties       - Latest
df_us_counties_latest = pd.read_csv(os.path.join(data_dir, data_file_dict['us-counties']['local_name_latest']))

## DATAFRAME - US Nationwide    - Historical
df_us_historical = pd.read_csv(os.path.join(data_dir, data_file_dict['us-nationwide']['local_name_historical']))

## DATAFRAME - US States        - Historical
df_us_states_historical = pd.read_csv(os.path.join(data_dir, data_file_dict['us-states']['local_name_historical']))
## DATAFRAME - US Counties      - Historical
df_us_counties_historical = pd.read_csv(os.path.join(data_dir, data_file_dict['us-counties']['local_name_historical']))


# Store latest cases and deaths into variables.
us_latest_cases = df_us_latest['cases'].iloc[0]
us_latest_deaths = df_us_latest['deaths'].iloc[0]

## Calculate rates
# US mortality vs cases
us_mortality_rate_cases = round((int(us_latest_deaths) * 100) / int(us_latest_cases), 3)
# US survival rate
us_survival_rate_cases = float(100 - us_mortality_rate_cases)
# US mortality rate
us_mortality_rate_pop = round((int(us_latest_deaths) * 100) / int(total_us_population), 3)
# US cases vs rates
us_cases_rate_pop = round((int(us_latest_cases) * 100) / int(total_us_population), 3)




us_states_deaths_figure = px.bar(df_us_states_latest, x="state", y="deaths")
us_states_deaths_figure.update_layout(barmode='stack', xaxis={'categoryorder':'total ascending'})

# Create dataframe of counties
df_us_counties_latest = pd.read_csv(os.path.join(data_dir, data_file_dict['us-counties']['local_name_latest']), dtype={"fips": str})

# Setting up list to combine NYC's stats with Nassau, New York (due to New York Times' not separating FIPS areas within NYC)
collection_columns = ['fips', 'cases', 'deaths', 'confirmed_cases', 'confirmed_deaths', 'probable_cases', 'probable_deaths']

# TODO: Delete this comment block later. Used for testing.
# query = df_us_counties_latest.loc[(df_us_counties_latest['county'] == "Nassau") & (df_us_counties_latest['state'] == "New York")]
# print(f"Nassau: {query}")
# query = df_us_counties_latest.loc[df_us_counties_latest['county'] == "New York City"]
# print(f"NYC (before): {query}")


# Set New York City to share the same column values (sum) as "Nassau, New York"
# Note: This is only for the latest county data set, as the NYT github data doesn't list a FIPS code for NYC.
for column in collection_columns:
    # Get initial data. Tell Pandas to fill NaN values with an integer zero.
    nassau_tmp = df_us_counties_latest.loc[(df_us_counties_latest['county'] == "Nassau") & (df_us_counties_latest['state'] == "New York"), [column]].fillna(0)
    nyc_tmp = df_us_counties_latest.loc[df_us_counties_latest['county'] == "New York City", [column]].fillna(0)

    # Get the value of the colum, use the to_string function to return the value without the index number.
    # Use the float() and int() functions to step the values down to basic integers.
    nassau_tmp = int(float(nassau_tmp[column].to_string(index=False)))
    nyc_tmp = int(float(nyc_tmp[column].to_string(index=False)))
    
    # Add Nassau's values to NYC
    df_us_counties_latest.loc[df_us_counties_latest['county'] == "New York City", [column]] = nassau_tmp + nyc_tmp

    # Delete Nassau's values so the choropleth map is reflected accurately (we don't want to have an overlap of values, especially 
    # after adding Nassau's values to NYC)
    df_us_counties_latest.loc[(df_us_counties_latest['county'] == "Nassau") & (df_us_counties_latest['state'] == "New York"), [column]] = 0


## GRAPH - Pie chart of nation-wide cases vs deaths
data_dict = [
    { 'name': 'cases', 'value': us_latest_cases },
    { 'name': 'population', 'value': total_us_population },
    { 'name': 'deaths', 'value': us_latest_deaths },
]
df = pd.DataFrame(data_dict)
fig_pie_case_death_pop = px.pie(df, values="value", names="name")


## US Counties - Choropleth by deaths
us_counties_deaths_figure = px.choropleth(
    df_us_counties_latest, 
    geojson=counties, 
    locations='fips',          
    color='deaths',
    color_continuous_scale="Turbo",
    range_color=(0, 20000),
    scope="usa",
    labels={'deaths':'Total COVID deaths', 'county': 'County', 'cases': 'Cases'},
    hover_name="county",
    hover_data=["deaths", "cases", "state", "county"]
    )
us_counties_deaths_figure.update_layout(height=700, margin={"r":0,"t":0,"l":0,"b":0})


#
## Build main view ("app") layout
app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='COVID Dashboard'),
        html.H2(children="Visualize latest and historical US COVID data."),
    ], id="header", style={'border-bottom': 'thin solid black', 'margin-bottom': '30px'}),

    html.H3(children="Nation-wide statistics"),

    dcc.Markdown(f'''
        * Deaths vs cases: {us_mortality_rate_cases}%.
        * Deaths vs population: {us_mortality_rate_pop}%.
        * Cases vs population: {us_cases_rate_pop}%.
    '''),

    dcc.Graph(figure=fig_pie_case_death_pop,
        id="fig-pie-cases-deaths-population",
        className="figure pie",
    ),

    html.Hr(children=None, className="hr-separator"),

    html.H3(children="COVID Deaths per State (ascending)"),
    html.Div(children="Note: Population is using the latest estimation from census data.", style={'font-style':'italic'}),
    dcc.Graph(
        id='deaths-per-state',
        className="figure bar",
        figure=us_states_deaths_figure
    ),

    html.Hr(children=None, className="hr-separator"),

    html.H3(children="Heat map of US Counties"),
    html.Div(children="Note: New York City had to be combined with Nassau, New York, because the New York Times does not list a county code for New York City."),
    dcc.Graph(
        id='deaths-per-county',
        className="figure map",
        figure=us_counties_deaths_figure
    ),

    html.Hr(children=None, className="hr-separator"),

    html.H3(children="Compare COVID death/case rates (State vs State)"),
    html.Div(children="Note: Territories such as DC, Puerto Rico, Virgin Islands, and Northern Islands are not included."),

    html.Div(children=[
        html.Div(children=[
            html.Span(children="State 1: ", className="state-vlabel"),
            dcc.Dropdown(
                id="state-dropdown-1",
                options=state_dropdown_list,
                className="state-dropdown",
                value="New York"
            )
        ], className="label-dropdown-container"),
        html.Div(children=[
            html.Span(children="State 2: ", className="state-vlabel"),
            dcc.Dropdown( 
                id="state-dropdown-2",
                options=state_dropdown_list,
                className="state-dropdown",
                value="California"
            )
        ], className="label-dropdown-container"),
        html.Div(children=[
            html.Span(children="Data type: ", className="state-vlabel"),
            dcc.Dropdown( 
                id="state-dropdown-3",
                options=[
                    {'label': 'deaths', 'value': 'deaths'},
                    {'label': 'cases', 'value': 'cases'}
                    ],
                className="state-dropdown",
                value="deaths"
            )
        ], className="label-dropdown-container"),
    ], className="dropdown-container"),

    dcc.Graph(
        id='state-comparison',
        className="figure line"
    ),

    html.Div(className="footer", children=[

    dcc.Markdown(f'''
        All data was pulled from public data, via Github.com. This dashboard was created by [Zero One Labs](https://zeroonelabs.com/), using Python 3, Plotly Express, Dash, and Pandas.
    '''),
    ])
], className="main-container")

@app.callback(
    Output(component_id='state-comparison', component_property='figure'),
    [
    Input(component_id='state-dropdown-1', component_property='value'),
    Input(component_id='state-dropdown-2', component_property='value'),
    Input(component_id='state-dropdown-3', component_property='value'),
    ]
)
def compare_states(state1, state2, valtype):
    # Need to define 'data', it's expecting a dict of historical COVID data
    # Call back to a function or local file to get this data?

    # Call function to load data 
    #      e.g. data = get_historical_covid_data() # Returns dataframe?
    #  >>> df_us_historical = get_us_historical_covid_data()
    # print(f"State1: {state1}, State2: {state2}, Value Type: {valtype}")

    dfc = None
    thefig = None

    # CONFIRMED this works! The graph isn't updating with some states.
    dfc = df_us_states_historical[df_us_states_historical['state'].isin([state1, state2])].copy()
    # dfc.to_csv('/Users/zan/Desktop/combined.csv')
    # dataframe_list.append(dfa)
    # dataframe_list.append(dfb)
    # dfx = pd.concat(dataframe_list)


    ## Create the figure from the two combined data frames
    thefig = px.line(
        dfc,
        x='date', 
        y=valtype, 
        color='state', 
        )
    return thefig


if __name__ == '__main__':
    app.run_server(debug=True)

## VIEW:
# - State (independent) statistics
# List population, total cases, total deaths






