import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import pandas as pd
import xml.etree.ElementTree as ET
from sqlalchemy import create_engine

load_dotenv()  # loads variables from .env


def get_entsoe_load_data(start_date, end_date, api_key):
    base_url = "https://web-api.tp.entsoe.eu/api"
    params = {
        "securityToken": api_key,
        "documentType": "A65",
        "processType": "A16",  # Realized
        "outBiddingZone_Domain": "10YPL-AREA-----S",  # Poland
        "periodStart": start_date,
        "periodEnd": end_date
    }

    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        print(f"Error {response.status_code}: {response.text}")
        return None

    return response.text  # XML response


def parse_entsoe_load_xml(xml_data):
    ns = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}
    root = ET.fromstring(xml_data)

    # Get the base datetime (start of the period)
    period = root.find(".//ns:TimeSeries/ns:Period", ns)
    time_interval = period.find("ns:timeInterval", ns)
    start_str = time_interval.find("ns:start", ns).text
    dt_start = datetime.strptime(start_str, "%Y-%m-%dT%H:%MZ")

    # Collect each point
    data = []
    for point in period.findall("ns:Point", ns):
        position = int(point.find("ns:position", ns).text)
        quantity = float(point.find("ns:quantity", ns).text)
        timestamp = dt_start + timedelta(hours=position - 1)  # 1-based position
        data.append({"timestamp": timestamp, "load_MW": quantity})

    df = pd.DataFrame(data)
    df.set_index("timestamp", inplace=True)
    df.index = df.index.tz_localize("UTC").tz_convert("Europe/Warsaw")
    return df



api_key = os.getenv("API_ENERGY_TOKEN")
start = 202401020000
end = 202401030000

xml_data = get_entsoe_load_data(start, end, api_key)



engine = create_engine("sqlite:///database//entsoe_load.db")  # Change for Postgres/MySQL


if xml_data:
    df = parse_entsoe_load_xml(xml_data)
    df.to_sql("load_data", con=engine, if_exists="append", index=True)
    print(f"Saved {len(df)} new rows.")
    print(df.head())


