import requests
import pandas as pd
import pyfiglet
from datetime import datetime, timezone

all_service_locations = []
all_service_types = []

URL = "https://www.suez.com.au/en-AU/api/LocationMap/InitMap?idMap={629C6BF1-8BD9-456D-BF49-9B1E24AFC1B6}"

RESPONSE = requests.get(URL)
JSON_CONTENT = RESPONSE.json()

def extract_service_locations() -> None:
    """
    This function extracts all the service locations from the JSON content
    """
    
    service_locations = JSON_CONTENT['PoiItem']
    
    for service in service_locations:
        icon_id = service["IconId"].replace("{", "").replace("}", "")
        service_name = service["Name"]
        latitude = service["Lat"]
        longitude = service["Lng"]
        
        location_details = {
            "icon_id": icon_id,
            "service_name": service_name,
            "latitude": latitude,
            "longitude": longitude
        }
        
        all_service_locations.append(location_details)
    return

def extract_service_types() -> None:
    """
    This function extracts all the service types from the JSON content
    """
    
    service_types = JSON_CONTENT['MapIcon']
    
    for service in service_types:
        icon_id = service["Id"].replace("{", "").replace("}", "")
        service_type = service["Legend"]
        service_icon = service["Image"]
        
        service_types_details = {
            'icon_id': icon_id,
            "service_type": service_type,
            "service_icon": service_icon
        }
        
        all_service_types.append(service_types_details)
    return

def load_data() -> None:
    """
    This function loads the scraped data into a CSV file
    """
    
    utc_timezone = timezone.utc
    current_utc_timestamp = datetime.now(utc_timezone).strftime('%d-%b-%Y %H:%M:%S')
    
    service_locations_df = pd.DataFrame(all_service_locations)
    service_types_df = pd.DataFrame(all_service_types)
    
    services_df = pd.merge(service_locations_df, service_types_df, on="icon_id", how="left")
    services_df = services_df.iloc[:,1:]
    services_df["last_updated_at_UTC"] = current_utc_timestamp
    
    services_df.to_csv('suez_services_raw_data.csv',encoding="utf-8", index=False)
    return

if __name__ == '__main__':
    
    scraper_title = "SUEZ SERVICES SCRAPER"
    ascii_art_title = pyfiglet.figlet_format(scraper_title, font='small')
    
    start_time = datetime.now()
    
    print('\n\n')
    print(ascii_art_title)
    print('Extracting Suez Service Locations...')
    
    extract_service_locations()
    
    print(f'Total Service Locations Available: {len(all_service_locations)}')
    print('Extracting Suez Service Types...')
    
    extract_service_types()
    
    print(f'Total Service Types Available: {len(all_service_types)}')
    print('\n')
    
    end_time = datetime.now()
    scraping_time = end_time - start_time
    
    print('All Services Types & Service Locations Collected...')
    print(f'Time spent on collecting: {scraping_time}')
    print('\n')
    print("Joining & Consolidating Service Locations & Service Types...")
    print("Loading data to CSV...")
    
    load_data()
    
    print('Data Exported to CSV...')
    print('Process Completed !!!')