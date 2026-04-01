import requests
import json 

BASE_URL = "https://apidatos.ree.es/es/datos/generacion/estructura-generacion"

def get_generacion_data(start_date, end_date):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "time_trunc": "hour", 
        "geo_limit": "peninsular"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(BASE_URL, params=params, headers=headers, timeout=10)

        print("STATUS:", response.status_code)
        print("URL:", response.url)
        print("TEXT:", response.text[:200])

        print("JSON:", json.dumps(response.json(), indent=2)[:1000])    

        if response.status_code != 200:
            print(f"Error API: {response.status_code}")
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Error llamando a la API: {e}")
        return None