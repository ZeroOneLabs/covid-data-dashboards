import json
import os
from datetime import datetime

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Symbol, Group

import plotly.express as px
import plotly.graph_objects as pxg


today = datetime.today()
today_str = today.strftime("%Y-%m-%d")

html_container_list = []
count = 0

app = dash.Dash(__name__)


us_totals_df = pd.read_csv("data/NYT/us-latest.csv")
states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")
with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "r") as f:
    state_file = json.load(f)

us_totals_cases = us_totals_df["cases"].values[0]
us_totals_death = us_totals_df["deaths"].values[0]
us_totals_mrate = round((us_totals_death / us_totals_cases) * 100, 3)


## Iterator to define list of National data

html_container_list.append(
    html.Div(children=[
        html.H2(children="National Statistics"),
        html.Table(children=[
            html.Tr(children=[
                html.Td(children="Total COVID Cases"),
                html.Td(children=f": {us_totals_cases:,}", className="nat-stat-num")
            ]),
            html.Tr(children=[
                html.Td(children="Total COVID Deaths"),
                html.Td(children=f": {us_totals_death:,}", className="nat-stat-num")
            ]),
            html.Tr(children=[
                html.Td(children="Avg Mortality Rate"),
                html.Td(children=f": {us_totals_mrate:,}%", className="nat-stat-num")
            ])
        ]),
        html.Hr()
    ])
)

    # html_container_list.append()


html_container_list.append(
    html.Div(children=[
        html.H2(children="State and Territory Statistics")
    ])
)
## Iterator to define list of graphs/data/lists for each state
for state, data in state_file.items():
    state_list = []
    
    state_id_str = state.replace(" ", "-").lower()

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
    grouped_age_demo_deaths_dict = { "Age Group": [ "Child", "Teen/Adult", "Adult", "Senior" ], "Total Deaths": [] }
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
    grouped_age_demo_deaths_dict["Total Deaths"].append(child_deaths)
    grouped_age_demo_deaths_dict["Total Deaths"].append(teenadult_deaths)
    grouped_age_demo_deaths_dict["Total Deaths"].append(adult_deaths)
    grouped_age_demo_deaths_dict["Total Deaths"].append(senior_deaths)


    ## Create dataframe for bar graphs
    age_death_bar_df = pd.DataFrame(age_demo_death_dict, columns=["Age Range", "COVID Deaths"])
    grouped_age_death_bar_df = pd.DataFrame(grouped_age_demo_deaths_dict, columns=["Age Group", "Total Deaths"])
    ## Create bar graphs
    age_death_bar = px.bar(age_death_bar_df, x="COVID Deaths", y="Age Range", orientation='h', title="Deaths by Age", color_continuous_scale="Geyser", color="COVID Deaths")
    grouped_age_death_bar = px.bar(grouped_age_death_bar_df, x="Total Deaths", y="Age Group", orientation='h', barmode="group", title="Deaths by Age (Grouped)", color_continuous_scale="Geyser", color="Total Deaths")
    ## Create pie graphs
    age_death_pie = px.pie(age_demo_death_pct_dict, values='Percent of Deaths', names='Age Range', title='Percent of COVID deaths', color_discrete_sequence=px.colors.diverging.Geyser_r)
    age_death_pie.update_traces(textposition='inside', textinfo='percent+label')
    grouped_age_death_pie = px.pie(grouped_age_demo_death_pct_dict, values='Percent of Deaths', names='Age Group', title='Percent of COVID deaths (Grouped)', color_discrete_sequence=px.colors.diverging.Geyser_r)
    grouped_age_death_pie.update_traces(textposition='inside', textinfo='percent+label')


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
    race_death_bar = px.bar(race_death_bar_df, x="COVID Deaths", y="Race Group", orientation='h', barmode="group", title="Deaths by Race")
    nonwhite_race_death_bar = px.bar(nonwhite_race_death_bar_df, x="COVID Deaths", y="Race Group", orientation='h', barmode="group", title="Deaths by Race (Non-White)")
    ## Create pie graph
    race_death_pie = fig = px.pie(race_demo_death_pct_dict, values='Percent of Deaths', names='Race Group', title='Percent of COVID deaths', color_discrete_sequence=px.colors.diverging.Geyser_r)
    race_death_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    nonwhite_race_death_pie = fig = px.pie(nonwhite_race_demo_death_pct_dict, values='Percent of Deaths', names='Race Group', title='Percent of COVID deaths (Non-White)', color_discrete_sequence=px.colors.diverging.Geyser_r)
    nonwhite_race_death_pie.update_traces(textposition='inside', textinfo='percent+label')
    


    ## List state-wide statistics
    # deaths
    # cases
    # average mortailty rate

    state_cases = states_totals_df.loc[states_totals_df["state"] == state]["cases"].values[0]
    state_death = states_totals_df.loc[states_totals_df["state"] == state]["deaths"].values[0]
    state_mrate = round((state_death / state_cases) * 100, 3)

    html_container_list.append(html.H3(children=state))
    html_container_list.append(html.Div(children=[
        
        html.Table(children=[
            html.Tr(children=[
                html.Td(children="Total Cases"),
                html.Td(children=f": {state_cases:,}", className="state-stat-num")
            ]),
            html.Tr(children=[
                html.Td(children="Total Deaths"),
                html.Td(children=f": {state_death:,}", className="state-stat-num")
            ]),
            html.Tr(children=[
                html.Td(children="Avg Mortality Rate"),
                html.Td(children=f": {state_mrate:,}%", className="state-stat-num")
            ])
        ])
    ]))


    html_container_list.append(html.H4(children="Age Statistics (Ungrouped)"))
    html_container_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-bar',className="state-figure-bar",figure=age_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-pie',className="state-figure-pie",figure=age_death_pie)], className="pie chart")
        ], className="row"))

    html_container_list.append(html.H3(children="Age Statistics (Grouped)"))
    html_container_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-bar-grouped',className="state-figure-bar",figure=grouped_age_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-pie-grouped',className="state-figure-pie",figure=grouped_age_death_pie)], className="pie chart")
        ], className="row"))

    html_container_list.append(html.H3(children="Race Statistics (All)"))
    html_container_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-bar',className="state-figure-bar",figure=race_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-pie',className="state-figure-pie",figure=race_death_pie)], className="pie chart")
        ], className="row"))

    html_container_list.append(html.H3(children="Race Statistics (Non-White)"))
    html_container_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-bar-nonwhite',className="state-figure-bar",figure=nonwhite_race_death_bar)], className="bar chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-pie-nonwhite',className="state-figure-pie",figure=nonwhite_race_death_pie)], className="pie chart")
        ], className="row"))

    html_container_list.append(html.Hr())

    ## NOTE: Uncomment to interrupt the loop and see if data is displaying correctly, without having to calculate all items.
    # count += 1
    # if count == 1:
    #     break


