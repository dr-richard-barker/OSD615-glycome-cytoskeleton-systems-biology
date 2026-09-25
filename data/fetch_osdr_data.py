import os
import json
import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pandas as pd
import numpy as np

def get_session():
    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))
    return session

def fetch_data():
    session = get_session()
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)
    
    print("Fetching OSD-615 manifest...")
    try:
        res = session.get("https://osdr.nasa.gov/osdr/data/osd/files/615?all_files=true", timeout=10)
        res.raise_for_status()
        print("Successfully fetched OSD-615 manifest")
    except requests.RequestException as e:
        print(f"OSDR API unavailable: {e}. Please ensure network connectivity or use local curated empirical files.")
        return

if __name__ == '__main__':
    fetch_data()
