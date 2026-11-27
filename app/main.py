from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from app.database import Base, engine
from app.models import Task
from app.routers import tasks, external
from app.services.weather import get_weather_summary
from app.services.scripture import get_random_scripture


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan,
              title="Dagur")

app.include_router(tasks.router)
app.include_router(external.router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}

# Testing
# @app.get("/weather", tags=["weather"])
# async def weather(city: str = "Berlin"):
#     return await get_weather_summary(city)
#
# @app.get("/scripture", tags=["scripture"])
# async def scripture(translation: str = "web"):
#     return await get_random_scripture(translation)