app.layout = html.Div(children=[
    html.Div(id="container", className="header", children=[
        html.Div(id="header", className="header", children=[
            html.Div(children=[
                html.H1(children="COVID demographic statistics US State by age and race")
            ],style={
                "marginBottom": "100px"
            })
        ]),



        html.Div(children=html_container_list, className="main-container"),

html.P(children=[
            html.Br(),
            html.H4(children="Notes"),
            # html.Br(),
            html.P(children="Please take care to notice and pay respect to the number of total deaths per state. Each bar graph displays the total, in a relative width, which may give an impresison the respective deaths are far greater than they really are."),
            html.P(children="State-wide data is retrieved nightly from the New York Times GitHub repository."),
            html.P(children=[
                html.Span(children="Mortality rates are calculated, using the CDC's definition for the methodology of calculating the mortality rate of an infectious disease using the following formula:"),
                html.Br(),
                html.Span(children="(deaths / cases) * 100 ~ per 100,000 people, or over a period of time (in this case the total span of the COVID pandemic)", className="monospaced")
            ]),
            # html.Br(),
            html.Div(children=[
            html.P(children="Age Groups are defined as follows:"), 
                html.P(children=[
                    html.Li(children=["Children: 0-14"]),
                    html.Li(children=["Teen/Adult: 15-24"]),
                    html.Li(children=["Adult: 25-64"]),
                    html.Li(children=["Senior: 65-85+"]),
                    ])
                ]),
            html.Br(),
            html.Br(),
            html.Br(),
        ]),

        html.Div(id="footer", className="footer", 
            style={
                'height': "200px"
            })

    ],
    style={
        'backgroundColor': "#fff",
        'padding': "1em"
    })
])


if __name__ == '__main__':
    app.run_server(debug=True,host=os.getenv('HOST','127.0.0.1'))
    # app.run_server(host=os.getenv('HOST','127.0.0.1'))


# print(json.dumps(parent_dict))
