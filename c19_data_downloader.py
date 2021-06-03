import os
import sys
import json
import pathlib
import html5lib
import requests
import pandas as pd
import urllib.request
from datetime import datetime
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs




base_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = os.path.join(base_dir, "data")
# String object
today_str = datetime.strftime(datetime.today(), "%Y-%m-%d")
# Datetime object
today = datetime.strptime(today_str, "%Y-%m-%d")

def create_dirs(dirs: list):
    if type(dirs) != list:
        print("create_dirs(): Argument passed does not contain a type of 'list'.")
        return

    for dir in dirs:
        if not os.path.exists(dir):
            try:
                os.makedirs(dir)
            except Exception as s:
                exit(s)


def download_file(url, path):
    # print(f"Trying to download {url} to {path}")
    try:
        urllib.request.urlretrieve(url, path)
    except Exception as e:
        print(e)


def download_geojson_counties():
    save_file_geojson = os.path.join(data_dir, 'geojson-counties-fips.json')
    if not os.path.exists(save_file_geojson):
        # If it doesn't exist, then download it and write it to a file.
        with urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)
        # Write it.
        with open(save_file_geojson, 'w') as f:
            json.dump(counties, f)
    else:
        # Must mean the file exists. Load it.
        with open(save_file_geojson, 'r') as f:
            counties = json.load(f)

def download_nyt_data():

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
                today = datetime.strptime(datetime.strftime(datetime.today(), "%Y-%m-%d"), "%Y-%m-%d")
            except:
                file_exists = False

            # If the file doesn't exist or it's modified time is earlier than today
            # then download a fresh file
            if not os.path.exists(tmp_local_file) \
                or not modified_day \
                or modified_day < today:
                url = remote_url + data_file_dict[csv_file]['remote_name']
                print(f"Downloading from {url} to {tmp_local_file}.")
                download_file(url, tmp_local_file)
                ## TODO add funtion to back up previous downloads and g-zip them so we can audit data for integrity later if needed?


def download_github_data(city_resources: dict, city_name: str): 
    ## The data passed to this function is expected to be in the following format
    # { 
    #     "urls": {
    #         "total-deaths-by-demo": {
    #             "url": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/deaths-by-race-age.csv",
    #             "type": "csv"
    #         },
    #         "total-cases-by-poverty": {
    #             "url": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/antibody-by-poverty.csv",
    #             "type": "csv"
    #         },
    #         "deaths_by_conditions": {
    #             "url": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/totals/deaths-by-underlying-conditions.csv",
    #             "type": "csv"
    #         },
    #         "latest-summary": {
    #             "url": "https://raw.githubusercontent.com/nychealth/coronavirus-data/master/latest/now-summary.csv",
    #             "type": "csv"
    #         }
    #     }
    # }



    download_path = os.path.join(data_dir, "city/", city_name)

    create_dirs([os.path.join(download_path, "totals"), os.path.join(download_path, "latest")])

    for item in city_resources:
        for url in city_resources[item]:
            url_parsed = urlparse(city_resources[item][url])
            the_filename = os.path.basename(url_parsed.path)

            path_to_file = os.path.join(download_path, item, the_filename)
            full_path = pathlib.Path(path_to_file)

            try:
                modified_day = datetime.fromtimestamp(full_path.stat().st_mtime)
                # Store the following two variables as datetime objects so they can be compared.
                modified_day = datetime.strptime(datetime.strftime(modified_day, "%Y-%m-%d"), "%Y-%m-%d")
            except:
                modified_day = today
                file_exists = False

            # if chk_file.is_file():
            if not full_path.is_file() or not modified_day or modified_day < today:
                the_url = city_resources[item][url]
                download_file(the_url, full_path)
                # print(f"Trying to download {the_url} to {full_path}.")


            # print(item, the_filename)

def download_la_data():
    path_to_city_dir = os.path.join(data_dir, "city", "Los Angeles")
    create_dirs([path_to_city_dir])

    table_xpath = "/html/body/div[2]/div[1]/div[3]/div/div/table"

    r = requests.get("http://publichealth.lacounty.gov/media/Coronavirus/locations.htm")
    soup = bs(r.content, 'lxml')
    main_table = soup.select("div.pb-4:nth-child(3) > div:nth-child(1) > div:nth-child(1) > table:nth-child(1)")[0]

    ## Instantiate multiple variables at type 'dict'
    main_list = main_list["race-cases"] = main_list["race-deaths"] = main_list["age-cases"] = main_list["sex-cases"] = main_list["sex-cases"] = main_list["summary"] = {}
    the_key = the_val = ""
    count = 0
    suffix = ""
    # suffix = " " + str(count) # testing to find out the number/index of each entered line.
    for row in main_table.find_all('td'):
        the_text = row.text.strip('-  ')
        the_text = the_text.strip('**')
        the_text = the_text.replace(u'\xa0', u' ')

        if 18 < count < 27:
            count += 1
            continue

        mod = count % 2
        if mod == 0:
            # We're on the left-hand column values of the table
            the_key = the_text

            # If the left-hand value is empty, then the right side is worthless. Increase the count by 2 and skip the main iteration.
            if the_key == "":
                count += 2
                continue 

        else:
            # We're on the right-hand column values of the table
            # Skip lines we don't want.
            if count in [1, 13, 15, 17, 27, 45, 43, 47, 53, 61, .75, 81, 83, 85, 87, 99, 59, 101]:
                count += 1
                continue

            if 1 < count < 13:
                main_list["summary"][the_key] = the_text + suffix
                count += 1
                continue

            if 47 < count < 58:
                main_list["sex-cases"][the_key] = the_text + suffix
                count += 1
                continue

            if 27 < count < 42:
                main_list["age-cases"][the_key] = the_text + suffix
                count += 1
                continue

            if 59 < count < 78:
                main_list["race-cases"][the_key] = the_text + suffix
                count += 1
                continue
            

            if 85 < count < 104: 
                main_list["race-deaths"][the_key] = the_text + suffix
                count += 1
                continue

            main_list[the_key] = the_text + suffix
            the_key = ""
        count += 1


    the_filename = today_str + "-los-angeles-covid-data.json"
    write_path = os.path.join(path_to_city_dir, the_filename)

    with open(write_path, "w") as outfile:
        json.dump(main_list, outfile, indent=4)


def download_chicago_data():
    path_to_city_dir = os.path.join(data_dir, "city", "Los Angeles")
    create_dirs([path_to_city_dir])
    
    today_str = datetime.strftime(datetime.today(), "%Y-%m-%d")
    the_filename = today_str + "-los-angeles-covid-data.json"
    write_path = os.path.join(path_to_city_dir, the_filename)

def download_houston_data():
    # Since this file requires being converted to UTF-8 with no BOM, I left this as-is.
    teh_file = requests.get("https://opendata.arcgis.com/api/v3/datasets/7d0e9739dc5a4dc6abc1f714b77f0976_0/downloads/data?format=csv&spatialRefId=4326")
    teh_file.encoding = 'utf-8-sig'

    with open("data/city/Houston/" + today_str + "-summary.csv", "w") as f:
        f.write(teh_file.text)





