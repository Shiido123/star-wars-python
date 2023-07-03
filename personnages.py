import mysql.connector
import requests
from datetime import datetime

def fetch_all_people():
    url = "https://swapi.dev/api/people/"
    all_people = []

    while url:
        response = requests.get(url)
        data = response.json()
        all_people.extend(data['results'])
        print(f"Fetched {len(data['results'])} people from {url}")
        url = data['next']

    print(f"Total people fetched: {len(all_people)}")
    return all_people

def process_people_data(people):
    processed_people = []

    for person in people:
        mass = None
        # Check if mass is a number
        try:
            mass = float(person['mass'])
        except ValueError:
            print(f"Cannot convert {person['mass']} to float")

        # Convert 'created' and 'edited' to datetime
        created = datetime.fromisoformat(person['created'].replace("Z", "+00:00"))
        edited = datetime.fromisoformat(person['edited'].replace("Z", "+00:00"))

        processed_person = (
            person['name'], 
            person['height'], 
            mass,
            person['hair_color'], 
            person['skin_color'], 
            person['eye_color'], 
            person['birth_year'], 
            person['gender'], 
            person['homeworld'], 
            created, 
            edited, 
            person['url']
        )

        processed_people.append(processed_person)

    return processed_people

def insert_people_data(cnx, people):
    insert_person = ("INSERT INTO personnages "
                     "(name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, created, edited, url) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor = cnx.cursor()

    for person in people:
        try:
            cursor.execute(insert_person, person)
            cnx.commit()
        except Exception as e:
            print(f"Error inserting person {person[0]}: {e}")
            cnx.rollback()

    cursor.close()

def insert_all_people_to_db(cnx):
    all_people = fetch_all_people()
    processed_people = process_people_data(all_people)
    insert_people_data(cnx, processed_people)

# Où que vous exécutiez votre script
cnx = mysql.connector.connect(user='root', password='password', host='localhost', database='starwars')
insert_all_people_to_db(cnx)
cnx.close()
