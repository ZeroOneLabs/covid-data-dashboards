import json
from datetime import datetime, timedelta
# from pydoc import classname

import pandas as pd
pd.options.mode.chained_assignment = None
import plotly.express as px
import plotly.graph_objects as go

from dash import html
from dash import dcc
from dash import dash_table

import shared_data as sd
import dashboard_utils as du

GRAPH_TEMPLATE="plotly_dark"


def get_national_stats(
        us_percent_infected, 
        us_percent_killed, 
        us_totals_mrate, 
        us_totals_mrate_noseniors,
        national_total_pct_age_table_dict,
        us_totals_cases, us_totals_death) -> list:

    nat_children_deaths = national_total_pct_age_table_dict["row1"]["values"][1]
    nat_teen_adult_deaths = national_total_pct_age_table_dict["row2"]["values"][1]
    nat_adult_deaths = national_total_pct_age_table_dict["row3"]["values"][1]
    nat_adv_adult_deaths = national_total_pct_age_table_dict["row4"]["values"][1]
    nat_senior_deaths = national_total_pct_age_table_dict["row5"]["values"][1]

    retval = [

        html.H1("US Statistics", className="page-title center-center"),

        html.P(className="spacer"),
        html.P(className="spacer"),
        html.P(className="spacer"),

        html.Div([
            html.Div([
                html.Span("Total Cases"),
                " : ",
                html.Span(f"{us_totals_cases:,}", className="nat-stat-num")
            ]),
            html.Div([
                html.Span("Total Deaths"),
                " : ",
                html.Span(f"{us_totals_death:,}", className="nat-stat-num")
            ]),
        ], className="colon-align section-div center-center"),

        html.P(className="spacer"),

        html.Div([
            html.Div([
                html.Span(f"Roughly {us_percent_infected:,}% "),
                "of the US population has been infected. ",
                html.Sup("*")
            ]),

            html.Div([
                html.Span(f"{us_percent_killed:,}% ", className="us-nat-death-num"),
                "of the US population has died from COVID. ",
                html.Sup("**")
            ]),
        ], className="section-div center-center"),


        html.P(className="spacer"),

        html.Div([
            "Since March of 2020, the mortality rate for COVID is ",
            html.Span(f"{us_totals_mrate:,}%", className="nat-stat-num"),
            ". When the deaths of senior citizens (65+ years) are removed"\
            " from the total of COVID deaths, the mortality rate drops to ",
            html.Span(f"{us_totals_mrate_noseniors:,}%", className="nat-stat-num"),
            "."
        ], className="section-div  center-center"),


        html.P(className="spacer"),

        html.Div([

        
            html.H2("Deaths by age group"),
            html.P([
                "Total recorded COVID deaths since March of 2020",
                html.Sup(" ***")],
            ),
            
            html.P(className="spacer"),
            html.P(className="spacer"),


            html.Div([
                html.Div([
                    html.Span("Children (0-14) "),
                    " : ",
                    html.Span(f"{nat_children_deaths}", className="nat-stat-num")
                ]),
                html.P(className="spacer"),
                html.Div([
                    html.Span("Teen-adults (15-24) "),
                    " : ",
                    html.Span(f"{nat_teen_adult_deaths}", className="nat-stat-num")
                ]),
                html.Div([
                    html.Span("Adults (25-44) "),
                    " : ",
                    html.Span(f"{nat_adult_deaths}", className="nat-stat-num")
                ]),
                html.Div([
                    html.Span("Advanced adults (45-64) "),
                    " : ",
                    html.Span(f"{nat_adv_adult_deaths}", className="nat-stat-num")
                ]),
                html.Div([
                    html.Span("Seniors (65+) "),
                    " : ",
                    html.Span(f"{nat_senior_deaths}", className="nat-stat-num us-nat-death-num")
                ]),
            ], className="colon-align center-center"),

        ], className="section-div"),


        html.P(className="spacer"),
        html.P(className="spacer"),
        html.P(className="spacer"),

        html.P([
            "* Positive COVID cases have not been differentiated between",
            " antigen-positive or antibody-positive (which can be triggered",
            " by developing antibodies to fight off diseases that are similar",
            " to SARS-CoV-2 (COVID-19) or false-positive results (",
            html.A(
                "source CDC",
                href="https://www.cdc.gov/coronavirus/2019-ncov/testing/serology-overview.html",
                target="_blank"
            ),
            ")."
        ]),
        html.P([
            "** COVID deaths included, were significantly and relatively higher with people",
            " that were obese, had diabetes, neurocognitive disorders",
            " (including including dementia and Alzheimer’s disease),",
            " chronic obstructive pulmonary disease, aplastic anemia,",
            " heart disease, and thyroid disorders, etc (",
            html.A("source CDC", href="https://www.cdc.gov/pcd/issues/2021/21_0123.htm", target="_blank"),
            ")."
        ]),
        html.P([
            "*** Age demographic data pulled directly from CDC datasets,",\
            " which included COVID deaths and COVID+pneumonia deaths.",\
            " This means the combined deaths for the age demographic may",\
            " differ from the national total of COVID deaths.",
        ]),
        html.P(className="spacer"),
        html.P(className="spacer"),
        html.P(className="spacer"),
        html.P(className="spacer"),
    ]
    return retval


