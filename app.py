import os
import json
import sys
from datetime import datetime

import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px

import data_writer as dw
import data_downloader as dd

import dashboard_utils as du
import data_sections
import shared_data

today = datetime.today()
today_str = today.strftime("%Y-%m-%d")

html_container_list = []
state_info_data_list = []

dash_theme = dbc.themes.BOOTSTRAP
# dash_theme = dbc.themes.LUX
# dash_theme = dbc.themes.CYBORG

app = dash.Dash(__name__,external_stylesheets=[dash_theme])
server = app.server
app.title="Zero One Labs - US COVID Demographic Dashboard"


# TODO: Removed "default_state" and only include state data when 
# a user clicks on a state name
default_state = "California"

## Load file data
try:
    dd.download_nyt_data()
    us_totals_df = pd.read_csv("data/NYT/us-latest.csv")
    states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")
except Exception as e:
    print(e)

# Delete regions that throw errors from the States data frame
for drop_state in ["Northern Mariana Islands", "Virgin Islands", "Puerto Rico", "Guam"]:
    states_totals_df = states_totals_df.drop(
            states_totals_df[states_totals_df['state'] == drop_state].index
        )

try:
    with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "r") as f:
        state_file = json.load(f)
except:
    dw.write_data()
    with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "r") as f:
        state_file = json.load(f)

with open("data/state_info.json", "r") as jinfo:
    population_info = json.load(jinfo)


def get_national_data():
    pass


# GLOBALS
last_updated_race = pd.read_json(f"data/CDC/{today_str}-Deaths_by_Race_and_Hispanic_Origin.json")["end_week"].values[0].replace('T00:00:00.000', '')
last_updated_age = pd.read_json(f"data/CDC/{today_str}-Deaths_by_Sex_and_Age.json")["end_date"].values[0].replace('T00:00:00.000', '')



## NATIONAL STUFF

#TODO: Add total death numbers for each age group and race
#TODO: Add total death percentages for each age group and race
#TODO: Write function to create bar and pie graphs to reduce code duplication
#TODO: Write function to create "National Statistics", "State Statistics" (semi-done), and "About" html element lists
    #TODO: Put each major function in their own .py file to reduce clutter?


national_child_deaths, national_teenadult_deaths, national_adult_deaths, national_senior_deaths = 0, 0, 0, 0
for state, data in state_file.items():
    for age_demo in data["Age"]:
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue

        if age_demo == "Under 1 year" or age_demo == "1-4 years" or age_demo == "5-14 years":
            national_child_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "15-24 years" or age_demo == "25-34 years" or age_demo == "35-44 years":
            national_teenadult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "45-54 years" or age_demo == "55-64 years":
            national_adult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "65-74 years" or age_demo == "75-54 years" or age_demo == "85 years and over":
            national_senior_deaths += data["Age"][age_demo]["total_deaths"]

us_totals_cases = us_totals_df["cases"].values[0]
us_totals_death = us_totals_df["deaths"].values[0]
us_totals_mrate = round((us_totals_death / us_totals_cases) * 100, 3)

us_totals_deaths_noseniors = us_totals_cases - national_senior_deaths
us_totals_mrate_noseniors = round(((us_totals_death - national_senior_deaths) / us_totals_deaths_noseniors) * 100, 3)

# us_total_pct_age_child_deaths, us_total_pct_age_teenadlt, us_total_pct_age_advadlt, us_total_pct_age_senior
us_total_pct_age_child_deaths = round( ( national_child_deaths / us_totals_death ) * 100)
us_total_pct_age_teenadlt = round( ( national_teenadult_deaths / us_totals_death ) * 100)
us_total_pct_age_advadlt = round( ( national_adult_deaths / us_totals_death ) * 100)
us_total_pct_age_senior = round( ( national_senior_deaths / us_totals_death ) * 100)

# print(national_child_deaths, national_teenadult_deaths, national_adult_deaths, national_senior_deaths)
# print(us_total_pct_age_child_deaths, us_total_pct_age_teenadlt, us_total_pct_age_advadlt, us_total_pct_age_senior)

