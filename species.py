import requests
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='starwars')
c = conn.cursor()

url = 'https://swapi.dev/api/species'
while url:
    response = requests.get(url)
    data = response.json()
    for species in data['results']:
        created = datetime.strptime(species['created'], "%Y-%m-%dT%H:%M:%S.%fZ")
        edited = datetime.strptime(species['edited'], "%Y-%m-%dT%H:%M:%S.%fZ")
        insert_species = (
            "INSERT INTO species (name, classification, designation, average_height, skin_colors, hair_colors, eye_colors, average_lifespan, homeworld, language, created, edited, url) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        species_data = (
            species['name'], 
            species['classification'], 
            species['designation'], 
            species['average_height'] if species['average_height'] != 'unknown' else None, 
            species['skin_colors'], 
            species['hair_colors'], 
            species['eye_colors'], 
            species['average_lifespan'] if species['average_lifespan'] != 'unknown' else None, 
            species['homeworld'], 
            species['language'], 
            created,
            edited,
            species['url']
        )
        c.execute(insert_species, species_data)

    # Get the next page URL
    url = data['next']

conn.commit()
conn.close()