def get_data_tables(state_table_dict_df, state_table_age_dict_df, state_table_race_dict_df) -> list:
    retval = [

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
                    'backgroundColor': 'rgb(40, 40, 40)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
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
                    'backgroundColor': 'rgb(40, 40, 40)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
        ),


        html.Div([
            html.P("Note: One or more age groups have counts between 1-9 and have been suppressed in accordance with NCHS confidentiality standards -they will appear as zero ('0')."),
        ], className="section-div"),

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
                    'backgroundColor': 'rgb(40, 40, 40)'
                }
            ],
            style_header={
                'backgroundColor': 'rgb(30, 30, 30)',
                'color': 'white'
            },
            style_data={
                'backgroundColor': 'rgb(50, 50, 50)',
                'color': 'white'
            },
        )

    ]
    return retval


def get_about_covid_disease() -> list:
    retval = [

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
        html.P(className="spacer")

    ]

    return retval


def get_about_covid_stats() -> list:
    retval = [

        html.H1("About this dashboard", className="site-title"),
        html.P(className="spacer"),

        html.Div([

            dcc.Markdown('''
            This dashboard was created after I asked myself the question \
            "What age group makes up the majority of COVID deaths for my state?" \
            Most dashboards that I could find at the time listed cases with \
            'rolling averages' or 'last 7 days', but why not deaths? How \
            was I able to find out how lethal COVID was if I can't measure \
            the cases against the deaths?
            '''),

            dcc.Markdown('''
            This lead me down a path of trying to find a complete sets of data \
            which I could download for the US and each state. Then I was able to \
            find data sets for age and race demographics. Once I got the first \
            draft of the dashboard up and running, I realized I had something \
            powerful in my hands: data which could help a lot of people.
            
            I want people to be able to plainly see how deadly this COVID-19 \
            disease is affecting people in the United States, and I hope that \
            this dashboard helps you empower yourselves with simple, \
            yet effective knowledge, which is sourced from the New York Times and \
            the CDC.
            ''', id="purpose-div"),
        ], className="section-div")

    ]
    return retval


def get_covid_mortality_info() -> list:
    """Returns data section containing all Dash HTML elements for the "How deadly is COVID-19?" section.

    Returns:
        html.Div
    """


    retval = [

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
        html.P(className="spacer")

    ]
    return retval


def get_state_picker(state_name_link_html_list) -> list:
    retval = [

        html.H1("View individual State data", className="page-title"),
        html.P("Click or tap on a US State below."),

        html.P(className="spacer"),

        html.H5("Choose a state"),
        html.Div([
                state_link for state_link in state_name_link_html_list
            ], className="state-link-list"
        )
    ]
    return retval