national_total_pct_age_dict = [
        { "Age Group": "0-14", "Percent of COVID deaths (Nationally)": us_total_pct_age_child_deaths },
        { "Age Group": "15-44", "Percent of COVID deaths (Nationally)": us_total_pct_age_teenadlt },
        { "Age Group": "45-64", "Percent of COVID deaths (Nationally)": us_total_pct_age_advadlt },
        { "Age Group": "65+", "Percent of COVID deaths (Nationally)": us_total_pct_age_senior },
]

national_total_pct_age_table_dict = {
        "row0": { "values": [ "Age Range", "Total Deaths", "% of all Deaths" ], "classname": "table-data-row" },
        "row1": { "values": [ "0-14", f"{int(national_child_deaths):,}", f"{us_total_pct_age_child_deaths}%" ], "classname": "table-data-row" },
        "row2": { "values": [ "15-44", f"{int(national_teenadult_deaths):,}", f"{us_total_pct_age_teenadlt}%"  ], "classname": "table-data-row" },
        "row3": { "values": [ "45-64", f"{int(national_adult_deaths):,}", f"{us_total_pct_age_advadlt}%"  ], "classname": "table-data-row" },
        "row4": { "values": [ "65+", f"{int(national_senior_deaths):,}", f"{us_total_pct_age_senior}%"  ], "classname": "table-data-row" }
    }



def create_nat_age_death_pct_pie() -> px.pie:
    national_total_pct_age_fig = px.pie(
        national_total_pct_age_dict, 
        values='Percent of COVID deaths (Nationally)', names='Age Group', 
        color="Age Group", 
        )
    national_total_pct_age_fig.update_traces( textposition='inside', textinfo='percent+label', showlegend=False )
    national_total_pct_age_fig.update_layout( font=pie_legend_font_config, title=None, margin=pie_graph_margins )

    return national_total_pct_age_fig



us_population = population_info['national']['US']['pop']

us_percent_infected = round((us_totals_cases / us_population) * 100 ,2)
us_percent_killed = round((us_totals_death / us_population) * 100 ,2)


## Add national_html_list here



## STATE STUFF
state_name_list = [ state for state in states_totals_df['state'] ]

# State Links
state_name_link_html_list = []
for state in state_name_list:
    state_name_link_html_list.append(
        html.A([state], href="/" + state, className="state_link")
    )





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



## DATA TABLE STUFF
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

        if age_demo == "15-24 years" or age_demo == "25-34 years" or age_demo == "35-44 years":
            teenadult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "45-54 years" or age_demo == "55-64 years":
            adult_deaths += data["Age"][age_demo]["total_deaths"]

        if age_demo == "65-74 years" or age_demo == "75-54 years" or age_demo == "85 years and over":
            senior_deaths += data["Age"][age_demo]["total_deaths"]

    state_table_age_dict["0-14"].append(child_deaths)
    state_table_age_dict["15-24"].append(teenadult_deaths)
    state_table_age_dict["25-64"].append(adult_deaths)
    state_table_age_dict["65-85+"].append(senior_deaths)

    for race_demo in data["Race"]:
        state_table_race_dict[race_demo].append(data["Race"][race_demo]["death"])

state_table_dict_df = pd.DataFrame(state_table_dict)
state_table_dict_df = state_table_dict_df.sort_values(by="Mortality Rate", ascending=False)
state_table_age_dict_df = pd.DataFrame(state_table_age_dict)
state_table_race_dict_df = pd.DataFrame(state_table_race_dict)
# END DATA TABLE STUFF


