import mysql.connector
from datetime import datetime

# Connexion à la base de données
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="starwars"
)
c = cnx.cursor()

# Liste des nouveaux films à ajouter
new_films = [
{
"title": "The Force Awakens",
"episode_id": 7,
"opening_crawl": "Luke Skywalker has vanished. In his absence, the sinister FIRST ORDER has risen from the ashes of the Empire and will not rest until Skywalker, the last Jedi, has been destroyed. With the support of the REPUBLIC, General Leia Organa leads a brave RESISTANCE. She is desperate to find her brother Luke and gain his help in restoring peace and justice to the galaxy. Leia has sent her most daring pilot on a secret mission to Jakku, where an old ally has discovered a clue to Luke’s whereabouts…",
"director": "J.J. Abrams",
"producer": "Kathleen Kennedy, J.J. Abrams, Bryan Burk",
"release_date": "2015-12-11",
"created": datetime.now().isoformat(),
"edited": datetime.now().isoformat(),
"url": "https://swapi.dev/api/films/7/"
},
{
"title": "The Last Jedi",
"episode_id": 8,
"opening_crawl": "The First Order reigns...",
"director": "Rian Johnson",
"producer": "Kathleen Kennedy, Ram Bergman",
"release_date": "2017-12-15",
"created": datetime.now().isoformat(),
"edited": datetime.now().isoformat(),
"url": "https://swapi.dev/api/films/8/"
},
{
"title": "The Rise of Skywalker",
"episode_id": 9,
"opening_crawl": "The dead speak!...",
"director": "J.J. Abrams",
"producer": "Kathleen Kennedy, J.J. Abrams, Michelle Rejwan",
"release_date": "2019-12-20",
"created": datetime.now().isoformat(),
"edited": datetime.now().isoformat(),
"url": "https://swapi.dev/api/films/9/"
}
]

# Parcours de la liste des nouveaux films
for film in new_films:
    # Insertion des données du film dans la table
    insert_film = "INSERT INTO films (title, episode_id, opening_crawl, director, producer, release_date, created, edited, url) VALUES (%(title)s, %(episode_id)s, %(opening_crawl)s, %(director)s, %(producer)s, %(release_date)s, %(created)s, %(edited)s, %(url)s)"
    c.execute(insert_film, film)

# Validation des modifications dans la base de données
cnx.commit()

# Fermeture de la connexion à la base de données
c.close()
cnx.close()
