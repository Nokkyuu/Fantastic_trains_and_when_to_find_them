from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import pandas as pd
import requests
import os
import pytz
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default arguments for the DAG
default_args = {
    'owner': 'train-delays',
    'depends_on_past': False,
    'start_date': days_ago(1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def load_stations_data():
    """Load and filter stations data"""
    stations_df = pd.read_csv("data/fromAPI/StaDa.csv")
    # Drop lower categories
    stations_df.drop(labels=stations_df.query("category == 6").index, axis=0, inplace=True)
    stations_df.drop(labels=stations_df.query("category == 7").index, axis=0, inplace=True)
    return stations_df

def fetch_train_delays(**context):
    """Main function to fetch train delay data"""
    berlin_tz = pytz.timezone('Europe/Berlin')
    
    # Load stations data
    stations_df = load_stations_data()
    eva_nrs = stations_df["eva_nr"].values
    names = stations_df["name"].values
    states = stations_df["state"].values
    cities = stations_df["city"].values
    zipcodes = stations_df["zipcode"].values
    longs = stations_df["long"].values
    lats = stations_df["lat"].values
    cats = stations_df["category"].values
    
    # API credentials
    client_id = os.getenv('DB_CLIENT_ID')
    client_secret = os.getenv('DB_API_KEY')
    
    if not client_id or not client_secret:
        raise ValueError("Missing environment variables. Please set DB_CLIENT_ID and DB_API_KEY in your .env file")
    
    headers = {
        "DB-Api-Key": client_secret,
        "DB-Client-Id": client_id,
        "accept": "application/xml"
    }
    
    # Initialize data collection
    grabtime = f"{datetime.now(berlin_tz).hour:02d}"
    plan_data = []
    change_data = []
    buglog = []
    date = datetime.now(berlin_tz).strftime("%y%m%d")
    
    print(f"Start data collection at {date} {grabtime}")
    
    # Fetch data for each station
    for i in range(len(eva_nrs)):
        url_change = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/{eva_nrs[i]}"
        url_plan = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/{eva_nrs[i]}/{date}/{grabtime}"
        
        try:
            response_plan = requests.get(url_plan, headers=headers)
            response_change = requests.get(url_change, headers=headers)
        except Exception as e:
            bug = f"{names[i]} connection skipped: {str(e)}"
            buglog.append(bug)
            print(bug)
            continue
        
        # Process plan data
        try:
            plan_root = ET.fromstring(response_plan.content)
            for s in plan_root.findall('.//s'):
                s_id = s.get('id')
                s_eva = s.get('eva')
                ar = s.find('ar')
                ar_pt = ar.get('pt') if ar is not None else None
                ar_ppth = ar.get('ppth') if ar is not None else None
                dp = s.find('dp')
                dp_pt = dp.get('pt') if dp is not None else None
                dp_l = dp.get('l') if dp is not None else None
                
                plan_data.append([s_id, ar_pt, dp_pt, dp_l, ar_ppth, eva_nrs[i], 
                                cats[i], names[i], states[i], cities[i], zipcodes[i], 
                                longs[i], lats[i]])
        except Exception as e:
            bug = f"{names[i]} plan skipped: {str(e)}"
            buglog.append(bug)
            print(bug)
        
        # Process change data
        try:
            change_root = ET.fromstring(response_change.content)
            for s in change_root.findall('.//s'):
                s_id = s.get('id')
                s_eva = s.get('eva')
                m = s.find('m')
                cat = m.get('cat') if m is not None else None
                ar = s.find('ar')
                ar_ct = ar.get('ct') if ar is not None else None
                dp = s.find('dp')
                dp_ct = dp.get('ct') if dp is not None else None
                
                change_data.append([s_id, ar_ct, dp_ct, cat])
        except Exception as e:
            bug = f"{names[i]} change skipped: {str(e)}"
            buglog.append(bug)
            print(bug)
    
    # Process and merge data
    columns = ['ID', 'arrival', "departure", "train", "path", 'eva_nr', 
               "category", "name", "state", "city", "zip", "long", "lat"]
    plan_df = pd.DataFrame(plan_data, columns=columns)
    plan_df['arrival'] = pd.to_datetime(plan_df['arrival'], format='%y%m%d%H%M', errors='coerce')
    plan_df['departure'] = pd.to_datetime(plan_df['departure'], format='%y%m%d%H%M', errors='coerce')
    
    columns = ['ID', 'arrival', "departure", "info"]
    change_df = pd.DataFrame(change_data, columns=columns)
    change_df['arrival'] = pd.to_datetime(change_df['arrival'], format='%y%m%d%H%M', errors='coerce')
    change_df['departure'] = pd.to_datetime(change_df['departure'], format='%y%m%d%H%M', errors='coerce')
    
    # Merge and calculate delays
    delay_df = pd.merge(plan_df, change_df, how='left', on="ID", suffixes=('_plan', '_change'))
    delay_df['depature_delay_m'] = delay_df['departure_change'] - delay_df['departure_plan']
    delay_df['arrival_delay_m'] = delay_df['arrival_change'] - delay_df['arrival_plan']
    
    # Sort columns
    delay_df = delay_df[['ID', 'train', 'path', 'eva_nr', "category", 'name', 'state', 
                        'city', 'zip', 'long', 'lat', 'arrival_plan', 'departure_plan', 
                        'arrival_change', 'departure_change', 'arrival_delay_m', 
                        'depature_delay_m', "info"]]
    
    # Convert delays to minutes
    delay_df["depature_delay_m"] = delay_df["depature_delay_m"].dt.total_seconds() / 60
    delay_df["depature_delay_m"] = delay_df["depature_delay_m"].fillna(value=0).astype(int)
    delay_df["arrival_delay_m"] = delay_df["arrival_delay_m"].dt.total_seconds() / 60
    delay_df["arrival_delay_m"] = delay_df["arrival_delay_m"].fillna(value=0).astype(int)
    delay_df["eva_nr"] = delay_df["eva_nr"].astype(int)
    
    # Save data
    os.makedirs("data/fromAPI/hourly2", exist_ok=True)
    delay_df.to_csv(f"data/fromAPI/hourly2/{date}_{grabtime}.csv", index=False)
    
    # Save log
    with open(f"data/fromAPI/hourly2/{date}_{grabtime}_log.txt", "w") as file:
        for item in buglog:
            file.write(f"{item}\n")
    
    print(f"Data collection completed. Saved {len(delay_df)} records.")

# Create the DAG
dag = DAG(
    'train_delays_hourly',
    default_args=default_args,
    description='Hourly train delays data collection from Deutsche Bahn API',
    schedule_interval='3 * * * *',  # Run at 3 minutes past every hour
    catchup=False,
    tags=['trains', 'delays', 'api'],
)

# Define the task
fetch_delays_task = PythonOperator(
    task_id='fetch_train_delays',
    python_callable=fetch_train_delays,
    dag=dag,
)

fetch_delays_task