html_container_list.append(
    html.Div([

        html.H2("How deadly is COVID-19?"),

        html.P("To begin to understand the threat an infectious disease like COVID-19 presents to the greater US population (and to each State), we must first declare and understand some underlying language, which is used to define some terms."),

        html.P(className="spacer"),

        html.H5("COVID 'Case'"),

        html.P("A COVID 'Case' is a recorded event where a person submits biological samples of cells from their respiratory system or blood to test for 1 of 2 types of tests."),

        html.H6("Antigen Tests"),
        html.P("Antigen tests basically look for a protein, which is typically found in a novel coronavirus (e.g. COVID-19). These tests are generally less expensive, but can also less reliable in some cases (e.g. if the testing person is not at the peak infection stage)."),


        html.H6("Antibody Tests"),
        html.P("Antibody tests basically look for antibodies that are developed from your body to defend against diseases similar to COVID-19. This means that, if your body has recently built a defense against an attack from a novel coronavirus (MERS, SARS CoV, SARS CoV-2 [AKA COVID-19]), or a disease similar to a coronavirus, like the Flu."),
        html.P(className="spacer"),


        html.H5("COVID 'Death'"),
        
        html.P("A COVID 'Death' is a recorded event where a person dies due to the direct effects of COVID-19 or if they have positive traces of COVID-19 in their body near, or at the time, of death."),
        html.P(className="spacer"),


        html.H5("Mortality Rate"),

        html.P("The lethality of infectious diseases are defined by the rate at which a disease kills a population, which is often referred to as the disease's 'mortality rate'. After enough data is collected, these mortality rates are calculated in order to assess the threat level the disease presents to, either the immediate population from where the disease emerged, or as large as a global scale if the disease's transmission rate and vector."),


        dcc.Markdown(
            """
            Reference links

            * [List of human disease case fatality rates](https://en.wikipedia.org/wiki/List_of_human_disease_case_fatality_rates)
            * [CDC Health Statistics](https://www.cdc.gov/nchs/fastats/infectious-disease.htm)

            """),

        html.P(className="spacer"),

        html.P("This application has pulled COVID-19 data from the CDC and New York Times (see the 'Notes' section for source links) – which contains total COVID cases and death numbers. From here we can then calculate the averate national mortality rate for COVID, based on a simple percentage formula."),

        html.P(className="spacer"),
        html.P(className="spacer"),

        html.H4("National Statistics"),
        html.P(className="spacer"),


        html.P(f"{us_percent_infected}% percent of US population has been recorded as infected with COVID."),
        html.P(f"{us_percent_killed}% percent of US population has been recorded as a COVID death."),

        html.P(className="spacer"),
        html.P(className="spacer"),


        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td("Average Mortality Rate"),
                    html.Td(f"{us_totals_mrate:,}%", className="nat-stat-num")
                ]),
                html.Tr([
                    html.Td("Seniors removed **"),
                    html.Td(f"{us_totals_mrate_noseniors:,}%", className="nat-stat-num")
                ])
            ])
        ], className="stat-table table table-responsive"),
        #national_total_pct_age_fig
        #    #         html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-bar-nonwhite',className="state-figure-bar",figure=nonwhite_race_death_bar)], className="bar chart"), 

        html.P(className="spacer"),
        html.P(className="spacer"),

        html.H4("Age Statistics"),

        html.P("Percent of COVID deaths by age group"),

        # Haha! Fuck YOU! I created a method to create tables programmatically!
        du.create_html_table(national_total_pct_age_table_dict, tableClassname="stat-table table table-responsive"),

        dcc.Markdown(
            f"""
            Regarding the average State, 'advanced adults' (45-64 years) and Seniors (65+) make up about 75% of COVID deaths. Inversely, **the average survival rate for COVID is {100 - us_totals_mrate}%,** and the average survival rate for people under 64 years of age is {100 - us_totals_mrate_noseniors}%.
            """),

        html.P("** Senior (65 yrs+) deaths & cases removed from pool of calculated data, leaving ages from 0 to 64."),


        html.P(className="spacer"),
        html.P(className="spacer"),
    ])
)


