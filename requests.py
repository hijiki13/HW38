import requests
import json


URL = r"https://swapi.dev/api/"
URL_CATEGORY = ["people/", "planets/", "films/", "species/", "vehicles/", "starships/"]

people_full = []
planets_full = []
films_full = []
species_full = []
vehicles_full = []
starships_full = []

res_list = [people_full, planets_full, films_full, species_full, vehicles_full, starships_full]

def get_data(url, results:list):
    response = requests.get(url)
    if response.status_code != 200:
        return
    
    res = json.loads(response.text)
    results.extend(res['results'])       

    if res['next'] != None:
        get_data(res['next'], results)


for category, res in list(zip(URL_CATEGORY, res_list)):
    get_data(URL+category, res)

# save so you don't have to run it again 
with open('data.json', 'w') as f:
    json.dump(res_list, f)