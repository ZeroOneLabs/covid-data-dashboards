import os
import json
import pathlib
import requests
import urllib.request
from datetime import datetime


base_dir = os.path.dirname(os.path.realpath(__file__))

today_str = datetime.strftime(datetime.today(), "%Y-%m-%d")
# Datetime object created from a format to eliminate hours, minutes, seconds, miliseconds.
today_obj = datetime.strptime(today_str, "%Y-%m-%d")

# List of data folders that we'll check if they exist
# This was implemented after I decided to purge the files locally before comitting, 
# so that the Github repo wouldn't get filled with file downloads.
data_dir_names = [ "CDC", "NYT", "ZeroOneLabs" ]

for dir_name in data_dir_names:
    dir = os.path.join(base_dir, f"data/{dir_name}")
    if not os.path.exists(dir):
        try:
            os.mkdir(dir)
        except:
            print(f"There was an error creating the directory: {dir}")


def download_file(url, path):

    # print(f"Downloading file [{url}] to local path [{path}]")
    try:
        urllib.request.urlretrieve(url, path)
    except Exception as e:
        print(e)


def download_cdc_data():
    cdc_data_path = os.path.join(base_dir, "data/CDC")

    race_date_url = "https://data.cdc.gov/resource/pj7m-y5uh.json?$order=end_week%20DESC"
    # age_date_url format: yyyy-mm-ddT00:00:00.000
    age_date_url = "https://data.cdc.gov/api/id/9bhg-hcku.json?$order=end_date%20DESC"

    # latest_date_str_race = json.loads(requests.get(race_date_url).text)[0]["end_week"]
    latest_date_str_age = json.loads(requests.get(age_date_url).text)[0]["end_date"]

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

    # The reason I set up these file names in a dict like this,
    # is because NYT has the same file names for both their 
    # historical and "live" (totals) data, which is annoying.
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

        for thefile in [ item['local_name_latest'], item['local_name_historical'] ]:
            
            remote_url = live_url if thefile == item['local_name_latest'] else base_url

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