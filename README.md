# Dagur ☀️

**Dagur** (Old Norse / Icelandic for *"Day"*) is a personal morning briefing and task management API built with **FastAPI** and **SQLite**. It aggregates your pending tasks, scrapes or fetches current weather forecasts, and delivers a curated morning digest email right to your inbox at 7:00 AM.

---

## 🚀 Features

- **Task Management**: RESTful endpoints to create, list, complete, and delete personal tasks stored in a local SQLite database.
- **Weather Fetcher / Scraper**: Service to gather current temperatures, conditions, and daily forecasts.
- **Morning Digest Engine**: Assembles pending to-dos, weather forecasts, and custom morning insights into a clean email format.
- **Email Delivery Service**: Configurable SMTP email client to dispatch the digest.
- **Cron Automation**: Lightweight script / endpoint designed to run via scheduled cron jobs (e.g., every morning at 7:00 AM).
- **Protected Endpoints**: API key dependency verification to secure administrative and trigger endpoints.

---

## 📁 Project Structure

```text
Dagur/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entrypoint & router registrations
│   ├── database.py          # SQLAlchemy engine, session maker, & base model
│   ├── dependencies.py      # Dependency injections (DB session, API key auth)
│   ├── models.py            # Database tables and Pydantic schemas (DTOs)
│   ├── schemas.py            
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py         # Task CRUD endpoints (add, list, complete, delete)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── weather.py       # Weather data scraping / API client
│   │   ├── email.py         # SMTP email sender (smtplib / email.message)
│   │   └── digest.py        # Compiles weather + tasks into formatted email body
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

## 🛠️ Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/)
- **Database**: [SQLite](https://www.sqlite.org/) with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **HTTP & Scraping**: [HTTPX](https://www.python-httpx.org/) & [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- **Testing**: [pytest](https://docs.pytest.org/)

---

## 🏁 Getting Started

### 1. Prerequisites
- Python 3.10+ (Recommended: Python 3.13+)
- `uv` (recommended) or standard `pip` / `venv`

### 2. Environment Setup

Clone the repository and create a virtual environment:

```bash
# Using uv:
uv venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux

# Using python venv:
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate # macOS/Linux
```

Install dependencies:

```bash
# Using pip:
pip install -r requirements.txt

# Or using uv:
uv sync
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your settings:

```bash
cp .env.example .env
```

Ensure you configure:
- `API_SECRET_KEY`: Secret token for securing endpoints.
- `DATABASE_URL`: Defaults to `sqlite:///./dagur.db`.
- `WEATHER_CITY`: Target city for weather forecast.
- `SMTP_*` & `EMAIL_*`: Credentials for your email provider (e.g. Gmail App Password).

---

## 🏃 Running the Application

Start the local development server:

```bash
# Using FastAPI CLI:
fastapi dev app/main.py

# Or using Uvicorn directly:
uvicorn app.main:app --reload
```

Once running, explore the interactive documentation:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints (Planned)

| Method | Endpoint | Description | Auth Required |
|---|---|---|---|
| `GET` | `/health` | Health check endpoint | No |
| `GET` | `/tasks` | List all pending / completed tasks | Optional / Yes |
| `POST` | `/tasks` | Create a new task | Optional / Yes |
| `PATCH`| `/tasks/{task_id}` | Update task status or details | Optional / Yes |
| `DELETE`| `/tasks/{task_id}` | Delete a task | Optional / Yes |
| `GET` | `/weather` | View current weather summary | No |
| `POST` | `/digest/send` | Manually trigger the morning digest email | Yes (`X-API-Key`) |

---

## ⏰ Cron Job Setup

To run the morning digest automatically every day at 7:00 AM on your deployed server:

```bash
# Open crontab editor
crontab -e

# Run via python job script at 07:00 every day
0 7 * * * cd /path/to/Dagur && /path/to/Dagur/.venv/bin/python -m app.jobs.send_digest >> /var/log/dagur.log 2>&1

# OR trigger via curl to your protected endpoint
0 7 * * * curl -X POST https://your-domain.com/digest/send -H "X-API-Key: your_secret_api_key_here"
```

---

## 🧪 Running Tests

```bash
pytest
```

---

### Notes
- Recommended build sequence: 1) Database & Models (`database.py`, `models.py`), 2) Task CRUD endpoints (`dependencies.py`, `routers/tasks.py`, `main.py`), 3) Individual Services (`weather.py`, `scripture.py`, `email.py`), 4) Digest Aggregator (`digest.py`), 5) Cron trigger script (`jobs/send_digest.py`), 6) Automated testing (`tests/`).
- Scripture service recommendation: Consider using a public Bible API (such as Bible-API.com or labs.bible.org) with `httpx` or a local list of verses/plans to retrieve a verse and reference of the day.