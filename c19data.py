import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

## Initialize Dash app
app = dash.Dash(__name__, assets_folder='assets')
server = app.server
 

## TODO - put this data in a separate file to reduce code complexity/density?
## TODO - if stored locally, add API to update the population?
us_state_dict = { 
    '0': {  'population': 4932000, 'short_name': "AL" , 'long_name': 'Alabama', 'file': 'alabama-history.csv' },
    '1': {  'population': 728903, 'short_name': "AK" , 'long_name': 'Alaska', 'file': 'alaska-history.csv' },
    '2': {  'population': 7278717, 'short_name': "AZ" , 'long_name': 'Arizona', 'file': 'arizona-history.csv' },
    '3': {  'population': 3017825, 'short_name': "AR" , 'long_name': 'Arkansas', 'file': 'arkansas-history.csv' },
    '4': {  'population': 39512223, 'short_name': "CA" , 'long_name': 'California', 'file': 'california-history.csv' },
    '5': {  'population': 5758736, 'short_name': "CO" , 'long_name': 'Colorado', 'file': 'colorado-history.csv' },
    '6': {  'population': 3565287, 'short_name': "CT" , 'long_name': 'Connecticut', 'file': 'connecticut-history.csv' },
    '7': {  'population': 973764, 'short_name': "DE" , 'long_name': 'Delaware', 'file': 'delaware-history.csv' },
    '8': {  'population': 705749, 'short_name': "DC" , 'long_name': 'District of Columbia', 'file': 'district-of-columbia-history.csv' },
    '9': {  'population': 21477737, 'short_name': "FL" , 'long_name': 'Florida', 'file': 'florida-history.csv' },
    '10': {  'population': 10617423, 'short_name': "GA" , 'long_name': 'Georgia', 'file': 'georgia-history.csv' },
    '12': {  'population': 1415872, 'short_name': "HI", 'long_name': 'Hawaii', 'file': 'hawaii-history.csv' },
    '13': {  'population': 1787065, 'short_name': "ID", 'long_name': 'Idaho', 'file': 'idaho-history.csv' },
    '14': {  'population': 12671821, 'short_name': "IL", 'long_name': 'Illinois', 'file': 'illinois-history.csv' },
    '15': {  'population': 6732219, 'short_name': "IN", 'long_name': 'Indiana', 'file': 'indiana-history.csv' },
    '16': {  'population': 3155070, 'short_name': "IA", 'long_name': 'Iowa', 'file': 'iowa-history.csv' },
    '17': {  'population': 2913314, 'short_name': "KS", 'long_name': 'Kansas', 'file': 'kansas-history.csv' },
    '18': {  'population': 4467673, 'short_name': "KY", 'long_name': 'Kentucky', 'file': 'kentucky-history.csv' },
    '19': {  'population': 4648794, 'short_name': "LA", 'long_name': 'Louisiana', 'file': 'louisiana-history.csv' },
    '20': {  'population': 1344212, 'short_name': "ME", 'long_name': 'Maine', 'file': 'maine-history.csv' },
    '21': {  'population': 6045680, 'short_name': "MD", 'long_name': 'Maryland', 'file': 'maryland-history.csv' },
    '22': {  'population': 6949503, 'short_name': "MA", 'long_name': 'Massachusetts', 'file': 'massachusetts-history.csv' },
    '23': {  'population': 9986857, 'short_name': "MI", 'long_name': 'Michigan', 'file': 'michigan-history.csv' },
    '24': {  'population': 5639632, 'short_name': "MN", 'long_name': 'Minnesota', 'file': 'minnesota-history.csv' },
    '25': {  'population': 2976149, 'short_name': "MS", 'long_name': 'Mississippi', 'file': 'mississippi-history.csv' },
    '26': {  'population': 6137428, 'short_name': "MO", 'long_name': 'Missouri', 'file': 'missouri-history.csv' },
    '27': {  'population': 1068778, 'short_name': "MT", 'long_name': 'Montana', 'file': 'montana-history.csv' },
    '28': {  'population': 1934408, 'short_name': "NE", 'long_name': 'Nebraska', 'file': 'nebraska-history.csv' },
    '29': {  'population': 3080156, 'short_name': "NV", 'long_name': 'Nevada', 'file': 'nevada-history.csv' },
    '30': {  'population': 1359711, 'short_name': "NH", 'long_name': 'New Hampshire', 'file': 'new-hampshire-history.csv' },
    '31': {  'population': 8882190, 'short_name': "NJ", 'long_name': 'New Jersey', 'file': 'new-jersey-history.csv' },
    '32': {  'population': 2096829, 'short_name': "NM", 'long_name': 'New Mexico', 'file': 'new-mexico-history.csv' },
    '33': {  'population': 19453561, 'short_name': "NY", 'long_name': 'New York', 'file': 'new-york-history.csv' },
    '34': {  'population': 10488084, 'short_name': "NC", 'long_name': 'North Carolina', 'file': 'north-carolina-history.csv' },
    '35': {  'population': 762062, 'short_name': "ND", 'long_name': 'North Dakota', 'file': 'north-dakota-history.csv' },
    '36': {  'population': 55194, 'short_name': "NI", 'long_name': 'Northern Mariana Islands', 'file': 'northern-mariana-islands-history.csv' },
    '37': {  'population': 11689100, 'short_name': "OH", 'long_name': 'Ohio', 'file': 'ohio-history.csv' },
    '38': {  'population': 3956971, 'short_name': "OK", 'long_name': 'Oklahoma', 'file': 'oklahoma-history.csv' },
    '39': {  'population': 4217737, 'short_name': "OR", 'long_name': 'Oregon', 'file': 'oregon-history.csv' },
    '40': {  'population': 12801989, 'short_name': "PA", 'long_name': 'Pennsylvania', 'file': 'pennsylvania-history.csv' },
    '41': {  'population': 3193694, 'short_name': "PR", 'long_name': 'Puerto Rico', 'file': 'puerto-rico-history.csv' },
    '42': {  'population': 1059361, 'short_name': "RI", 'long_name': 'Rhode Island', 'file': 'rhode-island-history.csv' },
    '43': {  'population': 5148714, 'short_name': "SC", 'long_name': 'South Carolina', 'file': 'south-carolina-history.csv' },
    '44': {  'population': 884659, 'short_name': "SD", 'long_name': 'South Dakota', 'file': 'south-dakota-history.csv' },
    '45': {  'population': 6833174, 'short_name': "TN", 'long_name': 'Tennessee', 'file': 'tennessee-history.csv' },
    '46': {  'population': 28995881, 'short_name': "TX", 'long_name': 'Texas', 'file': 'texas-history.csv' },
    '47': {  'population': 3205958, 'short_name': "UT", 'long_name': 'Utah', 'file': 'utah-history.csv' },
    '48': {  'population': 623989, 'short_name': "VT", 'long_name': 'Vermont', 'file': 'vermont-history.csv' },
    '49': {  'population': 8535519, 'short_name': "VA", 'long_name': 'Virginia', 'file': 'virginia-history.csv' },
    '50': {  'population': 104914, 'short_name': "VI", 'long_name': 'Virgin Islands', 'file': 'us-virgin-islands-history.csv' },
    '51': {  'population': 7614893, 'short_name': "WA", 'long_name': 'Washington', 'file': 'washington-history.csv' },
    '52': {  'population': 1792147, 'short_name': "WV", 'long_name': 'West Virginia', 'file': 'west-virginia-history.csv' },
    '53': {  'population': 5822434, 'short_name': "WI", 'long_name': 'Wisconsin', 'file': 'wisconsin-history.csv' },
    '54': {  'population': 578759, 'short_name': "WY", 'long_name': 'Wyoming', 'file': 'wyoming-history.csv' },
}
## TODO - include total population into above dict? Have it as item zero?
total_us_population = 331814684
us_stats_dict = {
    'population': 331814684, 'short_name': "US", 'long_name': 'United States of America', 'file': 'national-history.csv'
}


app.layout = html.Div(children=[
    html.Div(children=[
        html.H1(children='COVID Dashboard'),
        html.H2(children="Visualize latest and historical US COVID data."),
    ], id="header", style={'border-bottom': 'thin solid black', 'margin-bottom': '30px'}),

    html.H3(children="Nation-wide statistics"),




], className="main-container")




if __name__ == '__main__':
    app.run_server(debug=True)