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
import shared_data as sd
import data_downloader as dd
import dashboard_utils as du

import data_sections



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
us_totals_df = sd.us_totals_df
states_totals_df = sd.states_totals_df

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
us_totals_mrate = round((us_totals_death / us_totals_cases) * 100, 2)

us_totals_deaths_noseniors = us_totals_cases - national_senior_deaths
us_totals_mrate_noseniors = round(((us_totals_death - national_senior_deaths) / us_totals_deaths_noseniors) * 100, 2)

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
    national_total_pct_age_fig.update_layout( font=sd.pie_legend_font_config, title=None, margin=sd.pie_graph_margins )

    return national_total_pct_age_fig



us_population = population_info['national']['US']['pop']

us_percent_infected = round((us_totals_cases / us_population) * 100 ,2)
us_percent_killed = round((us_totals_death / us_population) * 100 ,2)


## Add national_html_list here



## STATE STUFF
state_name_list = [ state for state in states_totals_df['state'] ]

# State Links
state_name_link_html_list = []
alphabet_upper = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

for letter in alphabet_upper:
    letter_list = [html.Span(letter + " - ", className="state-letter-item")]
    state_append_count = 0
    for state in state_name_list:
        if state.startswith(letter):
            letter_list.append(html.A([state], href="/state/" + state, className="state_link"))
            state_append_count += 1

    if state_append_count > 0:
        state_name_link_html_list.append( html.Li(letter_list) )






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



##                         ##
## # # Main App Layout # # ##
##                         ##

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        html.Div([
                html.H1("US COVID Statistics", className="main-header"),
                html.H2("[ Age and Race ]", className="main-subheader"),
                html.H3("Developed by Zero One Labs", className="main-domsubheader"),
                html.P(className="spacer"),
                html.Div([
                    html.A("National", href="/stats/national"),
                    html.Span("•"),
                    html.A("State", href="/stats/state"),
                    html.Span("•"),
                    html.A("Data Tables", href="/stats/tables"),
                    html.Span("•"),
                    html.A("About", href="/about"),
                ], className="header-links")
        ], id="header", className="header"),

        # This is where we display main content above graphs
        html.Div([
            # This is where we return the main content
            html.Div(
                [],
                className="data-container", 
                id="data-loader"
            ),

        ]),



        html.Div([

            html.P(className="spacer"),
            html.P(className="spacer"),


            html.Hr(),

            html.H4("Notes", className="main-subheader"),
            html.P("Please take care to notice and pay respect to the number of COVID deaths per state. Each bar graph displays the total, in a relative width, which may give an impresison the respective deaths are far greater than they really are. For example, one state may have a maximum of COVID deaths of around 23,000, while another state's max COVID deaths may be around 9,000."),
            html.P("State-wide data is retrieved nightly from the New York Times GitHub repository."),
            html.P("The information on this website is by no means to be taken as medical advice. If you have any serious concerns about your health, I urge you to contact your doctor or your healthcare maintenance organization (HMO). I advise you to follow your local and federal ordinances, in regards to any safety measures for mitigating the effects of COVID-19."),

            html.P(className="spacer"),
            html.P(className="spacer"),

            html.H3("Data last updated from CDC"), 

            html.P(className="spacer"),

            html.Div([
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

            html.P(className="spacer"),

            html.Div([
                html.H4("Age Group Definitions"), 
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

        ], id="footer", className="footer"),

        html.P(className="footer-spacer"),
        html.P("You are not allowed to read this far. You must scroll up immediately.", className="not-allowed")
    ]) # End "container" Div
], id="container", className="container-fluid") # End app layout Div
@app.callback(
        Output('data-loader', 'children'),
        Input('url', 'pathname')
        # Input('drop-down-chooser', 'value') # From a previous drop-down state picker. It was kinda ugly.
    )
def update_figure(pathname: None):
    value = default_state
    url_path_list = pathname.split("/")
    url_path_list.pop(0)
    # print(f"URL printout: {url_path_list}")

    url_path_one = url_path_list[0].lower()

    try:

        url_path_two = url_path_list[1]

        if url_path_one == "about":
            print("Getting about stats...")
            return data_sections.get_about_covid_stats()

        if url_path_one == "covid-definitions":
            return data_sections.get_about_covid_disease()




        if url_path_one == "stats":
            if url_path_two == "national":
                return data_sections.get_national_stats(
                us_percent_infected, 
                us_percent_killed, 
                us_totals_mrate, 
                us_totals_mrate_noseniors, 
                national_total_pct_age_table_dict,
                us_totals_cases, us_totals_death
            )

            if url_path_two == "state":
                return data_sections.get_state_picker(state_name_link_html_list)

            if url_path_two == "tables":
                return data_sections.get_data_tables(state_table_dict_df, state_table_age_dict_df, state_table_race_dict_df)


            if url_path_two == "":
                return data_sections.get_stats_page()


        if url_path_one == "state":
            if url_path_two:
                urlpath_state_name = url_path_two.strip("/").replace("%20", " ")
                if urlpath_state_name in state_name_list:
                    value = urlpath_state_name

            if url_path_two == "":
                value = default_state

            state_figure_list = data_sections.build_state_graphs(state_file, value)
            return state_figure_list        


    except Exception as e:
        # print(f"Error: pathone [{url_path_one}], error [{e}]") # Troubleshooting only.
        pass

    # Default to getting the "About" page if nothing matches above.
    return data_sections.get_about_covid_stats()


if __name__ == '__main__':
    app.run_server(debug=True,host=os.getenv('HOST','192.168.1.20')) # Use for testing
    # app.run_server(debug=True,host=os.getenv('HOST','127.0.0.1')) # Use for testing
    # app.run_server(debug=False) # Use for production




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
