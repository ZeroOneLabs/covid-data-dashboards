import pandas as pd
import plotly.express as px

import dash_html_components as html
import dash_core_components as dcc
import dash_table

import shared_data as sd
import dashboard_utils as du

def get_national_stats(
        us_percent_infected, 
        us_percent_killed, 
        us_totals_mrate, 
        us_totals_mrate_noseniors,
        national_total_pct_age_table_dict,
        us_totals_cases, us_totals_death) -> list:

    retval = [

        html.H2("National Statistics", className="main-header"),

        html.P(className="spacer"),
        html.P(className="spacer"),

        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td("Total Cases"),
                    html.Td(f"{us_totals_cases:,}", className="nat-stat-num")
                ]),
                html.Tr([
                    html.Td("Total Deaths"),
                    html.Td(f"{us_totals_death:,}", className="nat-stat-num")
                ])
            ])
        ], className="stat-table table table-responsive"),
        html.P(className="spacer"),

        html.Table([
            html.Tbody([
                html.Tr([
                    html.Td("US Population % infected"),
                    html.Td(f"{us_percent_infected:,}%", className="nat-stat-num")
                ]),
                html.Tr([
                    html.Td("US Population % deaths"),
                    html.Td(f"{us_percent_killed:,}%", className="nat-stat-num")
                ])
            ])
        ], className="stat-table table table-responsive"),
        html.P(className="spacer"),
        html.P(className="spacer"),

        html.H4("Mortality Rates", className="main-subheader"),
        # html.P("Percent of COVID deaths by age group", className="main-domsubheader"),
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

        html.H4("Age Statistics", className="main-subheader"),
        html.P("Percent of COVID deaths by age group", className="main-domsubheader"),
        html.P(className="spacer"),

        # Haha! Fuck YOU! I created a method to create tables programmatically!
        du.create_html_table(national_total_pct_age_table_dict, tableClassname="stat-table table table-responsive"),

        dcc.Markdown(
            f"""
            Regarding the average State, 'advanced adults' (45-64 years) and Seniors (65+) make up about 75% of COVID deaths. Inversely, **the average survival rate for COVID is {100 - us_totals_mrate}%,** and the average survival rate for people under 64 years of age is {100 - us_totals_mrate_noseniors}%.
            """),

        html.P("** Senior (65 yrs+) deaths & cases removed from pool of calculated data, leaving ages from 0 to 64."),
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
        html.H3("About this COVID-19 Dashboard", className="main-subheader"),
        html.P(className="spacer"),

        dcc.Markdown('''
        This dashboard was created out of necessity, when I asked myself the question "What age group makes up the majority of COVID deaths for my state?" and "most dashboards list cases with 'rolling averages' or 'last 7 days', but no deaths? How lethal is this disease if I can't measure the cases against the deaths?" 
        '''),

        dcc.Markdown('''
        This lead me down a path of trying to find a complete set of data that I could download for my state, which then lead me to find more data for each state... which then lead me down the path to finding COVID data about age ranges and race groups.

        The ultimate purpose of this dashboard is to help people like you empower yourselves with simple, yet effective knowledge that comes from the New York Times and the CDC. I want to help educate people on generally how deadly the COVID-19 disease in the United States by pulling official data and calculating those numbers to get a mortality rate – or rather the relative chances one would have if they contracted COVID in a certain geographical area in the United States.

        &nbsp;

        If you are viewing this data dashboard on a tablet or mobile device, I would advise you to turn your device into "landscape mode" in order to see the graphs and text a little better, or to view this on a desktop web browser.
        ''', id="purpose-div"),

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

        ], className="state-picker-row")
    ]
    return retval


def build_state_graphs(json_state_file, state) -> list:
    state_info_data_list = []
    state_id_str = state.replace(" ", "-").lower()
    data = json_state_file[state]
