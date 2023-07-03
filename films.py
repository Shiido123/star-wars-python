import mysql.connector
import requests
from datetime import datetime

# Connexion à la base de données
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="starwars"
)
c = cnx.cursor()

# Récupération des données depuis l'API
response = requests.get("https://swapi.dev/api/films/")
films_data = response.json()

# Parcours de la liste des films
for film_data in films_data["results"]:
    # Conversion de la valeur de la colonne "created" en un format compatible avec MySQL
    created = datetime.strptime(film_data["created"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Conversion de la valeur de la colonne "edited" en un format compatible avec MySQL
    edited = datetime.strptime(film_data["edited"], "%Y-%m-%dT%H:%M:%S.%fZ")

    # Extraction des autres données du film
    film = {
        "title": film_data["title"],
        "episode_id": film_data["episode_id"],
        "opening_crawl": film_data["opening_crawl"],
        "director": film_data["director"],
        "producer": film_data["producer"],
        "release_date": film_data["release_date"],
        "created": created,
        "edited": edited,
        "url": film_data["url"]
    }

    # Insertion des données du film dans la table
    insert_film = "INSERT INTO films (title, episode_id, opening_crawl, director, producer, release_date, created, edited, url) VALUES (%(title)s, %(episode_id)s, %(opening_crawl)s, %(director)s, %(producer)s, %(release_date)s, %(created)s, %(edited)s, %(url)s)"
    c.execute(insert_film, film)

# Validation des modifications dans la base de données
cnx.commit()

# Fermeture de la connexion à la base de données
c.close()
cnx.close()
