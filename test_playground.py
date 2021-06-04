import json
import pandas as pd

# import c19_data_downloader as cdd
# nyc_data_dict = {
#     "totals": {
#         "deaths_by_race_age": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/deaths-by-race-age.csv",
#         "cases_by_poverty": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/antibody-by-poverty.csv",
#         "deaths_by_conditions": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/deaths-by-underlying-conditions.csv"
#     },
#     "latest": {
#         "summary": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/latest/now-summary.csv"
#     }
# }
# # cdd.download_github_data(nyc_data_dict, "New York City")
# cdd.download_la_data()


# race_demo_df = race_demo_df.sort_values(by='Deaths_Total', ascending=False)
# race_columns = [ "Date", "State", "Cases_Total", "Cases_White", "Cases_Black", "Cases_Latinx", "Cases_Asian", "Cases_AIAN", "Cases_NHPI", "Cases_Multiracial", "Cases_Other", "Cases_Unknown", "Cases_Ethnicity_Hispanic", "Cases_Ethnicity_NonHispanic", "Cases_Ethnicity_Unknown", "Deaths_Total", "Deaths_White", "Deaths_Black", "Deaths_Latinx", "Deaths_Asian", "Deaths_AIAN", "Deaths_NHPI", "Deaths_Multiracial", "Deaths_Other", "Deaths_Unknown", "Deaths_Ethnicity_Hispanic", "Deaths_Ethnicity_NonHispanic", "Deaths_Ethnicity_Unknown", "Hosp_Total", "Hosp_White", "Hosp_Black", "Hosp_Latinx", "Hosp_Asian", "Hosp_AIAN", "Hosp_NHPI", "Hosp_Multiracial", "Hosp_Other", "Hosp_Unknown", "Hosp_Ethnicity_Hispanic", "Hosp_Ethnicity_NonHispanic", "Hosp_Ethnicity_Unknown", "Tests_Total", "Tests_White", "Tests_Black", "Tests_Latinx", "Tests_Asian", "Tests_AIAN", "Tests_NHPI", "Tests_Multiracial", "Tests_Other", "Tests_Unknown", "Tests_Ethnicity_Hispanic", "Tests_Ethnicity_NonHispanic", "Tests_Ethnicity_Unknown" ]
# age_columns = [ "Data As Of", "Start Date", "End Date", "Group", "Year", "Month", "State", "Sex", "Age Group", "COVID-19 Deaths", "Total Deaths", "Pneumonia Deaths", "Pneumonia and COVID-19 Deaths", "Influenza Deaths", '"Pneumonia, Influenza, or COVID-19 Deaths"', "Footnote" ]



race_demo_df = pd.read_csv("data/covidtracking.com/racial-demo-complete-latest.csv", header=0).fillna(0)
age_demo_df = pd.read_csv("data/CDC/Provisional_COVID-19_Deaths_by_Sex_and_Age.csv", header=0).fillna(0)
# state_df = pd.read_json("data/state_info.json")
with open("data/state_info.json") as j:
    state_df = json.load(j)

demo_age = [ "Under 1 year", "0-17 years", "1-4 years", "5-14 years", "15-24 years", "18-29 years", "25-34 years", "30-39 years", "35-44 years", "40-49 years", "45-54 years", "50-64 years", "55-64 years", "65-74 years", "75-84 years", "85 years and over" ]
demo_sex = [ "Male", "Female" ]



# for i, item in age_demo_df.iterrows():
#     print(item["Data As Of"])
#     break

# Iterate over states
#   Create new DF 
#   Iterate over new DF (speed?)
#       Create variables within each demo
#       Write dict for each state's demos

## INIT
# state_dict = { "STATE": "Age": {}, "Sex": {}, "Race": {}, "Totals": {} }
## SAVE
# pd.to_json("data/zol/demo_stats/STATE.json")
# {
#     "STATE": {
#         "Age": {
#             "youngins": "MORTALITY_RATE"
#         },
#         "Sex": {
#             "MEeeEeeEN": "MORTALITY_RATE"
#         },
#         "Race": {
#             "the_blacks": "MORTALITY_RATE",
#             "the_whiteys": "MORTALITY_RATE"
#         },
#         "Totals": {
#             "Mortality rate": "MORTALITY_RATE"
#         }
#     }
# }

demo_races = [ "Black", "White", "Latinx", "Asian", "Multiracial", "Other" ]
demo_types = [ "Cases_", "Deaths_"]

demo_race_cases = []
for demo in demo_races:
    for dt in demo_types:
        demo_race_cases.append(dt + demo)