##                         ##
## # # Main App Layout # # ##
##                         ##

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
                html.H1("US COVID Statistics", className="main-header"),
                html.H2("Age and Race", className="main-subheader"),
                html.H3("Developed by Zero One Labs", className="main-domsubheader")
        ], id="header", className="header"),

        html.Div(html_container_list),

        # This is where we display main content above graphs
        html.Div([
            html.Div([

                html.H2("View individual State data"),

                html.P("Below is a list of links of States in the US."),

                html.P("Click or tap on a US State to render information charts for that state. By default, this dashboard loads data for California, as that state has some of the highest rates of COVID deaths."),

                html.P("Note: You can control-click and copy a link to a State to share with your family and friends. Sharing this dashboard will also promote more sharing of knowledge. As I like to say: \"The more we know, the more we grow!\""),

                html.P(className="spacer"),

                html.H5("Choose a state"),


                html.Div([
                        state_link for state_link in state_name_link_html_list
                    ], className="state-link-list"
                ),

            ], className="state-picker-row"),
            html.P(className="spacer"),
            html.P(className="spacer"),

            # This is where we return a list of graphs
            html.Div(
                state_info_data_list,
                className="data-container", 
                id="state-info-list"
            ),

        ]),


        html.Div([
            html.P(className="spacer"),
            html.P(className="spacer"),

            html.H2("Data Tables for All States"),

            html.P("You can sort through each data category for all States. Some Territories have been excluded."),
            html.P(className="spacer"),

            html.H4("Cases, Deaths, and Mortality Rates by State"),
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
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.H4("Deaths by Age Range"),
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
            html.P(className="spacer"),
            html.H4("Deaths by Racial Group"),
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

            html.P(className="spacer"),
            html.P(className="spacer"),

            html.H3("About this COVID-19 Dashboard"),
            dcc.Markdown('''
            This dashboard was created out of necessity, when I asked myself the question "What age group makes up the majority of COVID deaths for my state?" and "most dashboards list cases with 'rolling averages' or 'last 7 days', but no deaths? How lethal is this disease if I can't measure the cases against the deaths?"...
            '''),
            html.P("[show more...]", id="purpose-title"),
            dcc.Markdown('''
            This lead me down a path of trying to find a complete set of data that I could download for my state, which then lead me to find more data for each state... which then lead me down the path to finding COVID data about age ranges and race groups.

            The ultimate purpose of this dashboard is to help people like you empower yourselves with simple, yet effective knowledge that comes from the New York Times and the CDC. I want to help educate people on generally how deadly the COVID-19 disease in the United States by pulling official data and calculating those numbers to get a mortality rate – or rather the relative chances one would have if they contracted COVID in a certain geographical area in the United States.

            **Note 1**: This graph is by no means to be taken as medical advice. If you have any serious concerns about your health, I urge you to contact your doctor or your healthcare maintenance organization (HMO). I advise you to follow your local and federal ordinances, in regards to any safety measures for mitigating the effects of COVID-19.

            **Note 2**: Age and race groups are defined at the bottom of the page.

            &nbsp;

            Below you will find a summary of national statistical data for the US, and a "state picker" which uses a drop-down utility to pick which state you would like to see graphs for. Please be aware that the graphs may take 1-2 seconds to update. Below the graphs are some data tables I created, in which you can sort each column of data (e.g. to sort states by mortality rate to see which state has the least to worst mortality rate).

            If you are viewing this data dashboard on a tablet or mobile device, I would advise you to turn your device into "landscape mode" in order to see the graphs and text a little better, or to view this on a desktop web browser.

            Thanks!

            Zan

            ''', id="purpose-div"),

            html.Hr(),

            html.H4("Notes"),
            html.P("Please take care to notice and pay respect to the number of COVID deaths per state. Each bar graph displays the total, in a relative width, which may give an impresison the respective deaths are far greater than they really are. For example, one state may have a maximum of COVID deaths of around 23,000, while another state's max COVID deaths may be around 9,000."),
            html.P("State-wide data is retrieved nightly from the New York Times GitHub repository."),
            html.Div([
                html.P("Data last updated from CDC:"), 
                html.P([
                    html.Li([f"Race data: {str(last_updated_race)}"]),
                    html.Li([f"Age data: {str(last_updated_age)}"]),
                    ])
            ]),
            html.P([
                html.Span("Mortality rates are calculated, using the CDC's definition for the methodology of calculating the mortality rate of an infectious disease using the following formula:"),
                html.Br(),
                html.Span("(deaths / cases) * 100 ~ per 100,000 people, or over a period of time (in this case the total span of the COVID pandemic)", className="monospaced")
            ]),
            html.Div([
                html.P("Age Groups are defined as follows:"), 
                html.P([
                    html.Li("Children: 0-14"),
                    html.Li("Teen/Adult: 15-44"),
                    html.Li("Adv Adult: 45-64"),
                    html.Li("Senior: 65 +"),
                    ])
            ]),

            html.Hr(),

            html.Br(),
            html.P("Data gathered from the following sources:"), 
                html.P([
                    html.Li([
                        html.A("CDC: Provisional COVID-19 Deaths - Distribution of Deaths by Race and Hispanic Origin", href="https://data.cdc.gov/NCHS/Provisional-COVID-19-Deaths-Distribution-of-Deaths/pj7m-y5uh", target="_blank")
                        ]),
                    html.Li([
                        html.A("CDC: Provisional COVID-19 - Deaths by Sex and Age", href="https://data.cdc.gov/NCHS/Provisional-COVID-19-Deaths-by-Sex-and-Age/9bhg-hcku", target="_blank")
                    ]),
                    html.Li([
                        html.A("New York Times' GitHub COVID-19 Repository", href="https://github.com/nytimes/covid-19-data", target="_blank")
                    ]),
            ]),
            html.P([html.Span("This COVID-19 data dashboard was created by "),html.A("ZeroOneLabs.com", href="https://zeroonelabs.com", target="_blank")]),
            html.Br(),
            html.Br(),
            html.Br(),
        ]),

        html.Div([
            html.H4("Roadmap"),
            html.P("I would like to implement the following features into this dashboard in the near future:"),
            html.Ul([
                html.Li("Age statistics on COVID cases, per state"),
                html.Li("Timeline of cases/deaths by age and race, per state."),
                html.Li("Animation of infection spread over each state (dot-plot graph over time)."),
            ])
        ], id="footer", className="footer"),
        html.P(className="footer-spacer"),
        html.P("You are not allowed to read this far. You must scroll up immediately.", className="not-allowed")
    ]) # End "container" Div
], id="container", className="container") # End app layout Div
@app.callback(
        Output('state-info-list', 'children'),
                Input('url', 'pathname')
                # Input('drop-down-chooser', 'value')
    )
