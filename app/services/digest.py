"""
This fetches and renders the morning digest data.
"""

import logging
import os
from collections.abc import Sequence
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models import Task
from app.services.scripture import get_random_scripture
from app.services.weather import get_weather_summary

load_dotenv()

logger = logging.getLogger(__name__)

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
env = Environment(
    loader=FileSystemLoader(TEMPLATES),
    autoescape=select_autoescape(["html"]),
)


def render_digest(
    day: date,
    tasks: Sequence[Task] | list,
    weather: dict | None = None,
    scripture: dict | None = None,
) -> str:
    """
    Renders the digest HTML template with the provided context.
    """
    return env.get_template("digest.html").render(
        date_label=f"{day:%A}, {day.day} {day:%B %Y}",
        tasks=tasks,
        weather=weather,
        scripture=scripture,
    )


async def generate_digest(
    city: str | None = None,
    session: Session | None = None,
    scripture_translation: str = "web",
    scripture_book: str | None = None,
) -> str:
    """
    Gathers pending tasks, current weather, and daily scripture,
    then renders the morning digest HTML.
    """
    # 1. Fetch pending tasks from the database
    tasks: Sequence[Task] | list = []
    if session is not None:
        tasks = (
            session.query(Task)
            .filter(Task.is_completed.is_(False))
            .order_by(Task.due_date.asc().nulls_last(), Task.priority.desc())
            .all()
        )
    else:
        with SessionLocal() as db_session:
            tasks = (
                db_session.query(Task)
                .filter(Task.is_completed.is_(False))
                .order_by(Task.due_date.asc().nulls_last(), Task.priority.desc())
                .all()
            )

    # 2. Fetch weather summary with graceful fallback
    target_city = city or os.getenv("WEATHER_CITY", "London")
    weather = None
    if target_city:
        try:
            weather = await get_weather_summary(target_city)
        except Exception as e:
            logger.warning(f"Could not retrieve weather for digest: {e}")

    # 3. Fetch scripture with graceful fallback
    scripture = None
    try:
        scripture = await get_random_scripture(
            translation=scripture_translation,
            book=scripture_book,
        )
    except Exception as e:
        logger.warning(f"Could not retrieve scripture for digest: {e}")

    # 4. Render HTML template
    return render_digest(
        day=date.today(),
        tasks=tasks,
        weather=weather,
        scripture=scripture,
    )


# Alias for backward compatibility
fetch_digest = generate_digest