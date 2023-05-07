from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Path
from fastapi.responses import HTMLResponse

app = FastAPI()


class Movie(BaseModel):
    id: int = Field(ge=1)
    title: str = Field(min_length=1, max_length=50)
    overview: str | None = Field(default="En la ...", max_length=200)
    year: int = Field(le=2022)
    rating: float = Field(default=5, ge=0, le=10)
    category: str | None = Field(max_length=50)

    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "title": "Titanic",
                "overview": "En el viaje inaugural del Titanic...",
                "year": 1997,
                "rating": 7.8,
                "category": "Romance"
            }
        }


movies_list = [Movie(id=1, title="Avatar", overview="En un exuberante planeta llamado Pandora viven los Na'vi, seres que ...", year=2009, rating=7.8, category="Acción"),
               Movie(id=2, title="Titanic", overview="En el viaje inaugural del Titanic, el barco más grande jamás construido, Rose...",
                     year=1997, rating=7.8, category="Romance"),
               Movie(id=3, title="Star Wars: Episodio IV - Una nueva esperanza",
                     overview="La princesa Leia es capturada y retenida como rehén por el malvado Imperio Galáctico ...", year=1977, rating=8.6, category="Fantasía"),
               Movie(id=4, title="El señor de los anillos: La comunidad del anillo", overview="La tranquilidad de la Comarca, una región del mundo de la Tierra Media habitada por ...", year=2001, rating=8.8, category="Aventura")]


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
    # return list(filter(lambda x: x['category'] == category, movies))


@app.post("/movies", tags=["movies"])
def create_movie(movie: Movie):
    movies_list.append(movie)
    return movies_list


@app.put("/movies/{id}", tags=["movies"])
def update_movie(id: int, movie: Movie):
    for m in movies_list:
        if m.id == id:
            m.title = movie.title
            m.overview = movie.overview
            m.year = movie.year
            m.rating = movie.rating
            m.category = movie.category

            return movies_list

    return {"error": "movie not found"}


@app.delete("/movies/{id}", tags=["movies"])
def delete_movie(id: int):
    for movie in movies_list:
        if movie.id == id:
            movies_list.remove(movie)

            return movies_list

    return {"error", "movie not found"}