parent_dict = {}
for st, state in state_df["states"].items():
    state_name = str(state["long"])

    # print(st, state["long"])
    # continue

    try:
        test = race_demo_df.loc[race_demo_df["State"] == st]["Cases_Total"].values[0]
    except:
        continue

    # INIT new state_dict
    state_dict = { state_name : { "Age": {}, "Sex": {}, "Race": {}, "Totals": {} } }

    state_df = age_demo_df.loc[(age_demo_df["State"] == state_name) & (age_demo_df["Start Date"] == "01/01/2020") & (age_demo_df["End Date"] == "05/22/2021") & (age_demo_df["Group"] == "By Total")]

    # Get cases for state from racial demo file
    demo_all_cases = race_demo_df.loc[race_demo_df["State"] == st]["Cases_Total"].values[0]
    demo_all_death = race_demo_df.loc[race_demo_df["State"] == st]["Deaths_Total"].values[0]
    # Iterate over age groups (all sexes)

    # print(f"Age statistics for {state_name}")
    for age in demo_age:
        age_all_sex = state_df.loc[(state_df["Age Group"] == age) & (state_df["Sex"] == "All Sexes")].fillna(0)

        try:
            age_all_sex_death = age_all_sex["COVID-19 Deaths"].values[0]
        except:
            age_all_sex_death = age_all_sex["COVID-19 Deaths"]

        age_mortality_rate = round((age_all_sex_death / demo_all_cases) * 100, 2) 
        age_pct_of_covid_deaths = round((age_all_sex_death / demo_all_death) * 100, 2)

        # Add items to age demographic
        if age not in state_dict[state_name]["Age"]:
            state_dict[state_name]["Age"][age] = {}

        state_dict[state_name]["Age"][age]["m_rate"] = age_mortality_rate
        state_dict[state_name]["Age"][age]["pct_covid_deaths"] = age_pct_of_covid_deaths

    # INIT race_dict
    race_dict = {"Black":{"cases":0,"death":0,"mrate":0,"pct_covid_deaths":0},"White":{"cases":0,"death":0,"mrate":0,"pct_covid_deaths":0},"Latino":{"cases":0,"death":0,"mrate":0,"pct_covid_deaths":0},"Asian":{"cases":0,"death":0,"mrate":0,"pct_covid_deaths":0},"Multiracial":{"cases":0,"death":0,"mrate":0,"pct_covid_deaths":0},"Other":{"cases":0,"death":0,"mrate":0,"pct_covid_deaths":0}}
    for race in demo_races:
        # Black
        #   for type in types:
        #       Black+_cases: 
        #           val = black_cases
        #       Black+_deaths:
        #           val = black_deaths
        #       add to race_dict under "Black"
        # and so on...'

        race_cases = race_demo_df.loc[race_demo_df["State"] == st][demo_types[0]+race].values[0]
        race_death = race_demo_df.loc[race_demo_df["State"] == st][demo_types[1]+race].values[0]
        race_mrate = round((race_death / race_cases)*100,3)
        
        # print(f"{race}: Cases {race_cases}, Deaths {race_death}, Mortality Rate: {race_mrate}%")
        break
        # Get race death #
        # Calculate each stat

        # Add stat to main dict
            


    parent_dict[state_name] = state_dict[state_name]
    # Stop at one state so far.
    break
print(json.dumps(parent_dict))


# for i, item in age_demo_df.loc[(age_demo_df["State"] == "California") & (age_demo_df["Start Date"] == "01/01/2020") & (age_demo_df["End Date"] == "05/22/2021")].iterrows():
#     for demo in demo_age:
#         print(item["Age Group"][demo])
#     #     break
#     # & (age_demo_df["Sex"] == "All Sexes") 

#     print(item)
    # break

exit()
# Date,State,Cases_Total,Cases_White,Cases_Black,Cases_Latinx,Cases_Asian,Cases_AIAN,Cases_NHPI,Cases_Multiracial,Cases_Other,Cases_Unknown,Cases_Ethnicity_Hispanic,Cases_Ethnicity_NonHispanic,Cases_Ethnicity_Unknown,
# Deaths_Total,Deaths_White,Deaths_Black,Deaths_Latinx,Deaths_Asian,Deaths_AIAN,Deaths_NHPI,Deaths_Multiracial,Deaths_Other,Deaths_Unknown,Deaths_Ethnicity_Hispanic,Deaths_Ethnicity_NonHispanic,Deaths_Ethnicity_Unknown,Hosp_Total,Hosp_White,Hosp_Black,Hosp_Latinx,Hosp_Asian,Hosp_AIAN,Hosp_NHPI,Hosp_Multiracial,Hosp_Other,Hosp_Unknown,Hosp_Ethnicity_Hispanic,Hosp_Ethnicity_NonHispanic,Hosp_Ethnicity_Unknown,Tests_Total,Tests_White,Tests_Black,Tests_Latinx,Tests_Asian,Tests_AIAN,Tests_NHPI,Tests_Multiracial,Tests_Other,Tests_Unknown,Tests_Ethnicity_Hispanic,Tests_Ethnicity_NonHispanic,Tests_Ethnicity_Unknown

count = 0
for i, item in race_demo_df.iterrows():
    cases_black = item["Cases_Black"]
    death_black = item["Deaths_Black"]

    cases_latin = item["Cases_Latinx"]
    death_latin = item["Deaths_Latinx"]

    cases_white = item["Cases_White"]
    death_white = item["Deaths_White"]

    cases_asian = item["Cases_Asian"]
    death_asian = item["Deaths_Asian"]

    cases_all = item["Cases_Total"]
    death_all = item["Deaths_Total"]

    print(item["Date"], item["State"], item["Cases_Total"])

# print(age_demo_df.columns)

# Group == By Total


# print(race_demo_df.head())