import json
import os
from datetime import datetime

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash.dependencies import Input, Output
from dash_table.Format import Format, Scheme, Symbol, Group

import plotly.express as px
import plotly.graph_objects as pxg

import data_writer as dw
import data_downloader as dd

today = datetime.today()
today_str = today.strftime("%Y-%m-%d")

html_container_list = []
state_info_data_list = []
app = dash.Dash(__name__)
app.title="Zero One Labs - US COVID Demographic Dashboard"

pie_legend_font_config = dict(family="Courier", size=24)
pie_graph_margins = dict(t=10, b=10, l=10, r=10)
bar_legend_font_config = dict(family="Helvetica", size=18, color="Black")
bar_graph_margins = dict(r=10)


try:
    dd.download_nyt_data()
    us_totals_df = pd.read_csv("data/NYT/us-latest.csv")
    states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")
except:
    dd.download_nyt_data()
    us_totals_df = pd.read_csv("data/NYT/us-latest.csv")
    states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")

try:
    with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "r") as f:
        state_file = json.load(f)
except:
    dw.write_data()
    with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "r") as f:
        state_file = json.load(f)

national_senior_deaths = 0
for state, data in state_file.items():
    for age_demo in data["Age"]:
        if age_demo == "65-74 years" or age_demo == "75-54 years" or age_demo == "85 years and over":
            national_senior_deaths += data["Age"][age_demo]["total_deaths"]



last_updated_race = pd.read_json(f"data/CDC/{today_str}-Deaths_by_Race_and_Hispanic_Origin.json")["end_week"].values[0].replace('T00:00:00.000', '')
last_updated_age = pd.read_json(f"data/CDC/{today_str}-Deaths_by_Sex_and_Age.json")["end_date"].values[0].replace('T00:00:00.000', '')

us_totals_cases = us_totals_df["cases"].values[0]
us_totals_death = us_totals_df["deaths"].values[0]
us_totals_mrate = round((us_totals_death / us_totals_cases) * 100, 3)
us_totals_mrate_noseniors = round(((us_totals_death - national_senior_deaths) / us_totals_cases) * 100, 3)


## Iterator to define list of National data

html_container_list.append(
    html.Div(children=[
        html.H2(children="National Statistics"),
        html.Table(children=[
            html.Tr(children=[
                html.Td(children="Totals"),
                html.Td()
            ]),
            html.Tr(children=[
                html.Td(children="COVID Cases"),
                html.Td(children=f": {us_totals_cases:,}", className="nat-stat-num")
            ]),
            html.Tr(children=[
                html.Td(children="COVID Deaths"),
                html.Td(children=f": {us_totals_death:,}", className="nat-stat-num")
            ])
        ], className="stat-table"),
        html.Table(children=[
            html.Tr(children=[
                html.Td(children="Totals"),
                html.Td()
            ]),
            html.Tr(children=[
                html.Td(children="COVID Cases"),
                html.Td(children=f": {us_totals_cases:,}", className="nat-stat-num")
            ]),
            html.Tr(children=[
                html.Td(children="COVID Deaths"),
                html.Td(children=f": {us_totals_death:,}", className="nat-stat-num")
            ])
        ], className="stat-table"),
    ])
)

## TODO: Change state iterator to function to return list of data to insert into ID of a dcc component.
## TODO: Create drop-down for each state/territory to call @app.callback
## TODO: Create @app.callback to recieve a state name, call the function to return list of data, then set the output to the cdd ID.

