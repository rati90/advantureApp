from fastapi import FastAPI

from services.backend.models import UserProfile, Adventure


app = FastAPI()


@app.get("/home")
async def get_home():
    return {"home_page": "Welcome"}


@app.post("/user_profile/")
async def get_profile(user_profile: UserProfile):
    return {"Name": user_profile.name,
            "Surname": user_profile.surname,
            "Birthdate": user_profile.birthdate}


@app.post("/adventure/{adventure_id}")
async def get_adventure(adventure_id: str,adventure: Adventure):
    return {"adventure_id": adventure_id,
            "adventure name": adventure.name}

