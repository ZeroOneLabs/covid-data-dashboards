import os

import pandas as pd
from pandas import DataFrame

# import dash
# import dash_core_components as dcc
# import dash_html_components as html
# from dash.dependencies import Input, Output
# import plotly.express as px

import jh_data_downloader as jhd



if not os.path.exists(jhd.JHD_YESTERDAY_FILE):
    jhd.download_johnshopkins_data()


df_jhdata = pd.read_csv(jhd.JHD_YESTERDAY_FILE)

# print(df_jhdata.columns)


## Trim the dataframe to rows that include items within the US
df_us_jhdata = df_jhdata.loc[df_jhdata["Country_Region"] == "US"]



def get_stat(city: str, state: str) -> DataFrame:
    return df_us_jhdata.loc[(df_us_jhdata["Admin2"] == city) & (df_us_jhdata["Province_State"] == state)]

def get_field_val(df: DataFrame, field: str):
    return df[field].values[0]


# stats = get_stat(city="Salt Lake", state="Utah")
# print(get_field_val(stats, "FIPS"))

citydata = pd.read_json(os.path.join(jhd.JHD_BASE_DIR, "data/us-city-population-2019-v2.json"))

count = 0
for city in citydata:
    cityname = citydata[city]["city"].strip(' City') #The Johns Hopkins data does not include " City" in city names like "New York City" or "Salt Lake City"
    citystate = citydata[city]["state"]
    city_stat = get_stat(cityname, citystate)
    # fips_val = get_field_val(city_stat, "FIPS")
    cases_val = get_field_val(city_stat, "Confirmed")
    deaths_val = get_field_val(city_stat, "Deaths")
    recovered_val = get_field_val(city_stat, "Recovered")
    mortality_rate = (deaths_val / cases_val) * 100

    city_pop = citydata[city]["pop"]
    city_density = citydata[city]["pop_dense_sqmi"]

    print(f"{cityname}, {citystate}, Mortality Rate: {mortality_rate}")
    count += 1
    if count == 50:
        break


