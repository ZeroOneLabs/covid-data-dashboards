import os
import json
import pathlib
import requests
import urllib.request
from datetime import datetime


base_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(base_dir, "data/NYT")
# String object
today_str = datetime.strftime(datetime.today(), "%Y-%m-%d")
# Datetime object
today = datetime.strptime(today_str, "%Y-%m-%d")

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

def download_file(url, path):
    # print(f"Trying to download {url} to {path}")
    try:
        urllib.request.urlretrieve(url, path)
    except Exception as e:
        print(e)


def download_nyt_data():
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
                today = datetime.strptime(datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d")
            except:
                file_exists = False

            # If the file doesn't exist or it's modified time is earlier than today
            # then download a fresh file
            if not os.path.exists(tmp_local_file) \
                or not modified_day \
                or modified_day < today:
                url = remote_url + data_file_dict[csv_file]['remote_name']
                # print(f"Downloading from {url} to {tmp_local_file}.")
                download_file(url, tmp_local_file)
                ## TODO add funtion to back up previous downloads and g-zip them so we can audit data for integrity later if needed?

if __name__ == "__main__":
    download_nyt_data()