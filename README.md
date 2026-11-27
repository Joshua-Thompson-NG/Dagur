# Dagur

**Dagur** (Old Norse / Icelandic for *"Day"*) is a personal morning briefing and task management API built with **FastAPI** and **SQLite**. It aggregates your pending tasks, fetches daily weather forecasts and an uplifting scripture passage, renders an HTML email digest using **Jinja2**, and delivers it to your inbox on schedule.

---

## Features

- **Task Management**: RESTful endpoints to create, list, update, and delete personal tasks stored in a local SQLite database.
- **Weather Service**: Fetches coordinates and daily forecast metrics (temperatures, precipitation chance, weather codes) via Open-Meteo.
- **Daily Scripture Service**: Retrieves scripture verses dynamically using the Bible API.
- **Morning Digest Engine**: Assembles pending to-dos, weather forecasts, and daily scripture into a clean, responsive HTML email template using Jinja2.
- **Email Delivery Service**: Configurable SMTP client with support for STARTTLS and SSL.
- **Cron Automation**: Python entrypoint designed to run via scheduled cron jobs (e.g., every morning at 7:00 AM).
- **Protected Endpoints**: API key authentication (`X-API-Key`) to secure task management endpoints.

---

## Project Structure

```text
Dagur/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entrypoint & router registrations
│   ├── database.py          # SQLAlchemy engine, session maker, & base model
│   ├── dependencies.py      # Dependency injections (DB session, API key auth)
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas (DTOs & validation)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py         # Task CRUD endpoints
│   │   └── external.py      # Weather and scripture preview endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather.py       # Open-Meteo weather service
│   │   ├── scripture.py     # Bible API scripture service
│   │   ├── email.py         # SMTP email delivery service
│   │   └── digest.py        # Compiles tasks, weather, & scripture into HTML
│   ├── templates/
│   │   └── digest.html      # Jinja2 HTML email digest template
│   └── jobs/
│       ├── __init__.py
│       └── send_digest.py   # CLI / Cron entrypoint to trigger daily digest
├── tests/                   # Pytest test suite
├── .env                     # Local environment variables (gitignored)
├── .env.example             # Example configuration template
├── .gitignore
├── pyproject.toml
└── requirements.txt         # Project dependencies
```

---

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database**: [SQLite](https://www.sqlite.org/) with [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **Templating**: [Jinja2](https://jinja.palletsprojects.com/)
- **HTTP Client**: [HTTPX](https://www.python-httpx.org/)
- **Testing**: [pytest](https://docs.pytest.org/)

---

## Getting Started

### 1. Prerequisites
- Python 3.13+ 
- `uv` (recommended) or standard `pip` / `venv`

### 2. Environment Setup

Clone the repository and set up a virtual environment:

```bash
# Using uv:
uv venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux

# Using standard python venv:
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux
```

Install dependencies:

```bash
# Using uv:
uv sync

# Or using pip:
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your settings:

```bash
cp .env.example .env
```

Key environment variables:
- `API_SECRET_KEY`: Secret key required in the `X-API-Key` header for task endpoints.
- `DATABASE_URL`: SQLite connection string (defaults to `sqlite:///./dagur.db`).
- `WEATHER_CITY`: Target city for daily weather forecast (e.g. `London`, `Berlin`).
- `SMTP_HOST`: SMTP server host (e.g. `smtp.gmail.com`).
- `SMTP_PORT`: SMTP port (`587` for STARTTLS, `465` for SSL).
- `SMTP_USER`: Email account username / address.
- `SMTP_PASSWORD`: Email password or Gmail App Password.
- `EMAIL_FROM`: Sender address.
- `EMAIL_TO`: Recipient address for the morning digest.

---

## Running the Application

### Start the API Server

```bash
# Using FastAPI CLI:
fastapi dev app/main.py

# Or using Uvicorn directly:
uvicorn app.main:app --reload
```

Interactive API documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## API Endpoints

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/health` | Health check endpoint | No |
| `GET` | `/tasks` | List all tasks | Yes (`X-API-Key`) |
| `POST` | `/tasks` | Create a new task | Yes (`X-API-Key`) |
| `PATCH` | `/tasks/{id}` | Update task details or completion status | Yes (`X-API-Key`) |
| `DELETE` | `/tasks/{id}` | Delete a task | Yes (`X-API-Key`) |
| `GET` | `/external/weather` | Fetch weather summary for a city | No |
| `GET` | `/external/random-scripture` | Fetch a daily or random scripture verse | No |

---

## Running the Morning Digest Job

To execute the digest generation and dispatch the email immediately:

```bash
# Run as a Python module from project root
uv run python -m app.jobs.send_digest
# or
python -m app.jobs.send_digest
```

### Cron Job Scheduling (Linux / Server)

To automate the delivery every morning at 7:00 AM:

```bash
# Open crontab editor
crontab -e

# Run every day at 07:00
0 7 * * * cd /path/to/Dagur && /path/to/Dagur/.venv/bin/python -m app.jobs.send_digest >> /var/log/dagur.log 2>&1
```

---

## Running Tests

```bash
pytest
```