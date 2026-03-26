import requests

#Ejemplo de llamada hacia endpoint de generación

import requests

BASE_URL = "https://apidatos.ree.es/es/datos/generacion/evolucion_renovable"

def get_generacion_data(start_date, end_date):
    params = {
        "start_date": "2023-01-01T00:00",
        "end_date": "2023-01-01T05:00",
        "time_trunc": "hour", 
        "geo_limit": "peninsular"
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.get(BASE_URL, params=params, headers=headers)

    print("STATUS:", response.status_code)
    print("URL:", response.url)
    print("TEXT:", response.text[:200])

    if response.status_code != 200:
        raise Exception(f"Error API: {response.status_code}")

    return response.json()