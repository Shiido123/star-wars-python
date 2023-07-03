import requests
import mysql.connector
from datetime import datetime

conn = mysql.connector.connect(user='root', password='password', host='localhost', database='starwars')
c = conn.cursor()

url = 'https://swapi.dev/api/vehicles'
while url:
    response = requests.get(url)
    data = response.json()
    for vehicle in data['results']:
        try:
            created = datetime.strptime(vehicle['created'].rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            created = datetime.strptime(vehicle['created'].rstrip('Z'), "%Y-%m-%dT%H:%M:%S")
        
        try:
            edited = datetime.strptime(vehicle['edited'].rstrip('Z'), "%Y-%m-%dT%H:%M:%S.%f")
        except ValueError:
            edited = datetime.strptime(vehicle['edited'].rstrip('Z'), "%Y-%m-%dT%H:%M:%S")
        
        cargo_capacity = None if vehicle['cargo_capacity'] in ['unknown', 'none'] else float(vehicle['cargo_capacity'])
        
        insert_vehicle = (
            "INSERT INTO vehicles (name, model, manufacturer, cost_in_credits, length, max_atmosphering_speed, crew, passengers, cargo_capacity, consumables, vehicle_class, created, edited, url) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        )
        vehicle_data = (
            vehicle['name'],
            vehicle['model'],
            vehicle['manufacturer'],
            vehicle['cost_in_credits'] if vehicle['cost_in_credits'] != 'unknown' else None,
            vehicle['length'] if vehicle['length'] != 'unknown' else None,
            vehicle['max_atmosphering_speed'] if vehicle['max_atmosphering_speed'] != 'unknown' else None,
            vehicle['crew'] if vehicle['crew'] != 'unknown' else None,
            vehicle['passengers'] if vehicle['passengers'] != 'unknown' else None,
            cargo_capacity,
            vehicle['consumables'],
            vehicle['vehicle_class'],
            created,
            edited,
            vehicle['url']
        )
        c.execute(insert_vehicle, vehicle_data)

    # Get the next page URL
    url = data['next']

conn.commit()
conn.close()
