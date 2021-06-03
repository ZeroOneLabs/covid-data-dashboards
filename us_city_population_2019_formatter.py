import pandas as pd

exit("Reformat the JSON fields to match the new format")

ct_df = pd.read_json("data/us-city-population-2019.json")
# ct_df.to_json("data/us-city-population-2019.json")
cities_dict = {}
for i, city in enumerate(ct_df["City"]):
    name = city
    state = ct_df["State"][i]
    population = ct_df["population (2019)"][i]
    area_sqft = ct_df["Area (sq mi)"][i]
    area_sqkm = ct_df["Area (sq km)"][i]
    pop_dense_sqmi = ct_df["Pop density (sq mi)"][i]
    pop_dense_sqkm = ct_df["Pop density (sq km)"][i]
    coordinates = ct_df["coordinates"][i]
    
    cities_dict[i] = { 
        "city": name, "county": [], "state": state, 
        "pop": population, 
        "area_sqft": area_sqft, "area_sqkm": area_sqkm, 
        "pop_dense_sqmi": pop_dense_sqmi, 
        "pop_dense_sqkm": pop_dense_sqkm, "coordinates": coordinates,
        "resources": {
            "github": {
                "totals": {
                    "url1_example": "https://sample.url/"
                }
            },
            "github_data_type": "",
            "city_covid_portal": "",
            "notes": ""
        },
        "data": {
            "totals": {
                "cases": 0,
                "deaths": 0
            },
            "recent": {
                "range": "",
                "cases": 0,
                "deaths": 0
            }
        },
        "rates_all_time": { 
            "mort_rate_total": "", 
            "mort_rate_senior": "", 
            "mort_rate_mid": "", 
            "mort_rate_adult": "", 
            "mort_rate_teen": "", 
            "mort_rate_child": "" 
        },
        "rates_recent": { 
            "mort_rate_total": "", 
            "mort_rate_senior": "", 
            "mort_rate_mid": "", 
            "mort_rate_adult": "", 
            "mort_rate_teen": "", 
            "mort_rate_child": "" 
        }
    }

# print(cities_dict)

ct_jsdf = pd.DataFrame(cities_dict)
ct_jsdf.to_json("data/us-city-population-2019-v2.json")
