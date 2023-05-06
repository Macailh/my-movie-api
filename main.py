from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

movies_list = [
    {
        'id': 1,
        'title': 'Avatar',
        'overview': "En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...",
        'year': '2009',
        'rating': 7.8,
        'category': 'Acción'
    },
    {
        'id': 2,
        'title': 'Titanic',
        'overview': "En el viaje inaugural del Titanic, el barco más grande jamás construido, Rose...",
        'year': '1997',
        'rating': 7.8,
        'category': 'Drama, Romance'
    },
    {
        'id': 3,
        'title': 'Star Wars: Episodio IV - Una nueva esperanza',
        'overview': "La princesa Leia es capturada y retenida como rehén por el malvado Imperio Galáctico ...",
        'year': '1977',
        'rating': 8.6,
        'category': 'Acción, Aventura, Fantasía'
    },
    {
        'id': 4,
        'title': 'El señor de los anillos: La comunidad del anillo',
        'overview': "La tranquilidad de la Comarca, una región del mundo de la Tierra Media habitada por ...",
        'year': '2001',
        'rating': 8.8,
        'category': 'Acción, Aventura, Drama'
    }
]

@app.get("/", tags=["home"])
def root():
    return HTMLResponse("<h1>Start</h1>")

@app.get("/movies", tags=["movies"])
def get_all_movies():
    return movies_list

@app.get("/movies/{id}", tags=["movies"])
def get_movie_by_id(id: int):
    for movie in movies_list:
        if movie["id"] == id:
            return movie
    return {"error": "movie not found"}