from pydantic import BaseModel
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from jwt_manager import create_token


user_router = APIRouter()


class User(BaseModel):
    email: str
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@gmail.com",
                "password": "admin"
            }
        }


@user_router.post("/login", tags=["auth"])
def login(user: User):
    if user.email == "admin@gmail.com" and user.password == "admin":
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)
