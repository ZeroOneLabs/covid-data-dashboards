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

with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "r") as f:
    state_file = json.load(f)

# for state, data in state_file.items():
#     print(state, data)
    # for age_demo in data["Age"]:
    #     print(age_demo)
    #     break
    # break
# exit()

app = dash.Dash(__name__)


states_data_list = []
count = 0
# Run main loop to print out graphs for each state
for state, data in state_file.items():
    state_list = []
    # print(state, data)
    
    state_id_str = state.replace(" ", "-").lower()

    # age_df = pd.DataFrame(data["Age"])
    age_demo_death_dict = { "Age Group": [], "COVID Deaths": [] }
    for age_demo in data["Age"]:
        age_demo_death_dict["Age Group"].append(age_demo)
        age_demo_death_dict["COVID Deaths"].append(data["Age"][age_demo]["total_deaths"])
    
    age_demo_death_pct_dict = { "Age Group": [], "Percent of Deaths": [] }
    for age_demo in data["Age"]:
        age_demo_death_pct_dict["Age Group"].append(age_demo)
        age_demo_death_pct_dict["Percent of Deaths"].append(data["Age"][age_demo]["pct_covid_deaths"])
    
    age_death_df = pd.DataFrame(age_demo_death_dict, columns=["Age Group", "COVID Deaths"])
    
    death_bar = px.bar(age_death_df, x="COVID Deaths", y="Age Group", orientation='h', barmode="group", title="Deaths by Age")
    death_pie = fig = px.pie(age_demo_death_pct_dict, values='Percent of Deaths', names='Age Group', title='Percent of COVID deaths', color_discrete_sequence=px.colors.diverging.Geyser_r)
    death_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    states_data_list.append(html.H2(children=state))
    
    # states_data_list.append(html.H3(children="Deaths by Age"))
    states_data_list.append(html.Div([
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-bar',className="state-figure-bar",figure=death_bar)], className="bar-chart"), 
            html.Div([dcc.Graph(id=state_id_str + '-deaths-per-age-pie',className="state-figure-pie",figure=death_pie)], className="pie-chart")
        ], className="row"))
    # states_data_list.append(html.Div([)], style="width: 48%"))



    # states_data_list.append(state_list)
    # count += 1
    # if count == 5:
    #     break
    # break
# print(age_demo_death_dict)
# exit()
# H2 - State name
    # html.H2(children=state_name)
# DIV - Basic stats; total cases, deaths, averate mortality rate for entire duration of pandemic.

# Graphs
    # Age graph
    # Race graph
    # key that explains mortality rate is relative to total cases per state, not demographic. Call it "Total relative mortality rate"?



app.layout = html.Div(children=[
    html.Div(id="container", className="header", children=[
        html.Div(id="header", className="header", children=[
            html.Div(children=[
                html.H1(children="COVID demographic statistics US State by age and race")
            ],style={
                "marginBottom": "100px"
            })
        ]),

        html.Div(children=states_data_list),


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


# print(json.dumps(parent_dict))
