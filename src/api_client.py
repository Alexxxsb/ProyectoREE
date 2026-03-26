import requests

#Ejemplo de llamada hacia endpoint de generación

BASE_URL = "https://apidatos.ree.es/es/datos/generacion/estructura-generacion"

def fetch_data(start_date, end_date):
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "time_trunc": "hour"
    }

    response = requests.get(BASE_URL, params=params)
    return response.json()