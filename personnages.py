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
        url = data['next']

    return all_people

def process_people_data(people):
    processed_people = []

    for person in people:
        mass = None
        if person['mass'].isnumeric():
            mass = float(person['mass'])

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
            person['created'], 
            person['edited'], 
            person['url']
        )

        processed_people.append(processed_person)

    return processed_people


def insert_people_data(cnx, people):
    insert_person = ("INSERT INTO people "
                     "(name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, created, edited, url) "
                     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
    cursor = cnx.cursor()

    try:
        cursor.executemany(insert_person, people)
        cnx.commit()
    except Exception as e:
        print(f"Error inserting people data: {e}")
        cnx.rollback()
    finally:
        cursor.close()

def insert_all_people_to_db(cnx):
    all_people = fetch_all_people()
    processed_people = process_people_data(all_people)
    insert_people_data(cnx, processed_people)

# Où que vous exécutiez votre script
cnx = mysql.connector.connect(user='root', password='password', host='localhost', database='starwars')
insert_all_people_to_db(cnx)
cnx.close()
