import requests

def fetch_data(endpoint):
    response = requests.get(endpoint)
    response.raise_for_status()
    return response.json()
