from pydantic import BaseModel, Field


class Movie(BaseModel):
    id: int | None = None
    title: str = Field(min_length=1, max_length=50)
    overview: str | None = Field(default="En la ...", max_length=200)
    year: int = Field(le=2022)
    rating: float = Field(default=5, ge=0, le=10)
    category: str | None = Field(max_length=50)

    class Config:
        schema_extra = {
            "example": {
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