def build_state_graphs(state) -> list:
    state_info_data_list = []
    state_id_str = state.replace(" ", "-").lower()
    data = state_file[state]

    ## Age demo statistics
    age_demo_death_dict = { "Age Range": [], "COVID Deaths": [] }
    for age_demo in data["Age"]:
        # These group of data collects more deaths and skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue
        age_demo_death_dict["Age Range"].append(age_demo)
        age_demo_death_dict["COVID Deaths"].append(data["Age"][age_demo]["total_deaths"])


    age_demo_death_pct_dict = { "Age Range": [], "Percent of Deaths": [] }
    for age_demo in data["Age"]:
        # These group of data collects more deaths and skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue
        age_demo_death_pct_dict["Age Range"].append(age_demo)
        age_demo_death_pct_dict["Percent of Deaths"].append(data["Age"][age_demo]["pct_covid_deaths"])


    ## Grouped age statistics for percentage of COVID deaths - e.g. "Child (0-14), Teen/Adult (15-34), Adult (35-64), Senior (65-85+)"
    grouped_age_demo_death_pct_dict = { "Age Group": [ "Child", "Teen/Adult", "Adult", "Senior" ], "Percent of Deaths": [] }
    # Define variables
    child_death_pct, teenadult_death_pct, adult_death_pct, senior_death_pct = 0.0, 0.0, 0.0, 0.0

    for age_demo in data["Age"]:
        # These group of data collects more deaths and skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue

        if age_demo == "Under 1 year" or age_demo == "1-4 years" or age_demo == "5-14 years":
            child_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

        if age_demo == "15-24 years" or age_demo == "25-34 years":
            teenadult_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

        if age_demo == "35-44 years" or age_demo == "45-54 years" or age_demo == "55-64 years":
            adult_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

        if age_demo == "65-74 years" or age_demo == "75-54 years" or age_demo == "85 years and over":
            senior_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

    # Now add each category and concatenated percent for each group to dict
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(child_death_pct)
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(teenadult_death_pct)
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(adult_death_pct)
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(senior_death_pct)


    ## Grouped age statistics for total COVID deaths - e.g. "Child (0-14), Teen/Adult (15-34), Adult (35-64), Senior (65-85+)"
    grouped_age_demo_deaths_dict = { "Age Group": [ "Child", "Teen/Adult", "Adult", "Senior" ], "COVID Deaths": [] }
    # Define variables
    child_deaths, teenadult_deaths, adult_deaths, senior_deaths = 0.0, 0.0, 0.0, 0.0

    for age_demo in data["Age"]:
        # These group of data collects more deaths and skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue

        if age_demo == "Under 1 year" or age_demo == "1-4 years" or age_demo == "5-14 years":
            child_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "15-24 years" or age_demo == "25-34 years":
            teenadult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "35-44 years" or age_demo == "45-54 years" or age_demo == "55-64 years":
            adult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "65-74 years" or age_demo == "75-54 years" or age_demo == "85 years and over":
            senior_deaths += data["Age"][age_demo]["total_deaths"]

    # Now add each concatenated percent variable in the order of named age groups.
    grouped_age_demo_deaths_dict["COVID Deaths"].append(child_deaths)
    grouped_age_demo_deaths_dict["COVID Deaths"].append(teenadult_deaths)
    grouped_age_demo_deaths_dict["COVID Deaths"].append(adult_deaths)
    grouped_age_demo_deaths_dict["COVID Deaths"].append(senior_deaths)


    ## Create dataframe for bar graphs
    age_death_bar_df = pd.DataFrame(age_demo_death_dict, columns=["Age Range", "COVID Deaths"])
    grouped_age_death_bar_df = pd.DataFrame(grouped_age_demo_deaths_dict, columns=["Age Group", "COVID Deaths"])
    ## Create bar graphs
    age_death_bar = px.bar(age_death_bar_df, x="COVID Deaths", y="Age Range", orientation='h', title="Deaths by Age", color_continuous_scale="Geyser", color="COVID Deaths")
    age_death_bar.update_yaxes(title=None)
    age_death_bar.update_xaxes(title=None)
    age_death_bar.update_layout( font=bar_legend_font_config, margin=bar_graph_margins )

    grouped_age_death_bar = px.bar(grouped_age_death_bar_df, x="COVID Deaths", y="Age Group", orientation='h', barmode="group", title="Deaths by Age (Grouped)", color_continuous_scale="Geyser", color="COVID Deaths")
    grouped_age_death_bar.update_yaxes(title=None)
    grouped_age_death_bar.update_xaxes(title=None)
    grouped_age_death_bar.update_layout( font=bar_legend_font_config, margin=bar_graph_margins )

    ## Create pie graphs
    age_death_pie = px.pie(age_demo_death_pct_dict, values='Percent of Deaths', names='Age Range', title='Percent of COVID deaths', color_discrete_sequence=px.colors.diverging.Geyser_r)
    age_death_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    age_death_pie.update_layout( font=pie_legend_font_config, title=None, margin=pie_graph_margins )

    grouped_age_death_pie = px.pie(grouped_age_demo_death_pct_dict, values='Percent of Deaths', names='Age Group', title='Percent of COVID deaths (Grouped)', color_discrete_sequence=px.colors.diverging.Geyser_r)
    grouped_age_death_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    grouped_age_death_pie.update_layout( font=pie_legend_font_config, title=None, margin=pie_graph_margins )


    ## Race demo statistics
    # Create dictionary for deaths per race
    race_demo_death_dict = { "Race Group": [], "COVID Deaths": [] }
    for race_demo in data["Race"]:
        race_demo_death_dict["Race Group"].append(race_demo)
        race_demo_death_dict["COVID Deaths"].append(data["Race"][race_demo]["death"])

    # Create dictionary for percentage of race deaths
    race_demo_death_pct_dict = { "Race Group": [], "Percent of Deaths": [] }
    for race_demo in data["Race"]:
        race_demo_death_pct_dict["Race Group"].append(race_demo)
        race_demo_death_pct_dict["Percent of Deaths"].append(data["Race"][race_demo]["pct_covid_deaths"])

    ## Race demo statistics (non-White)
    # Create dictionary for deaths per race
    nonwhite_race_demo_death_dict = { "Race Group": [], "COVID Deaths": [] }
    for race_demo in data["Race"]:
        if race_demo == "White":
            continue
        nonwhite_race_demo_death_dict["Race Group"].append(race_demo)
        nonwhite_race_demo_death_dict["COVID Deaths"].append(data["Race"][race_demo]["death"])

    # Create dictionary for percentage of race deaths, minus White group
    nonwhite_race_demo_death_pct_dict = { "Race Group": [], "Percent of Deaths": [] }
    for race_demo in data["Race"]:
        if race_demo == "White":
            continue
        nonwhite_race_demo_death_pct_dict["Race Group"].append(race_demo)
        nonwhite_race_demo_death_pct_dict["Percent of Deaths"].append(data["Race"][race_demo]["pct_covid_deaths"])


    ## Create dataframes for bar graphs
    race_death_bar_df = pd.DataFrame(race_demo_death_dict, columns=["Race Group", "COVID Deaths"])
    nonwhite_race_death_bar_df = pd.DataFrame(nonwhite_race_demo_death_dict, columns=["Race Group", "COVID Deaths"])
    ## Create bar graphs
    race_death_bar = px.bar(race_death_bar_df, x="COVID Deaths", y="Race Group", orientation='h', barmode="group", title="All Races")
    race_death_bar.update_layout( font=pie_legend_font_config)
    race_death_bar.update_yaxes(title=None)
    race_death_bar.update_xaxes(title=None)
    race_death_bar.update_layout( font=bar_legend_font_config, margin=bar_graph_margins )

    nonwhite_race_death_bar = px.bar(nonwhite_race_death_bar_df, x="COVID Deaths", y="Race Group", orientation='h', barmode="group", title="Non-White Races")
    nonwhite_race_death_bar.update_layout( font=pie_legend_font_config)
    nonwhite_race_death_bar.update_yaxes(title=None)
    nonwhite_race_death_bar.update_xaxes(title=None)
    nonwhite_race_death_bar.update_layout( font=bar_legend_font_config, margin=bar_graph_margins )

    ## Create pie graph
    race_death_pie = fig = px.pie(race_demo_death_pct_dict, values='Percent of Deaths', names='Race Group', title=f'{state} - Race Demographics - % COVID deaths', color_discrete_sequence=px.colors.diverging.Tealrose_r)
    race_death_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    race_death_pie.update_layout( font=pie_legend_font_config, title=None, margin=pie_graph_margins )

    nonwhite_race_death_pie = fig = px.pie(
        nonwhite_race_demo_death_pct_dict, 
        values='Percent of Deaths', names='Race Group', 
        title=f'{state} - Race Demographics - % COVID deaths (Non-White)', 
        color_discrete_sequence=px.colors.diverging.Tealrose_r,
        )
    nonwhite_race_death_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    nonwhite_race_death_pie.update_layout( font=pie_legend_font_config, title=None, margin=pie_graph_margins )

    state_cases = states_totals_df.loc[states_totals_df["state"] == state]["cases"].values[0]
    state_death = states_totals_df.loc[states_totals_df["state"] == state]["deaths"].values[0]
    state_mrate = round((state_death / state_cases) * 100, 3)
    state_mrate_noseniors = round(((state_death - senior_deaths)/ state_cases) * 100, 3)

    state_info_data_list.append(html.H2(children=[
        html.A(children=state, id=state.replace(' ', '-'))
    ]))
    state_info_data_list.append(html.Div(children=[
        
        html.Table(children=[
            html.Th(children=[
                html.Td(children="Totals", className="state-stat-title state-stat-row"),
                html.Td()
            ]),
            html.Tr(children=[
                html.Td(children="COVID Cases", className="state-stat-title state-stat-row"),
                html.Td(children=f": {state_cases:,}", className="state-stat-num state-stat-row")
            ]),
            html.Tr(children=[
                html.Td(children="COVID Deaths", className="state-stat-title state-stat-row"),
                html.Td(children=f": {state_death:,}", className="state-stat-num state-stat-row")
            ])
        ], className="stat-table"),
        html.Table(children=[
            html.Th(children=[
                html.Td(children="Mortality Rates", className="state-stat-title state-stat-row"),
                html.Td()
            ]),
            html.Tr(children=[
                html.Td(children="All People", className="state-stat-title state-stat-row"),
                html.Td(children=f": {state_mrate:,}%", className="state-stat-num state-stat-row")
            ]),
            html.Tr(children=[
                html.Td(children="Without Seniors (case rate not adjusted)", className="state-stat-title state-stat-row"),
                html.Td(children=f": {state_mrate_noseniors:,}%", className="state-stat-num")
            ])
        ], className="stat-table")
    ]))


    state_info_data_list.append(html.H3(children="Age Statistics"))
    state_info_data_list.append(html.P(children="Note: One or more data groups (age/race) have counts between 1-9 and have been suppressed in accordance with NCHS confidentiality standards."))
    state_info_data_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-bar',className="state-figure-bar",figure=age_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-pie',className="state-figure-pie",figure=age_death_pie)], className="pie chart")
        ], className="row"))

    # state_info_data_list.append(html.H3(children="Age Statistics (Grouped)"))
    state_info_data_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-bar-grouped',className="state-figure-bar",figure=grouped_age_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-pie-grouped',className="state-figure-pie",figure=grouped_age_death_pie)], className="pie chart")
        ], className="row"))

    state_info_data_list.append(html.H3(children="Race Statistics"))
    state_info_data_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-bar',className="state-figure-bar",figure=race_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-pie',className="state-figure-pie",figure=race_death_pie)], className="pie chart")
        ], className="row"))

    # state_info_data_list.append(html.H3(children="Race Statistics (Non-White)"))
    state_info_data_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-bar-nonwhite',className="state-figure-bar",figure=nonwhite_race_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-pie-nonwhite',className="state-figure-pie",figure=nonwhite_race_death_pie)], className="pie chart")
        ], className="row"))

    # state_info_data_list.append(html.Hr())

    return state_info_data_list


