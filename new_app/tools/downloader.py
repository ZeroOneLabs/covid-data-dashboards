# Throw this in a Lambda? 
# AWS cost calculator says running this code every day in Lambda would be free

# IF data does not exist (in Aurora?)
#   Download entire set of data
# ELSE
#   get current date of data
#   # NYT data will be difficult because they store everything in a giant CSV file. :/ 


# URLs
'''
race_date_url = "https://data.cdc.gov/resource/pj7m-y5uh.json?$order=end_week%20DESC"
age_date_url = "https://data.cdc.gov/api/id/9bhg-hcku.json?$order=end_date%20DESC"

base_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/"

race_date_url = "https://data.cdc.gov/resource/pj7m-y5uh.json?$order=end_week%20DESC"
age_date_url = "https://data.cdc.gov/api/id/9bhg-hcku.json?$order=end_date%20DESC"


latest_date_str_age = json.loads(requests.get(age_date_url).text)[0]["end_date"]

"Deaths_by_Race_and_Hispanic_Origin": f"https://data.cdc.gov/resource/pj7m-y5uh.json?end_week={latest_date_str_age}&start_week=2020-01-01T00:00:00.000",
"Deaths_by_Sex_and_Age": f"https://data.cdc.gov/api/id/9bhg-hcku.json?$query=select%20*%2C%20%3Aid%20where%20((upper(%60group%60)%20%3D%20upper(%27By%20Total%27))%20and%20(%60end_date%60%20%3D%20%27{latest_date_str_age}%27)%20and%20((upper(%60state%60)%20!%3D%20upper(%27United%20States%27)%20OR%20%60state%60%20IS%20NULL))%20and%20(upper(%60sex%60)%20%3D%20upper(%27All%20Sexes%27))%20and%20((%60year%60%20!%3D%201999%20OR%20%60year%60%20IS%20NULL)))"

base_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/"


"Deaths_by_Race_and_Hispanic_Origin": f"https://data.cdc.gov/resource/pj7m-y5uh.json?end_week={latest_date_str_age}&start_week=2020-01-01T00:00:00.000",
"Deaths_by_Sex_and_Age": f"https://data.cdc.gov/api/id/9bhg-hcku.json?$query=select%20*%2C%20%3Aid%20where%20((upper(%60group%60)%20%3D%20upper(%27By%20Total%27))%20and%20(%60end_date%60%20%3D%20%27{latest_date_str_age}%27)%20and%20((upper(%60state%60)%20!%3D%20upper(%27United%20States%27)%20OR%20%60state%60%20IS%20NULL))%20and%20(upper(%60sex%60)%20%3D%20upper(%27All%20Sexes%27))%20and%20((%60year%60%20!%3D%201999%20OR%20%60year%60%20IS%20NULL)))"

'''
