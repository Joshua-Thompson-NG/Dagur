"""
Getting external information for the email
"""

import os

from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException, status

from app.services.scripture import get_random_scripture
from app.services.weather import get_weather_summary

load_dotenv()

weather_city = os.getenv("WEATHER_CITY", "London")

router = APIRouter(
    prefix="/external",
    tags=["external"]
)

@router.get("/weather")
async def get_weather_summary_endpoint(city: str = weather_city):
    return await get_weather_summary(city)

@router.get("/random-scripture")
async def get_random_scripture_endpoint(translation: str = "kjv",
                                book: str | None = "JHN"):
    return await get_random_scripture(translation=translation, book=book)