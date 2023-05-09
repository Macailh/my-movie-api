from typing import Optional
from pydantic import BaseModel, Field

from fastapi import FastAPI, Body, Path, Query, HTTPException, status, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.encoders import jsonable_encoder

from jwt_manager import create_token, validate_token

from config.database import Session, engine, Base
from models.movie import Movie as MovieModel

from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

app = FastAPI()
app.title = "Movies API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)

Base.metadata.create_all(bind=engine)


class User(BaseModel):
    email: str
    password: str


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


@app.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)


@app.get("/movies", tags=["movies"], response_model=list[Movie])
def get_all_movies():
    db = Session()
    result = db.query(MovieModel).all()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=0, le=2000)):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.get("/movies/", tags=["movies"], response_model=Movie)
def get_movies_by_category(category: str = Query(min_length=3, max_length=50)):
    db = Session()
    result = db.query(MovieModel).filter(
        MovieModel.category == category).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No movies in the category")

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.post("/movies", tags=["movies"], response_model=list[Movie])
def create_movie(movie: Movie):
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Movie register sucessfully"})


@app.put("/movies/{id}", tags=["movies"], response_model=list[Movie])
def update_movie(id: int, movie: Movie):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@app.delete("/movies/{id}", tags=["movies"], response_model=list[Movie])
def delete_movie(id: int = Path(ge=0, le=2000)):
    db = Session()
    result = db.query(MovieModel).filter(MovieModel.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    db.delete(result)
    db.commit()

    return JSONResponse(status_code=204)