def build_state_graphs(json_state_file, state_name, state_table_dict_df, us_totals_cases, us_totals_death, us_population, states_historical_df) -> list:
    state_info_data_list = []
    state_id_str = state_name.replace(" ", "-").lower()
    data = json_state_file[state_name]

    date_today_str = datetime.strftime(datetime.today(), "%Y-%m-%d")
    date_twodays_ago_str = datetime.strftime((datetime.now() - timedelta(2)), "%Y-%m-%d")
    date_sixty_days_ago = datetime.now() - timedelta(60)
    date_sixty_days_ago_str = datetime.strftime(date_sixty_days_ago, "%Y-%m-%d")
    date_fifty_nine_days_ago = datetime.now() - timedelta(59)
    date_fifty_nine_days_ago_str = datetime.strftime(date_fifty_nine_days_ago, "%Y-%m-%d")
    date_yesterday = datetime.now() - timedelta(1)
    date_yesterday_str = datetime.strftime(date_yesterday, "%Y-%m-%d")

    df = states_historical_df


    # Update the 'date' field to datetime objects
    df.date=pd.to_datetime(df.date)

    bar_legend_font_config = dict(family="Helvetica", size=18, color="Black")

    with open("data/state_info.json", "r") as jfile:
        state_info_jata = json.load(jfile)

    for the_state in state_info_jata['states']:
        if state_info_jata['states'][the_state]['long'] == state_name:
            # print(state_info_jata['states'][the_state]['long'])
            neighbors_list = state_info_jata['states'][the_state]['neighbors']
            neighbors_list.append(the_state)

    neighbors_list_long = []
    for state_short in neighbors_list:
        neighbors_list_long.append(state_info_jata['states'][state_short]['long'])

    state_neighbor_df = df[df['state'].isin(neighbors_list_long)]


    state_line_graph_linear_death = px.line(
        state_neighbor_df,
        x='date',
        y='deaths',
        color='state',
        title="Deaths",
        template=GRAPH_TEMPLATE
    )
    state_line_graph_linear_death.update_layout(font=sd.line_legend_font_config)

    state_line_graph_linear_cases = px.line(
        state_neighbor_df,
        x='date',
        y='cases',
        color='state',
        title="Cases",
        template=GRAPH_TEMPLATE
    )
    state_line_graph_linear_cases.update_layout(font=sd.line_legend_font_config)

    state_line_graph_log_death = px.line(
        state_neighbor_df,
        x='date',
        y='deaths',
        color='state',
        title="Deaths",
        template=GRAPH_TEMPLATE
    )
    state_line_graph_log_death.update_yaxes(type="log")
    state_line_graph_log_death.update_layout(font=sd.line_legend_font_config)

    state_line_graph_log_cases = px.line(
        state_neighbor_df,
        x='date',
        y='cases',
        color='state',
        title="Cases",
        template=GRAPH_TEMPLATE
    )
    state_line_graph_log_cases.update_yaxes(type="log")
    state_line_graph_log_cases.update_layout(font=sd.line_legend_font_config)


    df_historical_last_sixty = df.loc[
        (df['date'] > date_sixty_days_ago_str) & (df['date'] < date_yesterday_str)
    ].copy()
    df_historical_last_sixty_group = df_historical_last_sixty[
        df_historical_last_sixty['state'].isin(neighbors_list_long)
    ].copy()

    sixty_day_old_state_deaths = df_historical_last_sixty.loc[
        (df_historical_last_sixty['date'] == date_fifty_nine_days_ago_str) &
        (df_historical_last_sixty['state'] == state_name),
        "deaths"
    ].values[0]
    state_last_sixty_deaths = df_historical_last_sixty.loc[
        (df_historical_last_sixty['date'] == date_twodays_ago_str) &
        (df_historical_last_sixty['state'] == state_name),
        "deaths"
    ].values[0]

    sixty_day_old_state_cases = df_historical_last_sixty.loc[
        (df_historical_last_sixty['date'] == date_fifty_nine_days_ago_str) &
        (df_historical_last_sixty['state'] == state_name),
        "cases"
    ].values[0]
    state_last_sixty_cases = df_historical_last_sixty.loc[
        (df_historical_last_sixty['date'] == date_twodays_ago_str) &
        (df_historical_last_sixty['state'] == state_name),
        "cases"
    ].values[0]

    state_last_sixty_deaths = state_last_sixty_deaths - sixty_day_old_state_deaths
    state_last_sixty_cases = state_last_sixty_cases - sixty_day_old_state_cases
    sixty_day_mortality_rate = round((state_last_sixty_deaths / state_last_sixty_cases) * 100,3)
    sixty_day_survival_rate = 100 - sixty_day_mortality_rate

    df_historical_oldest_day = df.loc[
        df['date'] == date_sixty_days_ago_str
    ].copy()


    # ## Create state-specific dataframe from master dataframe
    # state_df = df_historical_last_sixty.loc[df_historical_last_sixty['state'] == state_name]


    for state_neighbor in neighbors_list_long:
        df_state_single = df_historical_last_sixty_group.loc[df_historical_last_sixty_group['state'] == state_neighbor]
        for case_type in ["cases", "deaths"]:
            state_oldest_case_val = df_historical_oldest_day.loc[df_historical_oldest_day['state'] == state_neighbor, case_type].values[0]

            for the_date in df_state_single['date']:
                new_case_val = 0
                current_case_val = df_historical_last_sixty_group.loc[
                    (df_historical_last_sixty_group['state'] == state_neighbor) & (df_historical_last_sixty_group['date'] == the_date), case_type
                ].values[0]
                new_case_val = current_case_val - state_oldest_case_val

                df_historical_last_sixty_group.loc[
                    (df_historical_last_sixty_group['state'] == state_neighbor) & (df_historical_last_sixty_group['date'] == the_date), case_type
                ] = new_case_val


    state_line_graph_linear_death_last_sixty = px.line(df_historical_last_sixty_group,
        x='date', y='deaths', color='state', title="Deaths", template=GRAPH_TEMPLATE)
    state_line_graph_linear_death_last_sixty.update_layout(font=sd.line_legend_font_config)

    state_line_graph_linear_cases_last_sixty = px.line(df_historical_last_sixty_group,
        x='date', y='cases', color='state', title="Cases", template=GRAPH_TEMPLATE)
    state_line_graph_linear_cases_last_sixty.update_layout(font=sd.line_legend_font_config)

    state_line_graph_log_death_last_sixty = px.line(df_historical_last_sixty_group,
        x='date', y='deaths', color='state', title="Deaths", template=GRAPH_TEMPLATE)
    state_line_graph_log_death_last_sixty.update_yaxes(type="log")
    state_line_graph_log_death_last_sixty.update_layout(font=sd.line_legend_font_config)

    state_line_graph_log_cases_last_sixty = px.line(df_historical_last_sixty_group,
        x='date', y='cases', color='state', title="Cases", template=GRAPH_TEMPLATE)
    state_line_graph_log_death_last_sixty.update_yaxes(type="log")
    state_line_graph_log_cases_last_sixty.update_layout(font=sd.line_legend_font_config)




    ## Age demo statistics
    age_demo_death_dict = { "Age Range": [], "COVID Deaths": [] }
    for age_demo in data["Age"]:
        # These groups collect more deaths which skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue
        age_demo_death_dict["Age Range"].append(age_demo)
        age_demo_death_dict["COVID Deaths"].append(data["Age"][age_demo]["total_deaths"])


    age_demo_death_pct_dict = { "Age Range": [], "Percent of Deaths": [] }
    for age_demo in data["Age"]:
        # These groups collect more deaths which skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue
        age_demo_death_pct_dict["Age Range"].append(age_demo)
        age_demo_death_pct_dict["Percent of Deaths"].append(data["Age"][age_demo]["pct_covid_deaths"])


    ## Grouped age statistics for percentage of COVID deaths - e.g. "Child (0-14), Teen/Adult (15-44), Adult (45-64), Senior (65-85+)"
    grouped_age_demo_death_pct_dict = { "Age Group": [ "Child", "Teen/Adult", "Adv Adult", "Senior" ], "Percent of Deaths": [] }
    # Define variables
    child_death_pct, teenadult_death_pct, adult_death_pct, senior_death_pct = 0.0, 0.0, 0.0, 0.0

    for age_demo in data["Age"]:
        # These groups collect more deaths which skews the visual representation in the graphs and pie charts.
        if age_demo == "50-64 years" or age_demo == "40-49 years" or age_demo == "30-39 years" or age_demo == "0-17 years" or age_demo == "18-29 years":
            continue

        if age_demo == "Under 1 year" or age_demo == "1-4 years" or age_demo == "5-14 years":
            child_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

        if age_demo == "15-24 years" or age_demo == "25-34 years" or age_demo == "35-44 years":
            teenadult_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

        if age_demo == "45-54 years" or age_demo == "55-64 years":
            adult_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

        if age_demo == "65-74 years" or age_demo == "75-54 years" or age_demo == "85 years and over":
            senior_death_pct += data["Age"][age_demo]["pct_covid_deaths"]

    # Now add each category and concatenated percent for each group to dict
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(child_death_pct)
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(teenadult_death_pct)
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(adult_death_pct)
    grouped_age_demo_death_pct_dict["Percent of Deaths"].append(senior_death_pct)


    ## Grouped age statistics for total COVID deaths - e.g. "Child (0-14), Teen/Adult (15-44), Adv Adult (45-64), Senior (65-85+)"
    grouped_age_demo_deaths_dict = { "Age Group": [ "Child", "Teen/Adult", "Adv Adult", "Senior" ], "COVID Deaths": [] }

    # Define variables
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

    # Now add each concatenated percent variable in the order of named age groups.
    grouped_age_demo_deaths_dict["COVID Deaths"].append(child_deaths)
    grouped_age_demo_deaths_dict["COVID Deaths"].append(teenadult_deaths)
    grouped_age_demo_deaths_dict["COVID Deaths"].append(adult_deaths)
    grouped_age_demo_deaths_dict["COVID Deaths"].append(senior_deaths)

    # previous color settings: , color_continuous_scale="Geyser", color="COVID Deaths"
    age_death_bar_df = pd.DataFrame(age_demo_death_dict, columns=["Age Range", "COVID Deaths"])
    age_death_bar = px.bar(
        age_death_bar_df,
        x="COVID Deaths",
        y="Age Range",
        orientation='h',
        title="COVID deaths by Age",
        template=GRAPH_TEMPLATE
    )
    age_death_bar.update_yaxes(title=None)
    age_death_bar.update_xaxes(title=None)
    age_death_bar.update_layout( font=sd.bar_legend_font_config, margin=sd.bar_graph_margins )
    age_death_bar.update_traces( texttemplate='%{x:,}', textposition='auto' )

    ## Create dataframe for bar graphs
    # grouped_age_death_bar_df = pd.DataFrame(grouped_age_demo_deaths_dict, columns=["Age Group", "COVID Deaths"])
    ## previous color settings: color_continuous_scale=bar_color_scale, color="COVID Deaths"
    # grouped_age_death_bar = px.bar(grouped_age_death_bar_df, x="COVID Deaths", y="Age Group", orientation='h', barmode="group", title="Deaths by Age (Grouped)")
    # grouped_age_death_bar.update_yaxes( title=None )
    # grouped_age_death_bar.update_xaxes( title=None )
    # grouped_age_death_bar.update_layout( font=bar_legend_font_config, margin=sd.bar_graph_margins )
    # grouped_age_death_bar.update_traces( texttemplate='%{x:,}', textposition='auto' )

    ## Create pie graphs
    # previous color settings: color_discrete_sequence=["red", "green", "blue"]
    age_death_pie = px.pie(
        age_demo_death_pct_dict,
        values='Percent of Deaths',
        names='Age Range',
        title='Percent of COVID deaths',
        template=GRAPH_TEMPLATE
        )
    age_death_pie.update_traces( textposition='inside', textinfo='percent+label', showlegend=False )
    age_death_pie.update_layout( font=sd.pie_legend_font_config, title=None, margin=sd.pie_graph_margins )

    ## previous color settings: color_discrete_sequence=px.colors.diverging.Geyser_r
    grouped_age_death_pie = px.pie(
        grouped_age_demo_death_pct_dict,
        values='Percent of Deaths',
        names='Age Group',
        title='Percent of COVID deaths (Grouped)',
        template=GRAPH_TEMPLATE
    )
    grouped_age_death_pie.update_traces( textposition='inside', textinfo='percent+label', showlegend=False )
    grouped_age_death_pie.update_layout( font=sd.pie_legend_font_config, title=None, margin=sd.pie_graph_margins )


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



    # Create dictionary for percentage of race deaths, minus White group
    nonwhite_race_demo_death_pct_dict = { "Race Group": [], "Percent of Deaths": [] }
    for race_demo in data["Race"]:
        if race_demo == "White":
            continue
        nonwhite_race_demo_death_pct_dict["Race Group"].append(race_demo)
        nonwhite_race_demo_death_pct_dict["Percent of Deaths"].append(data["Race"][race_demo]["pct_covid_deaths"])


    ## Create dataframes for bar graphs
    race_death_bar_df = pd.DataFrame(race_demo_death_dict, columns=["Race Group", "COVID Deaths"])
    ## Create bar graphs
    race_death_bar = px.bar(
        race_death_bar_df,
        x="COVID Deaths",
        y="Race Group",
        orientation="h",
        barmode="group",
        title="COVID deaths by race",
        template=GRAPH_TEMPLATE
    )
    race_death_bar.update_layout( font=sd.pie_legend_font_config)
    race_death_bar.update_yaxes(title=None)
    race_death_bar.update_xaxes(title=None)
    # race_death_bar.update_layout( font=bar_legend_font_config, margin=sd.bar_graph_margins )
    race_death_bar.update_traces( texttemplate='%{x:,}', textposition='auto' )


    ## Create pie graph
    race_death_pie = px.pie(
        race_demo_death_pct_dict,
        values="Percent of Deaths",
        names="Race Group",
        title=f"{state_name} - Race Demographics - % COVID deaths",
        color_discrete_sequence=px.colors.diverging.Tealrose_r,
        template=GRAPH_TEMPLATE
    )
    race_death_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    race_death_pie.update_layout( font=sd.pie_legend_font_config, title=None, margin=sd.pie_graph_margins )


    state_cases = sd.states_totals_df.loc[sd.states_totals_df["state"] == state_name]["cases"].values[0]
    state_death = sd.states_totals_df.loc[sd.states_totals_df["state"] == state_name]["deaths"].values[0]
    state_mrate = round((state_death / state_cases) * 100, 3)
    state_survival_rate = 100 - state_mrate
    # state_mrate_noseniors = round(((state_death - senior_deaths)/ (state_cases - senior_deaths)) * 100, 3)

    state_pct_of_natl_cases = round((state_cases / us_totals_cases) * 100, 2)
    state_pct_of_natl_deaths = round((state_death / us_totals_death) * 100, 2)

    # state_pct_of_natl_pop_cases = round((state_cases / us_population) * 100, 2)
    # state_pct_of_natl_pop_deaths = round((state_death / us_population) * 100, 3)

    # state_table_dict_df = state_table_dict_df.sort_values(by="Deaths", ascending=False)
    # state_rank = state_table_dict_df[state_table_dict_df["State"] == state].index[0]
    # print(state_table_dict_df.to_dict())

    state_rank_list = []
    state_rank_dict = state_table_dict_df.to_dict()
    try:
        for state_id, teh_state in state_rank_dict['State'].items():
            state_rank_list.append(
                {'state': teh_state, 'mortality_rate': state_rank_dict['Mortality Rate'][state_id]}
            )

        def sort_states(s):
            return s['mortality_rate']

        state_rank_list.sort(key=sort_states, reverse=True)
        state_rank = state_rank_list.index({'state': state_name, 'mortality_rate': state_mrate})

        state_top_rank = state_rank_list[0]['state']
        state_bot_rank = state_rank_list[-1]['state']

        state_rank += 1
    except Exception as e:
        # print(f"Error: {e}. State List: {state_rank_list}")
        state_rank = "unknown "



    state_info_data_list.append(
        html.Div([

            html.H1(state_name, className="page-title"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            
            # Section Div
            html.Div([
                html.H2("Case and Death Rates"),
                html.P(className="spacer"),
                
                dcc.Markdown(
                    f"""Since March of 2020, the CDC has recorded COVID statistics for \
                    {state_name} with {state_cases:,} cases and {state_death:,} deaths."""
                ),
                html.P(className="spacer"),
                dcc.Markdown("""Using the following formula:"""),
                dcc.Markdown(f"""`((cases / deaths) * 100) = m`"""),
                dcc.Markdown(f"""the mortality rate (`m`) for {state_name} calculates to {state_mrate:,}% (inversely, \
                    the survival rate would be {state_survival_rate}%)."""),

                html.P(className="spacer"),
                html.P(className="spacer"),

                html.P(f"For the last ~60 days, {state_name} has seen {state_last_sixty_cases:,} \
                    cases and {state_last_sixty_deaths:,} deaths. The mortality rate for the last 60 days \
                    is {sixty_day_mortality_rate:,}% (survival rate is {sixty_day_survival_rate:,}%)."),

                html.P(className="spacer"),

                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td(""),
                            html.Td("Cases"),
                            html.Td("Deaths"),
                            html.Td("Mortality Rate")
                        ]),
                        # TD class names: state-stat-title, state-stat-num
                        html.Tr([
                            html.Td("All Time"),
                            html.Td(f"{state_cases:,}"),
                            html.Td(f"{state_death:,}"),
                            html.Td(f"{state_mrate:,}")
                        ]),
                        html.Tr([
                            html.Td("Last 60 days"),
                            html.Td(f"{state_last_sixty_cases:,}"),
                            html.Td(f"{state_last_sixty_deaths:,}"),
                            html.Td(f"{sixty_day_mortality_rate:,}")
                        ]),
                    ])
                ], className="table table-responsive"),
            ], className="section-div"),

            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),

            html.Div([
                
                html.H2(f"{state_name} vs U.S. statistics"),
                
                html.P(f"COVID cases for {state_name} make up {state_pct_of_natl_cases}% \
                    of all recorded cases in the US. Deaths make up {state_pct_of_natl_deaths}%. \
                    Currently {state_name} is ranked #{state_rank} against all other States \
                    and the District of Columbia. The higher the rank means higher mortality \
                    rate. The state with Rank #1 is {state_top_rank} and the state with the \
                    lowest mortality rate is {state_bot_rank}."),
                
            ], className="section-div"),

            html.P(className="spacer"),
            html.P(className="spacer"),


            html.H2("Graphs"),
            html.P(className="spacer"),

            html.H3("Age Statistics"),

            # "COVID Deaths by Age" age range chart
            html.Div([
                dcc.Graph(
                    id=state_id_str + '-deaths-per-age-bar-grouped',
                    className="state-figure-bar",
                    figure=age_death_bar,
                    config={
                        "scrollZoom": False,
                        "displayModeBar": False,
                        "responsive": True,
                        "editable": False,
                        "staticPlot": True
                        }
                )],
                className="chart"
            ),

            # "COVID Deaths by Age" group chart
            # html.Div([
            #     dcc.Graph(
            #         id=state_id_str + '-deaths-per-age-pie-grouped',
            #         className="state-figure-pie",
            #         figure=grouped_age_death_pie,
            #         config={
            #             "scrollZoom": False,
            #             "displayModeBar": False,
            #             "responsive": True,
            #             "editable": False,
            #             "staticPlot": True
            #             }
            #     )],
            #     className="chart"
            # ),

            html.P(
            "Note: One or more demographic groups (age/race), which have \
            death counts between 1-9, have been suppressed in \
            accordance with NCHS confidentiality standards."),

            html.P(className="spacer"),
            html.P(className="spacer"),

            html.Div([
                
                html.H3("Race Statistics"),
                html.P(className="spacer"),

                html.Div([
                    dcc.Graph(
                        id=state_id_str + '-deaths-per-race-bar',
                        className="state-figure-bar",
                        figure=race_death_bar,
                        config={
                            "scrollZoom": False,
                            "displayModeBar": False,
                            "responsive": True,
                            "editable": False,
                            "staticPlot": True
                            }
                    )],
                    className="chart"),
                # html.Div([
                #     dcc.Graph(
                #         id=state_id_str + '-deaths-per-race-pie',
                #         className="state-figure-pie",
                #         figure=race_death_pie,
                #         config={
                #             "scrollZoom": False,
                #             "displayModeBar": False,
                #             "responsive": True,
                #             "editable": False,
                #             "staticPlot": True
                #             }
                #     )],
                #     className="chart"),
                
            ], className="section-div"),

            html.P(className="spacer"),

            html.Div([
                
                html.H3(
                    f"{state_name} vs their neighbors",
                    className="main-subheader"
                ),

                html.P(f"The following graphs compare {state_name} versus their neighbors ({', '.join(x for x in neighbors_list_long)})."),
                html.P(f"Note: If the state is Hawaii or Alaska, its listed neighbors are states with comparable populations."),

                html.P(className="spacer"),
                html.P(className="spacer"),
                html.P(className="spacer"),
                html.P(className="spacer"),
                
                html.H4("Linear Comparison (since Jan 2020)"),
                html.P(className="spacer"),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-deaths-linear-line',
                            className="state-figure-line",
                            figure=state_line_graph_linear_death,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    ),
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-cases-linear-line',
                            className="state-figure-pie",
                            figure=state_line_graph_linear_cases,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    )
                ], className="row"),
            ], className="section-div"),


            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),


            html.Div([
                
                html.H4("Logarithmic Comparison (since Jan 2020)"),
                html.P(className="spacer"),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-deaths-per-race-bar',
                            className="state-figure-bar",
                            figure=state_line_graph_log_death,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    ),
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-deaths-per-race-pie',
                            className="state-figure-pie",
                            figure=state_line_graph_log_cases,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    )],
                    className="row"
                ),
            ], className="sectino-div"),


            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),

            html.Div([
                
                html.H3("What is Linear vs Logarithmic?"),
                html.P(className="spacer"),
                html.P(className="spacer"),

                dcc.Markdown(f"""
                **Linear line graphs** represent a *1:1 representation* of values as \
                they grow on the X and Y axis. What this means, is if one state \
                has a value of 100 cases on *day 1* and 200 cases on day 2, and \
                another state has 5 cases on *day 1* and 10 cases on day 2, the \
                line graph will show a difference (i.e. a large gap) of 190 cases \
                on the 2nd day."),

                **Logarithmic line graphs** represent a *relative representation* \
                of values as they grow on the X and Y axis. What this means, is if \
                one state has a value of 100 cases on *day 1* and 200 cases on day \
                2, and *another state* has 5 cases on *day 1* and 10 cases on day \
                2, they both have a 200% increase - thus they have an equally \
                relative change in percent between days on the 2nd day (i.e. \
                there would be no gap between the lines).
                
                What this means, in regards to following COVID 'case' and 'death' \
                number trends, is that when we use logarithmic representations of \
                data, we can compare the patterns and/or tragectory of how the \
                disease might progress throughout those regions. 
                
                One piece of information which is very important to observe and \
                understand: **The closer the logarithmic lines are for each data \
                point (day of the month, i.e. the line pattern), the closer each \
                state is related, regarding their respective case and mortality \
                trends**. This means that if New York and Deleware have the same \
                relative increase in deaths, it could lean towards correlating \
                extra-carricular contexts between regions - for example, enforced \
                mask mandates, vaccines rates, local shut-downs, altitude, air \
                humidity, storm patterns, proximity to similar borders or \
                interstates, average poverty level, birth rate, or population density.

                Now let's take a look at {state_name} and each of their neighbors \
                for the last 60 days, in order to see a more recent picture of how \
                the disease is developing in these regions.
                """),
                
            ], className="section-div"),

            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),

            html.Div([
                
                html.H4("Linear Comparison (last 60 days)"),
                html.P(className="spacer"),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-deaths-linear-line',
                            className="state-figure-line",
                            figure=state_line_graph_linear_death_last_sixty,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    ), 
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-cases-linear-line',
                            className="state-figure-pie",
                            figure=state_line_graph_linear_cases_last_sixty,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    )],
                    className="row"
                ),
                
            ], className="section-div"),

            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),


            html.Div([
                
                html.H4("Logarithmic Comparison (last 60 days)"),
                html.P(className="spacer"),

                html.Div([
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-deaths-per-race-bar',
                            className="state-figure-bar",
                            figure=state_line_graph_log_death_last_sixty,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    ), 
                    html.Div([
                        dcc.Graph(
                            id=state_id_str + '-deaths-per-race-pie',
                            className="state-figure-pie",
                            figure=state_line_graph_log_cases_last_sixty,
                            config={
                                "scrollZoom": False,
                                "displayModeBar": False,
                                "responsive": True,
                                "editable": False,
                                "staticPlot": True
                                }
                        )],
                        className="line chart"
                    )],
                    className="row"
                ),
            ], className="section-div"),


            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),
            html.P(className="spacer"),

        ])    
    )

    return state_info_data_list


