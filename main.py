import requests
import mysql.connector

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='starwars')
c = conn.cursor()

url = 'https://swapi.dev/api/planets'
while url:
    response = requests.get(url)
    data = response.json()
    for planet in data['results']:
        insert_planet = (
            "INSERT INTO planets (name, rotation_period, orbital_period, diameter, climate, gravity, terrain, surface_water, population) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        planet_data = (
            planet['name'], 
            planet['rotation_period'] if planet['rotation_period'] != 'unknown' else None, 
            planet['orbital_period'] if planet['orbital_period'] != 'unknown' else None, 
            planet['diameter'] if planet['diameter'] != 'unknown' else None, 
            planet['climate'] if planet['climate'] != 'unknown' else None, 
            planet['gravity'] if planet['gravity'] != 'unknown' else None, 
            planet['terrain'] if planet['terrain'] != 'unknown' else None, 
            planet['surface_water'] if planet['surface_water'] != 'unknown' else None, 
            planet['population'] if planet['population'] != 'unknown' else None
        )
        c.execute(insert_planet, planet_data)

    # Get the next page URL
    url = data['next']

conn.commit()
conn.close()
