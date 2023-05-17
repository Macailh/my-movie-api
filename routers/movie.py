from pydantic import BaseModel, Field

from fastapi import APIRouter, Path, Query, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from models.movie import Movie as MovieModel
from config.database import Session
from services.movies import MovieService
from schemas.movie import Movie

movie_router = APIRouter()


@movie_router.get("/movies", tags=["movies"], response_model=list[Movie])
def get_all_movies():
    db = Session()
    result = MovieService(db).get_all_movies()
    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get("/movies/{id}", tags=["movies"], response_model=Movie)
def get_movie_by_id(id: int = Path(ge=0, le=2000)):
    db = Session()
    result = MovieService(db).get_movie_by_id(id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.get("/movies/", tags=["movies"], response_model=Movie)
def get_movies_by_category(category: str = Query(min_length=3, max_length=50)):
    db = Session()
    result = MovieService(db).get_movie_by_category(category)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="No movies in the category")

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.post("/movies", tags=["movies"], response_model=list[Movie])
def create_movie(movie: Movie):
    db = Session()
    new_movie = MovieModel(**movie.dict())
    db.add(new_movie)
    db.commit()
    return JSONResponse(status_code=201, content={"message": "Movie register sucessfully"})


@movie_router.put("/movies/{id}", tags=["movies"], response_model=list[Movie])
def update_movie(id: int, movie: Movie):
    db = Session()
    result = MovieService(db).get_movie_by_id(id)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    result.title = movie.title
    result.overview = movie.overview
    result.year = movie.year
    result.rating = movie.rating
    result.category = movie.category

    return JSONResponse(status_code=200, content=jsonable_encoder(result))


@movie_router.delete("/movies/{id}", tags=["movies"], response_model=list[Movie])
def delete_movie(id: int = Path(ge=0, le=2000)):
    db = Session()
    result = MovieService(db).delete_movie(id)

    print(result)

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    db.delete(result)
    db.commit()

    return JSONResponse(status_code=204, content={})