## Build table of all state data
state_table_dict = {
    "State": [],
    "Cases": [],
    "Deaths": [],
    "Mortality Rate": []
}

state_table_age_dict = {
    "State": [],
    "0-14": [],
    "15-24": [],
    "25-64": [],
    "65-85+": []
}

state_table_race_dict = {
    "State": [],
    "White": [],
    "Black": [],
    "Latino": [],
    "Asian": [],
    "Multiracial": [],
    "Indian_Alaskan": [],
    "Islander": []
}




for state in state_file.keys():
    data = state_file[state]

    state_cases = states_totals_df.loc[states_totals_df["state"] == state]["cases"].values[0]
    state_death = states_totals_df.loc[states_totals_df["state"] == state]["deaths"].values[0]
    state_mrate = round((state_death / state_cases) * 100, 3)

    if state == "District of Columbia":
        state_table_dict["State"].append("DC")
        state_table_age_dict["State"].append("DC")
        state_table_race_dict["State"].append("DC")
    else:
        state_table_dict["State"].append(state)
        state_table_age_dict["State"].append(state)
        state_table_race_dict["State"].append(state)

    state_table_dict["Cases"].append(state_cases)
    state_table_dict["Deaths"].append(state_death)
    state_table_dict["Mortality Rate"].append(state_mrate)

    child_deaths, teenadult_deaths, adult_deaths, senior_deaths = 0.0, 0.0, 0.0, 0.0

    for age_demo in data["Age"]:
        # These group of data collects more deaths and skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue

        if age_demo == "Under 1 year" or age_demo == "1-4 years" or age_demo == "5-14 years":
            child_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "15-24 years" or age_demo == "25-34 years":
            teenadult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "35-44 years" or age_demo == "45-54 years" or age_demo == "55-64 years":
            adult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "65-74 years" or age_demo == "75-54 years" or age_demo == "85 years and over":
            senior_deaths += data["Age"][age_demo]["total_deaths"]

    state_table_age_dict["0-14"].append(child_deaths)
    state_table_age_dict["15-24"].append(teenadult_deaths)
    state_table_age_dict["25-64"].append(adult_deaths)
    state_table_age_dict["65-85+"].append(senior_deaths)

    ## Race demo statistics
    for race_demo in data["Race"]:
        state_table_race_dict[race_demo].append(data["Race"][race_demo]["death"])

