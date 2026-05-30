# Pub Quiz

A multiplayer-style "pub quiz" game built as a learning project for exploring Python and Django from a PHP/Laravel background. Questions are sourced from the [Open Trivia Database](https://opentdb.com/), with the API layer designed to be extensible to other providers.

The repository is split into a Django REST API backend and a React SPA frontend, orchestrated via Docker Compose. Both sides are built against a shared OpenAPI contract ([api-contract.yaml](api-contract.yaml)).

## Tech Stack

**Backend** ([backend/](backend/))
- Python 3 / Django 5
- Django REST Framework + drf-spectacular (OpenAPI/Swagger)
- PostgreSQL 16
- pytest, pytest-django, factory-boy

**Frontend** ([frontend/](frontend/))
- React 19 + TypeScript
- Vite, React Router, TanStack Query, Axios
- Tailwind CSS + DaisyUI
- Vitest (unit) and Cypress (component)

**Infrastructure**
- Docker & Docker Compose

## Project Structure

```
api-contract.yaml      # Shared OpenAPI contract
docker-compose.yml     # db, backend, frontend services
agents/                # Project plan, user journeys, agent guidance
backend/               # Django project (accounts, quiz, core apps)
frontend/              # React SPA
```

Key planning docs:
- [agents/AGENTS.md](agents/AGENTS.md) — architecture and standards
- [agents/implementation_plan.md](agents/implementation_plan.md) — phased build plan
- [agents/user_journeys.md](agents/user_journeys.md) — end-user flows

## Getting Started

### Prerequisites
- Docker and Docker Compose

### Run with Docker Compose

```bash
docker compose up --build -d
```

Services:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080/api
- PostgreSQL: localhost:5433 (host) → 5432 (container)

The backend reads env vars from `backend/.env.example` (committed) with optional overrides in `backend/.env`.

### Apply migrations and seed demo data

```bash
docker compose exec backend python manage.py migrate
docker compose exec backend python manage.py seed_demo
```

## Backend Development

Run from inside the `backend` container (or a local venv with `requirements.txt` installed):

```bash
# Run tests
pytest

```

Backend standards (see [agents/AGENTS.md](agents/AGENTS.md)):
- RESTful endpoints aligned with `api-contract.yaml`
- Slim views; logic in service classes; persistence via repository classes
- Global throttling — by IP for anonymous routes, by user id for authenticated routes
- Feature tests cover auth, validation, and responses; service tests cover logic and DB persistence using transactional rollback
- Swagger docs generated via drf-spectacular

## Frontend Development

Requires Node version 20.19 before running these commands

```bash
cd frontend
npm install
npm run dev          # Vite dev server - should already be started by frontend/Dockerfile
npm test             # Vitest unit tests
npm run cy:run       # Cypress component tests
npm run lint
```

Frontend standards:
- SPA consuming the backend as an API-only service
- JWT access tokens stored client-side and sent via `Authorization` header
- Refresh-token rotation on expiry
