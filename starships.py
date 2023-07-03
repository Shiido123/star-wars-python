import requests
import mysql.connector
from datetime import datetime
import re

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='starwars')
c = conn.cursor()

url = 'https://swapi.dev/api/starships'
while url:
    response = requests.get(url)
    data = response.json()
    for starship in data['results']:
        MAX_DECIMAL_VALUE = 999999999999.999
        cost_in_credits = float(starship['cost_in_credits']) if starship['cost_in_credits'] != 'unknown' else None
        length = float(starship['length'].replace(',', '.')) if starship['length'] != 'unknown' else None
        max_atmosphering_speed = None
        if starship['max_atmosphering_speed'] not in ['unknown', 'n/a']:
            match = re.match(r"(\d+)", starship['max_atmosphering_speed'])
            if match:
                max_atmosphering_speed = int(match.group(1))
        crew = starship['crew'] if starship['crew'] != 'unknown' else None
        passengers = int(starship['passengers']) if 'passengers' in starship and starship['passengers'].isdigit() else None
        cargo_capacity = None
        if starship['cargo_capacity'] != 'unknown':
            temp_cargo_capacity = float(starship['cargo_capacity'])
            if temp_cargo_capacity < MAX_DECIMAL_VALUE:
                cargo_capacity = temp_cargo_capacity
        consumables = starship['consumables']
        hyperdrive_rating = float(starship['hyperdrive_rating']) if starship['hyperdrive_rating'] != 'unknown' else None
        mglt = int(starship['MGLT']) if 'MGLT' in starship and starship['MGLT'] != 'unknown' else None
        starship_class = starship['starship_class']
        created = datetime.strptime(starship['created'].rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f")
        edited = datetime.strptime(starship['edited'].rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f")
        url = starship['url']

        insert_starship = (
            "INSERT INTO starships (name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, hyperdrive_rating, MGLT, starship_class, created, edited, url) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        starship_data = (
            starship['name'],
            starship['model'],
            starship['manufacturer'],
            cost_in_credits,
            length,
            max_atmosphering_speed,
            crew,
            passengers,
            cargo_capacity,
            consumables,
            hyperdrive_rating,
            mglt,
            starship_class,
            created,
            edited,
            url
        )
        c.execute(insert_starship, starship_data)

    url = data['next']

conn.commit()
conn.close()
