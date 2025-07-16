from pathlib import Path
import requests


API_BASE_URL = 'https://pokeapi.co/api/v2/'


response = requests.get(API_BASE_URL)
endpoints = response.json()

API_POKEMON_URL = endpoints['pokemon']
API_STATS_URL = endpoints['stat']

