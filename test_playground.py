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


# race_demo_df = pd.read_csv("data/covidtracking.com/racial-demo-complete-latest.csv", names=[ "Date", "State", "Cases_Total", "Cases_White", "Cases_Black", "Cases_Latinx", "Cases_Asian", "Cases_AIAN", "Cases_NHPI", "Cases_Multiracial", "Cases_Other", "Cases_Unknown", "Cases_Ethnicity_Hispanic", "Cases_Ethnicity_NonHispanic", "Cases_Ethnicity_Unknown", "Deaths_Total", "Deaths_White", "Deaths_Black", "Deaths_Latinx", "Deaths_Asian", "Deaths_AIAN", "Deaths_NHPI", "Deaths_Multiracial", "Deaths_Other", "Deaths_Unknown", "Deaths_Ethnicity_Hispanic", "Deaths_Ethnicity_NonHispanic", "Deaths_Ethnicity_Unknown", "Hosp_Total", "Hosp_White", "Hosp_Black", "Hosp_Latinx", "Hosp_Asian", "Hosp_AIAN", "Hosp_NHPI", "Hosp_Multiracial", "Hosp_Other", "Hosp_Unknown", "Hosp_Ethnicity_Hispanic", "Hosp_Ethnicity_NonHispanic", "Hosp_Ethnicity_Unknown", "Tests_Total", "Tests_White", "Tests_Black", "Tests_Latinx", "Tests_Asian", "Tests_AIAN", "Tests_NHPI", "Tests_Multiracial", "Tests_Other", "Tests_Unknown", "Tests_Ethnicity_Hispanic", "Tests_Ethnicity_NonHispanic", "Tests_Ethnicity_Unknown" ])
race_demo_df = pd.read_csv("data/covidtracking.com/racial-demo-complete-latest.csv", header=0)
# race_demo_df = race_demo_df.sort_values(by='Deaths_Total', ascending=False)

columns = [ "Data As Of", "Start Date", "End Date", "Group", "Year", "Month", "State", "Sex", "Age Group", "COVID-19 Deaths", "Total Deaths", "Pneumonia Deaths", "Pneumonia and COVID-19 Deaths", "Influenza Deaths", '"Pneumonia, Influenza, or COVID-19 Deaths"', "Footnote" ]
age_demo_df = pd.read_csv("data/CDC/Provisional_COVID-19_Deaths_by_Sex_and_Age.csv", header=0)

demo_age = [ "All Ages", "Under 1 year", "0-17 years", "1-4 years", "5-14 years", "15-24 years", "18-29 years", "25-34 years", "30-39 years", "35-44 years", "40-49 years", "45-54 years", "50-64 years", "55-64 years", "65-74 years", "75-84 years", "85 years and over" ]
demo_sex = [ "All Sexes", "Male", "Female" ]


for i, item in age_demo_df.iterrows():
    print(item["Data As Of"])
    break

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

    print(item["Date"], item["State"])

print(age_demo_df.columns)

# Group == By Total


# print(race_demo_df.head())