# Alcovia AI Content API

FastAPI service that lets authenticated users upload short-form text, generates an AI-powered summary and sentiment analysis, and stores everything in a relational database. The project demonstrates JWT authentication, asynchronous processing, Hugging Face integration, containerization, and a CI/CD pipeline ready for GCP.

## Tech Stack

- FastAPI (Python 3.11) with async SQLAlchemy + PostgreSQL (SQLite fallback for local dev)
- Hugging Face Inference API (BART summarization + RoBERTa sentiment) with heuristic fallback
- JWT auth via `python-jose`, password hashing via `passlib[bcrypt]`
- Docker for containerization
- GitHub Actions CI (unit smoke test + Docker build)

## Setup Instructions

### 1. Clone & Install (local)

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment

Create a `.env` file with the following keys:

```
DATABASE_URL=postgresql+psycopg_async://user:pass@localhost:5432/alcovia
SECRET_KEY=super-secret-key
HUGGINGFACE_API_KEY=hf_xxx   # optional but recommended
```

> No Hugging Face key → the service falls back to a lightweight heuristic summarizer/sentiment estimator so the API stays functional in development.

### 3. Run Locally

```bash
uvicorn app.main:app --reload
```

Visit `http://localhost:8000/docs` for interactive Swagger docs.

### 4. Docker (containerized run)

```bash
docker build -t alcovia-api .
docker run --env-file .env -p 8000:8000 alcovia-api
```

## API Documentation

- `POST /auth/register` – create user (email + password)
- `POST /auth/login` – receive JWT access token
- `POST /contents` – submit text, triggers AI summary + sentiment (requires Bearer token)
- `GET /contents` / `GET /contents/{id}` – list or fetch content created by the authenticated user
- `PUT /contents/{id}` – edit title/body, re-runs AI pipeline
- `DELETE /contents/{id}` – remove content

➡️ Swagger UI available at `http://localhost:8000/docs` (FastAPI auto-generated).

Use the returned JWT in `Authorization: Bearer <token>` header for protected endpoints.

## Design Decisions

### Database

- Chose PostgreSQL for transactional consistency, rich JSON/text support, and easy managed hosting on GCP Cloud SQL; SQLite remains the default for lightweight local development.  
- Async SQLAlchemy engine (`AsyncSession`) keeps DB IO off the event loop threads so FastAPI can scale with minimal latency.  
- Migrations can be added with Alembic if the schema begins to evolve quickly.

### AI Integration

- Leveraged Hugging Face Inference API for best-in-class pretrained summarization (BART) and sentiment (RoBERTa) without managing GPUs ourselves.  
- `app/ai_service.py` issues concurrent requests via `asyncio.gather`, so the endpoint stays responsive while both models run.  
- Deterministic fallback heuristics keep the endpoint useful when the API key is missing or rate-limited, which is essential for local development and testing.

## Security

- Passwords hashed with bcrypt.
- JWT access tokens (HS256) include a 30-minute default expiry; tune via `ACCESS_TOKEN_EXPIRE_MINUTES`.
- Secrets/database credentials are never committed; set them through `.env` locally and environment variables in CI/CD.

## CI/CD

`.github/workflows/ci.yml` runs on every push/PR to `main`:

1. Spins up PostgreSQL service, installs dependencies, runs `python -m compileall` as a static check, and executes an async DB smoke test (ensures migrations + models align).  
2. Builds the Docker image to catch Docker regressions early.

## GCP Architecture (theoretical deployment)

1. **Artifact Build:** GitHub Actions builds and pushes the container to Artifact Registry using a service account key stored in repository secrets.  
2. **Infrastructure:** Use Terraform or gcloud CLI to create a Cloud SQL (PostgreSQL) instance and a Cloud Run service. Store secrets in Secret Manager and mount them as environment variables.  
3. **Release:** After CI succeeds, trigger a deploy job (`gcloud run deploy alcovia-api --image=... --region=us-central1 --set-env-vars=...`). Cloud Run provides HTTPS out of the box and scales to zero.  
4. **Networking & Observability:**  
   - Use Cloud Armor or IAP for additional auth policies if needed.  
   - Export logs/metrics to Cloud Logging & Cloud Monitoring, set alerts on 5xx error rate and response latency.  
5. **Future Enhancements:** Add Pub/Sub or Cloud Tasks if AI inference should be offloaded to a worker, allowing the API to respond immediately with a job ID.

---

You now have a complete, cloud-ready, AI-enabled REST API scaffolded and ready for iteration. Happy hacking!

