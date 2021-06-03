import pandas as pd
import json
import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_table.FormatTemplate as FormatTemplate
from dash_table.Format import Format, Scheme, Symbol, Group
import plotly.express as px


# exit("Don't run this without reformatting the JSON output.")

df = pd.read_csv("data/us-counties-latest.csv")

def lookup_county_stat(dataframe: pd.DataFrame, city: str, cat: str):
    stat = dataframe.loc[(df["county"] == city)][cat].iloc[0]
    return stat

# deaths = lookup_county_stat(df, "Los Angeles", "deaths")
# Date,State,Cases_Total,Cases_White,Cases_Black,Cases_Latinx,Cases_Asian,Cases_AIAN,Cases_NHPI,Cases_Multiracial,Cases_Other,Cases_Unknown,Cases_Ethnicity_Hispanic,Cases_Ethnicity_NonHispanic,Cases_Ethnicity_Unknown,Deaths_Total,Deaths_White,Deaths_Black,Deaths_Latinx,Deaths_Asian,Deaths_AIAN,Deaths_NHPI,Deaths_Multiracial,Deaths_Other,Deaths_Unknown,Deaths_Ethnicity_Hispanic,Deaths_Ethnicity_NonHispanic,Deaths_Ethnicity_Unknown,Hosp_Total,Hosp_White,Hosp_Black,Hosp_Latinx,Hosp_Asian,Hosp_AIAN,Hosp_NHPI,Hosp_Multiracial,Hosp_Other,Hosp_Unknown,Hosp_Ethnicity_Hispanic,Hosp_Ethnicity_NonHispanic,Hosp_Ethnicity_Unknown,Tests_Total,Tests_White,Tests_Black,Tests_Latinx,Tests_Asian,Tests_AIAN,Tests_NHPI,Tests_Multiracial,Tests_Other,Tests_Unknown,Tests_Ethnicity_Hispanic,Tests_Ethnicity_NonHispanic,Tests_Ethnicity_Unknown

race_demo = pd.read_csv("data/covidtracking.com/racial-demo-complete-latest.csv")
citypop = pd.read_json("data/us-city-population-2019-v2.json")
county_stats = pd.read_csv("data/us-counties-latest.csv")

app = dash.Dash(__name__)

master_list = []
for item in citypop:
    rank = int(item + 1)
    name = citypop[item]["city"]
    state = citypop[item]["state"]
    pop = citypop[item]["pop"]
    counties = citypop[item]["counties"]
    popdense_sqmi = citypop[item]["pop_dense_sqmi"]
    popdense_sqkm = citypop[item]["pop_dense_sqkm"]
    deaths: int = 0
    cases: int = 0
    for county in counties:
        deaths += int(county_stats.loc[(county_stats['county'] == county) & (county_stats['state'] == state), ["deaths"]].values[0][0])
        cases += int(county_stats.loc[(county_stats['county'] == county) & (county_stats['state'] == state), ["cases"]].values[0][0])
    if cases == 0:
        cases = 1
    mortality_rate = round((deaths / cases) * 100, 3)
    case_rate = round((cases / pop) * 100, 3)
    survival_rate = round((100 - mortality_rate), 2)
    master_list.append({
        # "population rank": rank,
        "name": name,
        "state": state.replace('District of Columbia', 'D.C.'),
        "population": int(pop),
        # "counties **": str(' | '.join(map(str, counties))),
        "popdense_sqmi": int(popdense_sqmi),
        # "popdense_sqkm": popdense_sqkm,
        "deaths": int(deaths),
        "cases": int(cases),
        "mortality_rate": float(mortality_rate),
        "case_rate": float(case_rate),
        # "survival_rate": survival_rate,
        # "adv_senior_mortality": "",
        # "senior_mortality": "",
        # "adv_adult_mortality": "",
        # "adult_mortality": "",
        # "young_adult_mortality": "",
        # "youth_mortality": "",
        # "child_mortality": ""
    })
    if item == 99:
        break
format_percentage = Format()
format_percentage = format_percentage.symbol(Symbol.yes).symbol_suffix('%')
format_number = Format()
format_number = {'locale': {}, 'nully': '', 'prefix': None, 'specifier': ','}

output_df = pd.DataFrame(master_list)
output_df = output_df.sort_values(by='mortality_rate', ascending=False)
# output_df.to_csv("/Users/zan/Desktop/2021-05-22_COVID-mortality-rates.csv")

style_description_div = {
    # "backgroundColor":"#fff",
    # "padding": "0.4em",
    "margin": "0 0 1em 0",
    "width": "80%",
    "fontSize": "1.2em"
    }

columns = [
    dict(id='name', name='City'),
    dict(id='state', name='State'),
    dict(id='population', name='Population *', type='numeric', format=format_number),
    dict(id='deaths', name='Deaths', type='numeric', format=format_number),
    dict(id='cases', name='Cases', type='numeric', format=format_number),
    dict(id='mortality_rate', name='M Rate', format=format_percentage),
    dict(id='case_rate', name='C Rate', format=format_percentage)
]

app.layout = html.Div(children=[
    html.Div(id="container", className="header", children=[
        html.Div(id="header", className="header", children=[
            html.Div(children=[
                html.H1(children="COVID statistics per the top 100 populated US Cities")
            ],style={
                "marginBottom": "100px"
            }),
            html.Div(className="description-div", children=[
                html.H2(children="COVID statistics table"),
                html.Div(children="The table below is sorted by Mortality Rate (most-to-least severe). The table has fields beneath each column which can be used to filter values. For example, under the 'state' column label you can filter for all the cities within California by typing 'California' in the filter field and pressing the return key. You can change how each column is sorted by clicking the up/down arrows in their respective column.", style=style_description_div),
            ])

        ]),

        html.Div(children=[
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=columns,
            data=output_df.to_dict('records'),
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="single",
            column_selectable=False,
            row_selectable=False,
            row_deletable=False,
            page_action="native",
            page_current=0,
            page_size=10,
            style_table={
                'fontSize': '1.5em',
                "fontFamily": "monospace"
            },
            style_header={
                # 'fontSize': '1.2em',
                'textAlign': 'center'
            },
            style_cell={
                'height': "2.5em",
                'paddingRight': "0.4em"
            }

        )], className="dataTable", 
        style={
            "border": "thin black solid",
            "paddingLeft": "1px"
        }),

        html.Div(id='datatable-interactivity-container'),

        html.H2(children="Table Key"),
        html.Div(children=[
            dcc.Markdown('''
                **City** - Name of city.

                **State** - The name of the State, province, or district.

                **Population** - The estimated population number from the 2019 census. Most population numbers were sourced from either New York Times COVID GitHub data repository, Johns Hopkins COVID GitHub data repository, or Wikipedia.

                **Deaths** *  - The number of confirmed COVID-19 deaths.

                **Cases** * - The number of confirmed COVID-19 cases.

                **M Rate (Mortality Rate)** - Mortality rate, which is calculated by the CDC's formula definition of `(cases / deaths) * 100`.

                **C Rate (Case Rate)** - Case rate shows the population of the city that's estimated to have contracted COVID.


                *Some cities have multiple districts listed under the GitHub repository from the New York Times. Each city's statistics with multiple counties were concatonated and compared with other authoritative sources to support confidence in those numbers.
            ''')
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
    app.run_server(debug=True,host=os.getenv('HOST','192.168.1.20'))