def update_figure(pathname: None):
    value = default_state
    if pathname:
        urlpath_state_name = pathname.strip("/").replace("%20", " ")
        if urlpath_state_name in state_name_list:
            value = urlpath_state_name

    if pathname == "":
        value = default_state
    state_figure_list = data_sections.build_state_graphs(state_file, value)
    return state_figure_list


if __name__ == '__main__':
    app.run_server(debug=True,host=os.getenv('HOST','127.0.0.1'))
    # app.run_server(debug=False)




# Previous bar graphs. Kept for posterity
    ## Create bar graphs

    # state_info_data_list.append(html.Div([
    #         html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-bar-nonwhite',className="state-figure-bar",figure=nonwhite_race_death_bar)], className="bar chart"), 
    #         html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-pie-nonwhite',className="state-figure-pie",figure=nonwhite_race_death_pie)], className="pie chart")
    #     ], className="row")
    # )
    # nonwhite_race_death_bar_df = pd.DataFrame(nonwhite_race_demo_death_dict, columns=["Race Group", "COVID Deaths"])
    # nonwhite_race_death_bar = px.bar(nonwhite_race_death_bar_df, x="COVID Deaths", y="Race Group", orientation='h', barmode="group", title="Non-White Races")
    # nonwhite_race_death_bar.update_layout( font=pie_legend_font_config)
    # nonwhite_race_death_bar.update_yaxes(title=None)
    # nonwhite_race_death_bar.update_xaxes(title=None)
    # nonwhite_race_death_bar.update_layout( font=bar_legend_font_config, margin=bar_graph_margins )
    # nonwhite_race_death_bar.update_traces( texttemplate='%{x:,}', textposition='inside' )

    # nonwhite_race_death_pie = fig = px.pie(
    #     nonwhite_race_demo_death_pct_dict, 
    #     values='Percent of Deaths', names='Race Group', 
    #     title=f'{state} - Race Demographics - % COVID deaths (Non-White)', 
    #     color_discrete_sequence=px.colors.diverging.Tealrose_r,
    #     )
    # nonwhite_race_death_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    # nonwhite_race_death_pie.update_layout( font=pie_legend_font_config, title=None, margin=pie_graph_margins )

    ## Race demo statistics (non-White)
    # Create dictionary for deaths per race

    # nonwhite_race_demo_death_dict = { "Race Group": [], "COVID Deaths": [] }
    # for race_demo in data["Race"]:
    #     if race_demo == "White":
    #         continue
    #     nonwhite_race_demo_death_dict["Race Group"].append(race_demo)
    #     nonwhite_race_demo_death_dict["COVID Deaths"].append(data["Race"][race_demo]["death"])
