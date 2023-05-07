from fastapi import FastAPI, Body, Path
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
        'category': 'Romance'
    },
    {
        'id': 3,
        'title': 'Star Wars: Episodio IV - Una nueva esperanza',
        'overview': "La princesa Leia es capturada y retenida como rehén por el malvado Imperio Galáctico ...",
        'year': '1977',
        'rating': 8.6,
        'category': 'Fantasía'
    },
    {
        'id': 4,
        'title': 'El señor de los anillos: La comunidad del anillo',
        'overview': "La tranquilidad de la Comarca, una región del mundo de la Tierra Media habitada por ...",
        'year': '2001',
        'rating': 8.8,
        'category': 'Aventura'
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

@app.get("/movies/", tags=["movies"])
def get_movies_by_category(category: str):
    for movie in movies_list:
        if movie["category"] == category:
            return movie
                
    return {"error": "no movies in the category"}
    #return list(filter(lambda x: x['category'] == category, movies))

@app.post("/movies", tags=["movies"])
def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    movies_list.append({
        "id": id,
        "tile": title,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
    })
    return movies_list

@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    for movie in movies_list:
        if movie["id"] == id:
            movie["title"] = title
            movie["overview"] = overview
            movie["year"] = year
            movie["rating"] = rating
            movie["category"] = category

            return movies_list
        
    return {"error": "movie not found"}

@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    for movie in movies_list:
        if movie["id"] == id:
            movies_list.remove(movie)

            return movies_list
    return {"error", "movie not found"}
