from fastapi import FastAPI

from services.backend.models import UserProfile


app = FastAPI()


@app.get("/home")
async def get_home():
    return {"home_page": "Welcome"}


@app.get("/user_profile/")
async def get_profile(user_profile: UserProfile):
    return {"Name": user_profile.name,
            "Surname": user_profile.surname,
            "Birthdate": user_profile.birthdate}
