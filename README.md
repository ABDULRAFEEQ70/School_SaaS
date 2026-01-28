# School_SaaS

A small Flask-based School SaaS backend providing authentication, student/course/class management, attendance, grades, and integrations (OpenAI). This README covers local development (Windows PowerShell), Docker, database migrations, and Celery worker setup.

## Prerequisites

- Python 3.11+ installed and on PATH
- Git (optional)
- Docker & Docker Compose (optional, for containerized setup)
- A broker for Celery (e.g., Redis, RabbitMQ) if using async tasks


## Project layout (key files)

- `app.py` - Flask application, extension initializations, blueprint registrations, Celery setup
- `routes.py` / `routes/` - API endpoints (auth, students, teachers, classes, admin, etc.)
- `services.py` - Business logic/services
- `models.py` - SQLAlchemy models
- `config.py` - Configuration class reading environment variables
- `requirements.txt` - Python dependencies
- `Dockerfile`, `docker-compose.yml` - Containerization


## Environment variables

The app loads configuration from environment variables (see `config.py`). Typical variables you'll need:

- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT secret
- `SQLALCHEMY_DATABASE_URI` - Database connection string (e.g., `sqlite:///data.db` or a Postgres URL)
- `CELERY_BROKER_URL` - e.g., `redis://localhost:6379/0`
- `OPENAI_API_KEY` - (optional) OpenAI API key
- `OPENAI_MODEL` - (optional) model name to use (e.g., `gpt-5-mini`)

A `.env.example` is included with placeholders you can copy to `.env`.


## Quick start — Windows PowerShell (local)

1. Clone repo (optional):

```powershell
git clone <repo-url> .
```

2. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

4. Create an `.env` file from the example and fill the values:

```powershell
copy .env.example .env
# then open .env in an editor and set values
```

5. Export `FLASK_APP` for migrations and CLI (current session):

```powershell
$env:FLASK_APP = 'app.py'
```

6. Run database migrations (first time only):

```powershell
flask db init        # only once
flask db migrate -m "Initial migration"
flask db upgrade
```

7. Run the app:

```powershell
python app.py
# or
flask run --host=0.0.0.0 --port=5000
```

The API will be available at http://127.0.0.1:5000 or the host you specify.


## Running Celery worker (local)

Ensure your `CELERY_BROKER_URL` is set (e.g., Redis). Then, from the activated virtualenv:

```powershell
# From project root with venv activated
celery -A app.celery worker --loglevel=info
```

Adjust the `-A` argument if your Celery instance is defined differently. The repo uses `celery = Celery(...)` in `app.py`, so `app.celery` should work.


## Docker (optional)

To run with Docker Compose (build and start):

```powershell
# ensure Docker Desktop is running
docker compose up --build -d
```

View logs:

```powershell
docker compose logs -f
```

If you need environment variables in the compose file, add them to the service's `environment:` section or use an env-file.


## Common troubleshooting

- "Module not found" errors: ensure virtualenv is activated and `pip install -r requirements.txt` succeeded.
- Docker build fails: confirm Docker Desktop is running, check the Dockerfile and `docker compose` logs for full error message.
- Flask-Migrate errors: ensure `FLASK_APP` is set to `app.py` and that your models are importable from the app context.
- Celery can't connect to broker: verify `CELERY_BROKER_URL` and that the broker service (Redis/RabbitMQ) is running and reachable.


## Security notes

- Do not commit real secrets or API keys. Use `.env` (kept out of VCS) and add `.env` to `.gitignore`.
- Rotate keys and use least-privilege API keys for production.


## Next steps I can help with

- Patch `config.py` to list required env vars and provide defaults where appropriate.
- Add a `Makefile` or PowerShell script to automate setup steps.
- Wire `OPENAI_MODEL` usage consistently across the codebase and add tests.

If you'd like, tell me which of the above I should do next and I will apply the changes.
