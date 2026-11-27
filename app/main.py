from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from app.database import Base, engine
from app.models import Task
from app.routers import tasks


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan,
              title="Dagur")

app.include_router(tasks.router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "healthy"}