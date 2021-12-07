import json
import os
import pandas as pd
from datetime import datetime

import data_downloader as dd

def write_data():

    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")

    cdc_file_names = {
        "Deaths_by_Race_and_Hispanic_Origin": "https://data.cdc.gov/resource/pj7m-y5uh.json",
        "Deaths_by_Sex_and_Age": "https://data.cdc.gov/resource/vsak-wrfu.json"
    }


    if not os.path.exists(f"data/CDC/{today_str}-Deaths_by_Race_and_Hispanic_Origin.json") or \
        not os.path.exists(f"data/CDC/{today_str}-Deaths_by_Sex_and_Age.json"):
        dd.download_cdc_data()


    ## TODO:
    #
    # * Write files per state
    # * Write files per age demo
    # * Write files per race demo
    # * Ditch NYT data and use only the CDC's data?


    ## TODO: Use os module to do logical .exists() checks?
    race_demo_df = pd.read_json(f"data/CDC/{today_str}-Deaths_by_Race_and_Hispanic_Origin.json").fillna(0)
    race_demo_df = race_demo_df.loc[(race_demo_df["start_week"] == "2020-01-01T00:00:00.000") & (race_demo_df["group"] == "By Total") & (race_demo_df["indicator"] == "Count of COVID-19 deaths")]
    age_demo_df = pd.read_json(f"data/CDC/{today_str}-Deaths_by_Sex_and_Age.json").fillna(0)
    states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")

    ## NOTE: For some reason Pandas wasn't iterating through a json dataframe the same way Python iterates natively over json. Weird.
    ## Edit - update: I found out that when I was iterating through a Pandas DataFrame, I needed to cite the .values[0] method to get the values.
    # state_age_info_df = pd.read_json("data/state_info.json")

    with open("data/state_info.json") as j:
        state_age_info_df = json.load(j)

    demo_age = [ "Under 1 year", "0-17 years", "1-4 years", "5-14 years", "15-24 years", "18-29 years", "25-34 years", "30-39 years", "35-44 years", "40-49 years", "45-54 years", "50-64 years", "55-64 years", "65-74 years", "75-84 years", "85 years and over" ]
    demo_sex = [ "Male", "Female" ]
    demo_races = { "Black": "non_hispanic_black_african_american", "White": "non_hispanic_white", "Latino": "hispanic_latino_total", "Asian": "non_hispanic_asian_pacific_islander", "Multiracial": "non_hispanic_more_than_one_race", "Indian_Alaskan": "non_hispanic_american_indian_alaska_native", "Islander": "nh_nhopi" }


    parent_dict = { }
    for st, state in state_age_info_df["states"].items():
        state_name = state["long"]
        if state_name == "Northern Mariana Islands" or state_name == "Virgin Islands" or state_name == "Puerto Rico":
            continue

        # Get total cases and deaths for that state
        state_cases = states_totals_df.loc[(states_totals_df["state"] == state_name)]["cases"].values[0]
        state_death = states_totals_df.loc[(states_totals_df["state"] == state_name)]["deaths"].values[0]

        # INIT new state_dict
        state_dict = { state_name : { "Age": {}, "Race": {} } }

        try:
            state_age_info_df = age_demo_df.loc[(age_demo_df["state"] == state_name)]
            # print(f"Found {state_name}")
        except:
            # print(f"Couldn't find {state_name}")
            continue

        ## Process age demographics
        for age in demo_age:
            age_all_sex = state_age_info_df.loc[(state_age_info_df["age_group"] == age)].fillna(0)

            try:
                age_all_sex_death = age_all_sex["covid_19_deaths"].values[0]
                age_all_sex_death += age_all_sex["pneumonia_influenza_or_covid"].values[0]
                age_all_sex_death += age_all_sex["pneumonia_and_covid_19_deaths"].values[0]
            except:
                age_all_sex_death = 0


            age_mortality_rate = round((age_all_sex_death / state_cases) * 100, 2)
            age_pct_of_covid_deaths = round((age_all_sex_death / state_death) * 100, 2)

            if age not in state_dict[state_name]["Age"]:
                state_dict[state_name]["Age"][age] = {}

            state_dict[state_name]["Age"][age]["m_rate"] = age_mortality_rate
            state_dict[state_name]["Age"][age]["pct_covid_deaths"] = age_pct_of_covid_deaths
            state_dict[state_name]["Age"][age]["total_deaths"] = age_all_sex_death

        parent_dict[state_name] = state_dict[state_name]

        try:
            race_death = race_demo_df.loc[race_demo_df["state"] == state_name]
        except:
            print("Error getting race_death: ")
            continue


        race_dict = {}
        for race, desc in demo_races.items():

            try:
                race_death = race_demo_df.loc[race_demo_df["state"] == state_name][desc].values[0]
                race_pct_of_covid_deaths = round((race_death / state_death) * 100, 2)
                if race not in race_dict:
                    race_dict[race] = {}
            except:
                continue

            race_dict[race]["death"] = race_death
            race_dict[race]["pct_covid_deaths"] = race_pct_of_covid_deaths


        parent_dict[state_name]["Race"] = race_dict
        # break

    ## TODO: Write function to load this data into a variable from an import/external reference clause.
    # print(parent_dict)
    with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "w") as d:
        json.dump(parent_dict, d)


if __name__ == "__main__":
    write_data()