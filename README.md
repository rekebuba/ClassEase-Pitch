# ClassEase

ClassEase is a modern school management platform for running core academic and administrative workflows in one place. It helps schools manage academic years, grades, subjects, student registrations, employee onboarding, authentication, and role-based access through a full-stack web application.

This repository contains the current ClassEase implementation:

- A FastAPI backend with PostgreSQL, Redis, Alembic migrations, and automated tests
- A React + Vite frontend with TanStack Router, React Query, Redux Persist, and a generated OpenAPI client
- Docker-based local development and production-style container builds

## Why ClassEase

Schools often have critical data spread across spreadsheets, paper forms, and disconnected tools. ClassEase is designed to centralize that work into a single system that is easier to operate, safer to manage, and more scalable over time.

Core goals of the platform:

- Reduce administrative overhead for academic operations
- Improve the accuracy and consistency of student and staff records
- Support secure, role-based access for admins, teachers, and students
- Provide a foundation for reporting, academic tracking, and future automation

## Current Product Scope

The current implementation is strongest in the admin experience and core school setup workflows. In particular, the project already includes:

- Authentication with password login, Google login, logout, email verification, and password recovery
- Academic year creation and setup
- Grade and subject configuration
- Student and employee registration flows
- Admin dashboards and management screens
- Generated frontend API bindings from the backend OpenAPI schema

Some teacher and student-facing areas are still evolving, so contributors should expect the platform to be under active development rather than feature-complete.

## Architecture

At a high level, the system follows this flow:

1. Administrators create and manage academic years
2. Each year is configured with grades, subjects, streams, and sections
3. Students and employees are registered into the system
4. Users authenticate and access the application according to their role

The repository is organized as a monorepo with separate frontend and backend applications:

```text
ClassEase-Pitch/
├── app/
│   ├── backend/   # FastAPI app, models, migrations, tests
│   └── frontend/  # React/Vite app, routes, UI, generated client
├── docker-compose.yml
├── docker-compose.test.yml
└── .github/workflows/
```

## Tech Stack

### Frontend

- React 19
- Vite
- TypeScript
- TanStack Router
- TanStack React Query
- Redux Toolkit + Redux Persist
- React Hook Form + Zod
- Tailwind CSS and component primitives

### Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Redis
- Alembic
- JWT authentication

### Tooling

- Docker and Docker Compose
- Pytest
- ESLint
- Ruff
- OpenAPI code generation with `@hey-api/openapi-ts`

## Repository Layout

### Backend

`app/backend/src/project/`

- `main.py`: FastAPI application entry point
- `api/v1/routers/`: versioned API endpoints
- `models/`: SQLAlchemy models for the school domain
- `schema/`: response and domain schemas
- `core/`: configuration, database, and security utilities
- `templates/`: email templates and seeded defaults

### Frontend

`app/frontend/src/`

- `main.tsx`: frontend application bootstrap
- `routes/`: file-based routing for the application
- `components/`: reusable UI and domain components
- `store/`: persisted client state
- `lib/`: shared frontend utilities and API wiring
- `client/`: generated SDK, React Query hooks, and Zod schemas from OpenAPI

## Getting Started

### Prerequisites

Recommended:

- Docker
- Docker Compose

For manual local development:

- Python 3.12+
- Node.js 24+
- `pnpm` via Corepack
- PostgreSQL
- Redis

## Quick Start With Docker

Docker Compose is the easiest way to run the full stack locally.

1. Review the environment files in `app/backend/`:

   - `.env.development`
   - `.env.testing`
   - `.env.production`

2. Start the application:

   ```bash
   docker compose up --build
   ```

3. Open the services:

   - Frontend: `http://localhost:8081`
   - Backend API: `http://localhost:8080`
   - API docs: `http://localhost:8080/api/v1/docs`

The Compose stack starts:

- PostgreSQL on `localhost:5432`
- Redis on `localhost:6379`
- Backend on `localhost:8080`
- Frontend on `localhost:8081`

## Local Development Without Docker

### Backend

From `app/backend`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn project.main:app --reload --app-dir src --port 8080
```

Notes:

- The backend configuration loads from `.env.development` by default
- API docs are available at `http://localhost:8080/api/v1/docs`
- Alembic is used for schema migrations

### Frontend

From `app/frontend`:

```bash
corepack enable
pnpm install
VITE_API_BASE_URL=http://localhost:8080 pnpm dev
```

The Vite dev server runs on `http://localhost:5173` by default.

### Regenerate the Frontend API Client

If you change backend endpoints or schemas, regenerate the frontend client while the backend is running:

```bash
cd app/frontend
pnpm generate:client
```

This refreshes:

- generated SDK functions
- React Query hooks
- TypeScript types
- Zod validators

## Testing and Quality Checks

### Backend Tests

From `app/backend`:

```bash
pytest
```

The backend test suite covers important API flows including authentication, registration, and academic-year management.

### Frontend Linting

From `app/frontend`:

```bash
pnpm lint
```

### Optional Git Hooks

If you use pre-commit locally:

```bash
pre-commit install
```

There are pre-commit configurations in the repository to help catch formatting and lint issues early.

## API and Authentication

The backend exposes a versioned REST API under `/api/v1`.

Key capabilities include:

- credential login
- provider login via Google
- email verification
- password recovery and reset
- JWT-based authorization
- role-based access controls for admin, teacher, and student users

In development and testing environments, OpenAPI docs are available at:

- `http://localhost:8080/api/v1/docs`
- `http://localhost:8080/api/v1/redoc`

## Contributing

Contributions are welcome. If you want to improve ClassEase, please keep changes focused, well-tested, and aligned with the current architecture.

Recommended workflow:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the relevant checks
5. Open a pull request with a clear summary

Before opening a PR, please:

- run backend tests if you changed backend behavior
- run frontend linting if you changed frontend code
- add or update tests for important logic changes
- regenerate the frontend API client if backend contracts changed
- include Alembic migrations if your backend model changes require schema updates

### Contribution Guidelines

- Prefer small, reviewable pull requests
- Keep documentation updated when workflows change
- Avoid breaking generated client contracts without updating the frontend
- Follow the existing project structure instead of introducing parallel patterns

## Deployment Notes

The repository includes:

- production-oriented Dockerfiles for both backend and frontend
- GitHub Actions workflows under `.github/workflows/`

Those workflows can serve as a starting point for CI/CD, image publishing, and deployment automation.

## Project Status

ClassEase is under active development. The current codebase already supports meaningful admin and school setup workflows, while broader teacher and student experiences continue to mature.

## License

This repository does not currently include a license file. If you plan to reuse or redistribute the project, please confirm the licensing terms with the repository owner first.
