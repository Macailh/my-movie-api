from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse


from config.database import engine, Base

from middlewares.error_handler import ErrorHandler
from middlewares.jwt_bearer import JWTBearer

from routers.movie import movie_router
from routers.user import user_router

app = FastAPI()
app.title = "Movies API"
app.version = "0.0.1"

app.add_middleware(ErrorHandler)
app.include_router(movie_router)
app.include_router(user_router)

Base.metadata.create_all(bind=engine)


@app.get("/", tags=["home"])
def root():
    return HTMLResponse("<h1>Start</h1>")
