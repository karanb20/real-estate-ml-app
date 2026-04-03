import requests
import pandas as pd
import time

def get_coordinates(sector):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"Sector {sector}, Gurugram, Haryana, India",
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "gurgaon-project/1.0 (test@gmail.com)"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if response.status_code == 200:
            results = response.json()
            if results:
                return results[0]["lat"], results[0]["lon"]
    except Exception as e:
        print(f"Error for sector {sector}: {e}")
    
    return None, None

data = []
for sector in range(1, 116):
    lat, lon = get_coordinates(sector)
    data.append({
        "Sector": f"Sector {sector}",
        "Latitude": lat,
        "Longitude": lon
    })
    print(f"Sector {sector}: {lat}, {lon}")
    time.sleep(1)

df = pd.DataFrame(data)
df.to_csv("gurgaon_sectors_coordinates.csv", index=False)