state_table_dict_df = pd.DataFrame(state_table_dict)
state_table_age_dict_df = pd.DataFrame(state_table_age_dict)
state_table_race_dict_df = pd.DataFrame(state_table_race_dict)


##                         ##
## # # Main App Layout # # ##
##                         ##

app.layout = html.Div(children=[
    html.Div(id="container", className="big-container", children=[
        html.Div(id="header", className="header", children=[
            html.Div(children=[
                html.H1(children="US COVID demographic statistics - age and race")
            ],style={
                "marginBottom": "100px"
            })
        ]),

        # This is where we display main content above graphs
        html.Div(children=html_container_list, className="main-container"),
        html.Div(className="main-container", children=[
            # This is where we show the dropdown of states/territories to choose from
            html.Div(children=[
                html.Div(children="Choose a State/Territory: ", className="dropdown-picker-cell"),
                html.Div(children=[
                dcc.Dropdown(
                    id='drop-down-chooser',
                    options=[{'label': k, 'value': k} for k in state_file.keys()],
                    value='California', className="state-dropdown"
                )
            ], className="dropdown-picker-cell"),

            ], className="dropdown-picker-row"),
            # This is where we return a list of graphs
            html.Div(children=state_info_data_list, className="data-container", id="state-info-list"),
        ]),



        html.Div(className="main-container", children=[
            html.H2("Data Tables for All States"),

            html.P("You can sort through each data category for all States and Territories"),
            html.P(),
            html.P(),

            html.H2("COVID Cases, Deaths, and Mortality Rates"),
            dash_table.DataTable(
                id='datatable-interactivity',
                columns=[
                    {"name": i, "id": i} for i in state_table_dict_df.columns
                ],
                data=state_table_dict_df.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                column_selectable=False,
                row_selectable=False,
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 11,
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            ),
            html.P(),
            html.P(),
            html.H2("COVID Deaths by Age Group"),
            dash_table.DataTable(
                id='datatable-interactivity-age',
                columns=[
                    {"name": i, "id": i} for i in state_table_age_dict_df.columns
                ],
                data=state_table_age_dict_df.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                column_selectable=False,
                row_selectable=False,
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 11,
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            ),
            html.P("Note: One or more age groups have counts between 1-9 and have been suppressed in accordance with NCHS confidentiality standards -they will appear as zero ('0')."),
            html.P(),
            html.H2("COVID Deaths by Racial Group"),
            dash_table.DataTable(
                id='datatable-interactivity-race',
                columns=[
                    {"name": i, "id": i} for i in state_table_race_dict_df.columns
                ],
                data=state_table_race_dict_df.to_dict('records'),
                editable=False,
                filter_action="native",
                sort_action="native",
                sort_mode="single",
                column_selectable=False,
                row_selectable=False,
                row_deletable=False,
                selected_columns=[],
                selected_rows=[],
                page_action="native",
                page_current= 0,
                page_size= 11,
                style_data_conditional=[
                    {
                        'if': {'row_index': 'odd'},
                        'backgroundColor': 'rgb(248, 248, 248)'
                    }
                ]
            ),

            html.Hr(),

            html.H4(children="Notes"),
            html.P(children="Please take care to notice and pay respect to the number of COVID deaths per state. Each bar graph displays the total, in a relative width, which may give an impresison the respective deaths are far greater than they really are. For example, one state may have a maximum of COVID deaths of around 23,000, while another state's max COVID deaths may be around 9,000."),
            html.P(children="State-wide data is retrieved nightly from the New York Times GitHub repository."),
            html.Div(children=[
                html.P(children="Data last updated from CDC:"), 
                html.P(children=[
                    html.Li(children=[f"Race data: {str(last_updated_race)}"]),
                    html.Li(children=[f"Age data: {str(last_updated_age)}"]),
                    ])
            ]),
            html.P(children=[
                html.Span(children="Mortality rates are calculated, using the CDC's definition for the methodology of calculating the mortality rate of an infectious disease using the following formula:"),
                html.Br(),
                html.Span(children="(deaths / cases) * 100 ~ per 100,000 people, or over a period of time (in this case the total span of the COVID pandemic)", className="monospaced")
            ]),
            html.Div(children=[
                html.P(children="Age Groups are defined as follows:"), 
                html.P(children=[
                    html.Li(children=["Children: 0-14"]),
                    html.Li(children=["Teen/Adult: 15-24"]),
                    html.Li(children=["Adult: 25-64"]),
                    html.Li(children=["Senior: 65-85+"]),
                    ])
            ]),

            html.Hr(),


            # state_table_dict
            html.Br(),
            html.P(children="Data gathered from the following sources:"), 
                html.P(children=[
                    html.Li(children=[
                        html.A(children="CDC: Provisional COVID-19 Deaths - Distribution of Deaths by Race and Hispanic Origin", href="https://data.cdc.gov/NCHS/Provisional-COVID-19-Deaths-Distribution-of-Deaths/pj7m-y5uh", target="_blank")
                        ]),
                    html.Li(children=[
                        html.A(children="CDC: Provisional COVID-19 - Deaths by Sex and Age", href="https://data.cdc.gov/NCHS/Provisional-COVID-19-Deaths-by-Sex-and-Age/9bhg-hcku", target="_blank")
                    ]),
                    html.Li(children=[
                        html.A(children="New York Times' GitHub COVID-19 Repository", href="https://github.com/nytimes/covid-19-data", target="_blank")
                    ]),
            ]),
            html.P([html.Span("This COVID-19 data dashboard was created by "),html.A("ZeroOneLabs.com", href="https://zeroonelabs.com", target="_blank")]),
            html.Br(),
            html.Br(),
            html.Br(),
        ]),
        html.Div(id="footer", className="footer", style={'height': "200px"})
        ]) # End "container" Div
]) # End app layout Div
@app.callback(
    Output('state-info-list', 'children'),
    Input('drop-down-chooser', 'value'))
def update_figure(value):
    state_list = build_state_graphs(value)
    # print(f"Received value: {value}. State List: {state_list}")
    return state_list


if __name__ == '__main__':
    # app.run_server(debug=True,host=os.getenv('HOST','127.0.0.1'))
    # app.run_server(debug=True,host=os.getenv('HOST','192.168.1.20'))
    # app.run_server(host=os.getenv('HOST','127.0.0.1'))
    # port = int(os.environ.get("PORT", 5000))
    app.run_server(
        debug=False,
        # host="0.0.0.0",
        # port=port
    )


# print(json.dumps(parent_dict))