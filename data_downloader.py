import os
import json
import pathlib
import requests
import urllib.request
from datetime import datetime


base_dir = os.path.dirname(os.path.realpath(__file__))

# String object
today_str = datetime.strftime(datetime.today(), "%Y-%m-%d")
# Datetime object created from a format to eliminate hours, minutes, seconds, miliseconds.
today_obj = datetime.strptime(today_str, "%Y-%m-%d")



def download_file(url, path):
    # print(f"Trying to download {url} to {path}")
    try:
        urllib.request.urlretrieve(url, path)
    except Exception as e:
        print(e)

def download_cdc_data():
    cdc_data_path = os.path.join(base_dir, "data/CDC")

    race_date_url = "https://data.cdc.gov/resource/pj7m-y5uh.json?$order=end_week%20DESC"
    age_date_url = "https://data.cdc.gov/api/id/9bhg-hcku.json?$order=end_date%20DESC"

    latest_date_str_race = requests.get(race_date_url).text
    latest_date_str_race = json.loads(latest_date_str_race)
    latest_date_str_race = latest_date_str_race[0]["end_week"]

    latest_date_str_age = requests.get(age_date_url).text
    latest_date_str_age = json.loads(latest_date_str_age)
    latest_date_str_age = latest_date_str_age[0]["end_date"]

    cdc_file_names = {
        "Deaths_by_Race_and_Hispanic_Origin": f"https://data.cdc.gov/resource/pj7m-y5uh.json?end_week={latest_date_str_age}&start_week=2020-01-01T00:00:00.000",
        "Deaths_by_Sex_and_Age": f"https://data.cdc.gov/api/id/9bhg-hcku.json?$query=select%20*%2C%20%3Aid%20where%20((upper(%60group%60)%20%3D%20upper(%27By%20Total%27))%20and%20(%60end_date%60%20%3D%20%27{latest_date_str_age}%27)%20and%20((upper(%60state%60)%20!%3D%20upper(%27United%20States%27)%20OR%20%60state%60%20IS%20NULL))%20and%20(upper(%60sex%60)%20%3D%20upper(%27All%20Sexes%27))%20and%20((%60year%60%20!%3D%201999%20OR%20%60year%60%20IS%20NULL)))"
    }


    for filename, url in cdc_file_names.items():
        filepath = os.path.join(cdc_data_path, f"{today_str}-{filename}.json")
        if not os.path.exists(filepath):
            # Download file to cdc_data_path
            download_file(url, filepath)



def download_nyt_data():
    data_dir = os.path.join(base_dir, "data/NYT")

    # Define names for CSV/JSON files
    ## Data pulled from NYT Github: https://github.com/nytimes/covid-19-data/tree/master
    base_url = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/"
    live_url = f"{base_url}live/"


    states_latest_csv_name = "us-states-latest.csv"
    counties_latest_csv_name = "us-counties-latest.csv"
    us_latest_csv_name = "us-latest.csv"

    states_historical_csv_name = "us-states-historical.csv"
    counties_historical_csv_name = "us-counties-historical.csv"
    us_historical_csv_name = "us-historical.csv"

    data_file_list = [ states_latest_csv_name, counties_latest_csv_name, us_latest_csv_name, states_historical_csv_name, counties_historical_csv_name, us_historical_csv_name ]

    data_file_dict = {
        'us-states': {
            'remote_name': 'us-states.csv',
            'local_name_latest': 'us-states-latest.csv',
            'local_name_historical': 'us-states-historical.csv',
        },
        'us-counties': {
            'remote_name': 'us-counties.csv',
            'local_name_latest': 'us-counties-latest.csv',
            'local_name_historical': 'us-counties-historical.csv',
        },
        'us-nationwide': {
            'remote_name': 'us.csv',
            'local_name_latest': 'us-latest.csv',
            'local_name_historical': 'us-historical.csv',
        }
    }

    # Check if the files exist in the current folder's subfolder of "data"
    #   if not: Download them from the URLs defined above
    for csv_file in data_file_dict:
        # store the dict in a short variable for clean reading
        item = data_file_dict[csv_file]

        # I originally had 'if statements' and variables duplicated. Figured, why not a for-loop?
        for thefile in [ item['local_name_latest'], item['local_name_historical'] ]:
            # for the file in [ 'us-latest.csv', 'us-historical.csv' ]

            if thefile == item['local_name_latest']:
                remote_url = live_url
            else:
                remote_url = base_url

            # Store temp variables to 
            tmp_local_file = os.path.join(data_dir, thefile)
            tmp_local_stat = pathlib.Path(tmp_local_file)
            # modified_day gets the datetime object from the pathlib.Path object output above.
            try:
                modified_day = datetime.fromtimestamp(tmp_local_stat.stat().st_mtime)
                # Store the following two variables as datetime objects so they can be compared.
                modified_day = datetime.strptime(datetime.strftime(modified_day, "%Y-%m-%d"), "%Y-%m-%d")
            except:
                file_exists = False

            # If the file doesn't exist or it's modified time is earlier than today
            # then download a fresh file
            if not os.path.exists(tmp_local_file) \
                or not modified_day \
                or modified_day < today_obj:
                url = remote_url + data_file_dict[csv_file]['remote_name']
                # print(f"Downloading from {url} to {tmp_local_file}.")
                download_file(url, tmp_local_file)
                ## TODO add funtion to back up previous downloads and g-zip them so we can audit data for integrity later if needed?

if __name__ == "__main__":
    download_nyt_data()
    download_cdc_data()