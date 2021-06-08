import json
import pandas as pd
from datetime import datetime

def write_data():

    today = datetime.today()
    today_str = today.strftime("%Y-%m-%d")

    ## TODO: Use os module to do logical .exists() checks?
    race_demo_df = pd.read_csv("data/CDC/Provisional_COVID-19_Deaths__Distribution_of_Deaths_by_Race_and_Hispanic_Origin.csv", header=0).fillna(0)
    race_demo_df = race_demo_df.loc[(race_demo_df["Start Date"] == "01/01/2020") & (race_demo_df["Group"] == "By Total") & (race_demo_df["Indicator"] == "Count of COVID-19 deaths")]
    age_demo_df = pd.read_csv("data/CDC/Provisional_COVID-19_Deaths_by_Sex_and_Age.csv", header=0).fillna(0)
    states_totals_df = pd.read_csv("data/NYT/us-states-latest.csv")

    ## NOTE: For some reason Pandas wasn't iterating through a json dataframe the same way Python iterates natively over json. Weird.
    # state_age_info_df = pd.read_json("data/state_info.json")

    with open("data/state_info.json") as j:
        state_age_info_df = json.load(j)

    demo_age = [ "Under 1 year", "0-17 years", "1-4 years", "5-14 years", "15-24 years", "18-29 years", "25-34 years", "30-39 years", "35-44 years", "40-49 years", "45-54 years", "50-64 years", "55-64 years", "65-74 years", "75-84 years", "85 years and over" ]
    demo_sex = [ "Male", "Female" ]
    demo_races = { "Black": "Non-Hispanic Black or African American", "White": "Non-Hispanic White", "Latino": "Hispanic or Latino", "Asian": "Non-Hispanic Asian", "Multiracial": "Non Hispanic more than one race", "Indian_Alaskan": "Non-Hispanic American Indian or Alaska Native", "Islander": "Non-Hispanic Native Hawaiian or Other Pacific Islander" }

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
            state_age_info_df = age_demo_df.loc[(age_demo_df["State"] == state_name) & (age_demo_df["Start Date"] == "01/01/2020") & (age_demo_df["End Date"] == "05/22/2021") & (age_demo_df["Group"] == "By Total")]
        except:
            continue

        for age in demo_age:
            age_all_sex = state_age_info_df.loc[(state_age_info_df["Age Group"] == age) & (state_age_info_df["Sex"] == "All Sexes")].fillna(0)

            try:
                age_all_sex_death = age_all_sex["COVID-19 Deaths"].values[0]
            except:
                age_all_sex_death = age_all_sex["COVID-19 Deaths"]


            age_mortality_rate = round((age_all_sex_death / state_cases) * 100, 2)
            age_pct_of_covid_deaths = round((age_all_sex_death / state_death) * 100, 2)

            if age not in state_dict[state_name]["Age"]:
                state_dict[state_name]["Age"][age] = {}

            state_dict[state_name]["Age"][age]["m_rate"] = age_mortality_rate
            state_dict[state_name]["Age"][age]["pct_covid_deaths"] = age_pct_of_covid_deaths
            state_dict[state_name]["Age"][age]["total_deaths"] = age_all_sex_death

        parent_dict[state_name] = state_dict[state_name]

        try:
            race_death = race_demo_df.loc[race_demo_df["State"] == state_name]
        except:
            continue


        race_dict = {}
        for race, desc in demo_races.items():

            try:
                race_death = race_demo_df.loc[race_demo_df["State"] == state_name][desc].values[0]
                race_pct_of_covid_deaths = round((race_death / state_death) * 100, 2)
                if race not in race_dict:
                    race_dict[race] = {}
            except:
                continue

            race_dict[race]["death"] = race_death
            race_dict[race]["pct_covid_deaths"] = race_pct_of_covid_deaths


        parent_dict[state_name]["Race"] = race_dict 

    ## TODO: Write function to load this data into a variable from an import/external reference clause.

    with open("data/ZeroOneLabs/" + today_str + "_demo_data.json", "w") as d:
        json.dump(parent_dict, d)


if __name__ == "__main__":
    write_data()