def get_footer(last_updated_race, last_updated_age) -> list:
    retval = [

        html.P(className="spacer"),
        html.Hr(),
        html.P(className="spacer"),

        html.H4("Spread the word - the more we know, the more we grow!"),
        html.P(className="spacer"),

        html.P("This project can only be as successful as the people who get involved and share this dashboard app. Please help me spread the word!"),
        html.Ul([
            html.Li(html.A("Share to Facebook", href="https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fcovid-state-demographic-data.herokuapp.com%2F", target="_blank")),
            html.Li(html.A("Share to Twitter", href="https://twitter.com/intent/tweet?text=Check out this awesome COVID data dashboard I found via @ZeroOneLabs: https%3A//covid-state-demographic-data.herokuapp.com/", target="_blank")),
            html.Li(html.A("Share to LinkedIn", href="https://www.linkedin.com/shareArticle?mini=true&url=https%3A//covid-state-demographic-data.herokuapp.com/&title=Check%20out%20this%20awesome%20COVID%20data%20dashboard!&summary=&source=", target="_blank")),
        ]),


        html.P(className="spacer"),
        html.P(className="spacer"),


        html.H4("Notes"),
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

        html.P("Data calcuated from the CDC does not include deaths with additional diseases, such as Pneumonia or Flu."),

        html.P(className="spacer"),

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
        html.Div([""], id="dev-info")

    ]
    return retval


def main():
    pass


if __name__ == "__main__":
    main()