# us_totals_cases, us_totals_death
    bar_legend_font_config = dict(family="Helvetica", size=18, color="Black")


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


    ## Grouped age statistics for percentage of COVID deaths - e.g. "Child (0-14), Teen/Adult (15-44), Adult (45-64), Senior (65-85+)"
    grouped_age_demo_death_pct_dict = { "Age Group": [ "Child", "Teen/Adult", "Adv Adult", "Senior" ], "Percent of Deaths": [] }
    # Define variables
    child_death_pct, teenadult_death_pct, adult_death_pct, senior_death_pct = 0.0, 0.0, 0.0, 0.0

    for age_demo in data["Age"]:
        # These group of data collects more deaths and skews the visual representation in the graphs and pie charts.
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

    ## Create dataframe for bar graphs
    grouped_age_death_bar_df = pd.DataFrame(grouped_age_demo_deaths_dict, columns=["Age Group", "COVID Deaths"])


    # previous color settings: , color_continuous_scale="Geyser", color="COVID Deaths"
    age_death_bar_df = pd.DataFrame(age_demo_death_dict, columns=["Age Range", "COVID Deaths"])
    age_death_bar = px.bar(age_death_bar_df, x="COVID Deaths", y="Age Range", orientation='h', title="Deaths by Age")
    age_death_bar.update_yaxes(title=None)
    age_death_bar.update_xaxes(title=None)
    age_death_bar.update_layout( font=bar_legend_font_config, margin=sd.bar_graph_margins )
    age_death_bar.update_traces( texttemplate='%{x:,}', textposition='auto' )

    # previous color settings: color_continuous_scale=bar_color_scale, color="COVID Deaths"
    grouped_age_death_bar = px.bar(grouped_age_death_bar_df, x="COVID Deaths", y="Age Group", orientation='h', barmode="group", title="Deaths by Age (Grouped)")
    grouped_age_death_bar.update_yaxes( title=None )
    grouped_age_death_bar.update_xaxes( title=None )
    grouped_age_death_bar.update_layout( font=bar_legend_font_config, margin=sd.bar_graph_margins )
    grouped_age_death_bar.update_traces( texttemplate='%{x:,}', textposition='auto' )

    ## Create pie graphs
    # previous color settings: color_discrete_sequence=["red", "green", "blue"]
    age_death_pie = px.pie( age_demo_death_pct_dict, values='Percent of Deaths', names='Age Range', title='Percent of COVID deaths' )
    age_death_pie.update_traces( textposition='inside', textinfo='percent+label', showlegend=False )
    age_death_pie.update_layout( font=sd.pie_legend_font_config, title=None, margin=sd.pie_graph_margins )

    # previous color settings: color_discrete_sequence=px.colors.diverging.Geyser_r
    grouped_age_death_pie = px.pie( grouped_age_demo_death_pct_dict, values='Percent of Deaths', names='Age Group', title='Percent of COVID deaths (Grouped)' )
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
    race_death_bar = px.bar(race_death_bar_df, x="COVID Deaths", y="Race Group", orientation='h', barmode="group", title="All Races")
    race_death_bar.update_layout( font=sd.pie_legend_font_config)
    race_death_bar.update_yaxes(title=None)
    race_death_bar.update_xaxes(title=None)
    race_death_bar.update_layout( font=bar_legend_font_config, margin=sd.bar_graph_margins )
    race_death_bar.update_traces( texttemplate='%{x:,}', textposition='auto' )


    ## Create pie graph
    race_death_pie = fig = px.pie(race_demo_death_pct_dict, values='Percent of Deaths', names='Race Group', title=f'{state} - Race Demographics - % COVID deaths', color_discrete_sequence=px.colors.diverging.Tealrose_r)
    race_death_pie.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    race_death_pie.update_layout( font=sd.pie_legend_font_config, title=None, margin=sd.pie_graph_margins )


    state_cases = sd.states_totals_df.loc[sd.states_totals_df["state"] == state]["cases"].values[0]
    state_death = sd.states_totals_df.loc[sd.states_totals_df["state"] == state]["deaths"].values[0]
    state_mrate = round((state_death / state_cases) * 100, 3)
    state_mrate_noseniors = round(((state_death - senior_deaths)/ state_cases) * 100, 3)


    state_info_data_list.append(
        html.Div([

            html.H2(state, className="main-header"),

            html.P(className="spacer"),
            html.P(className="spacer"),
        
            html.Table([
                html.Tbody([
                    html.Tr([
                        html.Td("Cases", className="state-stat-title"),
                        html.Td(f"{state_cases:,}", className="state-stat-num")
                    ]),
                    html.Tr([
                        html.Td("Deaths", className="state-stat-title"),
                        html.Td(f"{state_death:,}", className="state-stat-num")
                    ])
                ])
            ], className="stat-table table table-responsive"),

            html.P(className="spacer"),

            html.H4("Mortality Rates", className="main-subheader"),
            html.P(className="spacer"),

                html.Table([
                    html.Tbody([
                        html.Tr([
                            html.Td(f"Average mortality rate for {state}", className="state-stat-title"),
                            html.Td(f"{state_mrate:,}%", className="state-stat-num")
                        ]),
                        html.Tr([
                            html.Td(f"{state} Seniors Removed **", className="state-stat-title"),
                            html.Td(f"{state_mrate_noseniors:,}%", className="state-stat-num")
                        ])
                    ])
                ], className="stat-table table table-responsive"),

            html.P(className="spacer"),
            html.P(className="spacer"),

            html.H4("Age Statistics", className="main-subheader"),
            html.P("Note: One or more data groups (age/race) have counts between 1-9 and have been suppressed in accordance with NCHS confidentiality standards."),
            html.Ul([
                html.Li("Children: 0-14"),
                html.Li("Teen/Adult: 15-44"),
                html.Li("Adv Adult: 45-64"),
                html.Li("Senior: 65 +"),
            ]),

            html.P(className="spacer"),

            html.Div([
                html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-bar-grouped',className="state-figure-bar",figure=age_death_bar)], className="bar chart"), 
                html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-pie-grouped',className="state-figure-pie",figure=grouped_age_death_pie)], className="pie chart")
            ], className="row"),

            html.P(className="spacer"),
            html.P(className="spacer"),

            html.H4("Race Statistics", className="main-subheader"),
            html.P(className="spacer"),


            html.Div([
                html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-bar',className="state-figure-bar",figure=race_death_bar)], className="bar chart"), 
                html.Div([dcc.Graph(id=state_id_str + '-deaths-per-race-pie',className="state-figure-pie",figure=race_death_pie)], className="pie chart")
            ], className="row"),
        ])    
    )


    return state_info_data_list



def main():
    pass

if __name__ == "__main__":
    main()