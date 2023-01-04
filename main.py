import sqlite3
import json


# lists with values only 
people_values = []
planets_values = []
films_values = []
species_values = []
vehicles_values = []
starships_values = []
res_values = [people_values, planets_values, films_values, species_values, vehicles_values, starships_values]

# for intermediate tables (films_people -- f_people)
f_people = []
f_planets = []
f_starships = []
f_vehicles = []
f_species = []
p_starships = []
p_vehicles = []
many_to_many = [f_people, f_planets, f_starships, f_vehicles, f_species, p_starships, p_vehicles]

# function to get values only from dict
def get_values(full_list:list, val_list:list):
        for i in range(len(full_list)):
            val_list.append(list(full_list[i].values()))

# function to get only num from url (foreign key)
def get_key_from_url(url:str):
        temp = url.split('/')
        return int(temp.pop((len(temp)-2)))

# function to cut off irrelevent info (dates, lists (they'll go into intermediate tables like films_people)) + special condition for people table (species goes after films)
def filter_values(val_list:list, people=False, people_dict=None):
    indx = None
    for i in range(len(val_list)):
        for el in val_list[i]:
            # gets keys, not url
            if el is not None and isinstance(el, str) and 'https' in el:
                _indx = val_list[i].index(el)
                val_list[i][_indx] = get_key_from_url(el)
            # need to find index only once, they're all the same
            if indx:
                continue

            if isinstance(el, list):
                indx = val_list[i].index(el)

        val_list[i] = val_list[i][:indx]
    
        if not people:
            continue
            
        species = people_dict[i]['species']
        if species:
            people_values[i].append(get_key_from_url(species[0]))
        else:
            people_values[i].append(None)

# function to get list of nums (keys) not url
def get_key_list(lt:list):
    temp = lt.copy()
    for i in temp:
        temp[temp.index(i)] = get_key_from_url(i)
    return temp

# function gets data from json file, fills in all lists
def get_data():
    people_full = []
    planets_full = []
    films_full = []
    species_full = []
    vehicles_full = []
    starships_full = []
    res_full = [people_full, planets_full, films_full, species_full, vehicles_full, starships_full]

    with open('data.json', 'r') as f:
        temp = json.load(f)
    for i, j in list(zip(res_full, temp)):
        i.extend(j)

    for i, j in list(zip(res_full, res_values)):
        get_values(i, j)

    for el in res_values:
        if el == people_values:
            filter_values(el, True, people_full)
        filter_values(el)

    # so into list goes key, not url
    for i in range(len(films_full)):
        f_people.append(get_key_list(films_full[i]['characters']))
        f_planets.append(get_key_list(films_full[i]['planets']))
        f_starships.append(get_key_list(films_full[i]['starships']))
        f_vehicles.append(get_key_list(films_full[i]['vehicles'])) 
        f_species.append(get_key_list(films_full[i]['species'])) 

    for i in range(len(people_full)):
        p_starships.append(get_key_list(people_full[i]['starships']))
        p_vehicles.append(get_key_list(people_full[i]['vehicles']))

get_data()

# # sql connection/cursor -----------------------------------------------
connection = sqlite3.connect('Star_wars.db')
cursor = connection.cursor()

# create tables from file (if here - looks clunky)
with open('create_tables.sql', 'r') as sql_file:
    sql_script = sql_file.read()
cursor.executescript(sql_script)
connection.commit()

# insert records into tables -----------------------------------------------
cursor.executemany('INSERT INTO Films ("title", "episode_id", "opening_crawl", "director", "producer", "release_date") VALUES (?,?,?,?,?,?);', films_values)
cursor.executemany('INSERT INTO Planets ("name", "rotation_period", "orbital_period", "diameter", "climate", "gravity", "terrain", "surface_water", "population") VALUES (?,?,?,?,?,?,?,?,?);', planets_values)
cursor.executemany('INSERT INTO Starships ("name", "model", "manufacturer", "cost_in_credits", "length", "max_atmosphering_speed", "crew", "passengers", "cargo_capacity", "consumables", "hyperdrive_rating", "MGLT", "starship_class") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);', starships_values)
cursor.executemany('INSERT INTO Vehicles ("name", "model", "manufacturer", "cost_in_credits", "length", "max_atmosphering_speed", "crew", "passengers", "cargo_capacity", "consumables", "vehicle_class") VALUES (?,?,?,?,?,?,?,?,?,?,?);', vehicles_values)
cursor.executemany('INSERT INTO Species ("name", "classification", "designation", "average_height", "skin_colors", "hair_colors", "eye_colors", "average_lifespan", "homeworld", "language") VALUES (?,?,?,?,?,?,?,?,?,?);', species_values)
cursor.executemany('INSERT INTO People ("name", "height", "mass", "hair_color", "skin_color", "eye_color", "birth_year", "gender", "homeworld", "species") VALUES (?,?,?,?,?,?,?,?,?,?);', people_values)

connection.commit()

# insert records into intemediate tables -----------------------------------------------
def insert_many(key_list:list, table:str,  record1:str, record2:str):
    for i in range(len(key_list)):
        
        if not key_list[i]:
            cursor.execute(f'INSERT INTO {table} ({record1}, {record2}) VALUES ({i+1}, NULL);')
            continue
        
        for el in key_list[i]:
            cursor.execute(f'INSERT INTO {table} ({record1}, {record2}) VALUES ({i+1}, {el});')

insert_many(f_planets, "films_planets", "id_films", "id_planets")
insert_many(f_species, "films_species", "id_films", "id_species")
insert_many(f_starships, "films_starships", "id_films", "id_starships")
insert_many(f_vehicles, "films_vehicles", "id_films", "id_vehicles")
insert_many(f_people, "films_people", "id_films", "id_people")
insert_many(p_starships, "people_starships", "id_people", "id_starships")
insert_many(p_vehicles, "people_vehicles", "id_people", "id_vehicles")

connection.commit()

#---------------------------------------------------------------------
# Testing

cursor.execute('''
    SELECT Films.title, Films.director, Films.release_date 
    FROM Films;
''')
res = cursor.fetchmany(3)

print('Films --------------------------')
print(res)
print()

cursor.execute('''
    SELECT People.name, People.birth_year, Planets.name 
    FROM People
    INNER JOIN Planets ON People.homeworld = Planets.id;
''')
res = cursor.fetchmany(3)

print('People/Species--------------------------')
print(res)
print()

cursor.execute('''
    SELECT People.name, People.birth_year, Planets.name 
    FROM People
    INNER JOIN Planets ON People.homeworld = Planets.id
    WHERE People.gender = "female";
''')
res = cursor.fetchall()

print('Women --------------------------')
print(res)
print()

cursor.execute('''
    SELECT Films.title, Planets.name, Planets.population 
    FROM films_planets
    INNER JOIN Films ON films_planets.id_films = Films.id
    INNER JOIN Planets ON films_planets.id_planets = Planets.id
    ORDER BY Films.episode_id;
''')
res = cursor.fetchall()

print('Films/Planets --------------------------')
print(res)
print()

cursor.close()