import os
import requests
from datetime import datetime
from datetime import timedelta

today = datetime.today()
yesterday = today - timedelta(days = 1)
yesterday_str = datetime.strftime(yesterday, '%m-%d-%Y')

JHD_BASE_DIR = os.path.dirname(os.path.realpath(__file__))
JHD_DATA_DIR = os.path.join(JHD_BASE_DIR, "data", "JohnsHopkins")
JHD_YESTERDAY_FILE = os.path.join(JHD_DATA_DIR, yesterday_str + ".csv")

jh_data_url = f"https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/{yesterday_str}.csv"

def download_johnshopkins_data():
    if not os.path.exists(JHD_YESTERDAY_FILE):
        teh_file = requests.get(jh_data_url)
        teh_file.encoding = 'utf-8-sig'

        if teh_file.response_code == 200:
            with open(JHD_YESTERDAY_FILE, "w") as f:
                f.write(teh_file.text)
        else:
            yesterday = today - timedelta(days = 2)
            yesterday_str = datetime.strftime(yesterday, '%m-%d-%Y')
            teh_file = requests.get(jh_data_url)
            teh_file.encoding = 'utf-8-sig'

            if teh_file.response_code == 200:
                with open(JHD_YESTERDAY_FILE, "w") as f:
                    f.write(teh_file.text)
            else:
                print(f"{__name__}: Could not download previous 2 days of Johns Hopkins data.")


if __name__ == "__main__":
    download_johnshopkins_data()



