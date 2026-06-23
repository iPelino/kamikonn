# KamiKonn

KamiKonn is a cross-university academic event discovery platform for Rwanda's 10 major Kigali universities.

## Tech Stack
- **Backend**: Django 5.2 LTS + DRF 3.15 (Python 3.12+)
- **Frontend**: React 19 + Vite 6.x + Tailwind CSS 4.x + shadcn/ui
- **Database**: PostgreSQL 16
- **Caching & Workers**: Redis + Celery
- **Infrastructure**: Docker + Docker Compose

## Quick Start (Development)

1. **Clone and Setup**
   ```bash
   git clone https://github.com/your-username/kamikonn.git
   cd kamikonn
   ```

2. **Environment Variables**
   ```bash
   cp .env.example .env
   ```

3. **Install Dependencies**
   - Install `uv` and `pnpm`.
   - Backend: `cd backend && uv sync`
   - Frontend: `cd frontend && pnpm install`

4. **Run Services**
   ```bash
   docker compose up --build
   ```

5. **Run Migrations**
   ```bash
   make migrate
   ```

## Development Commands
Check the `Makefile` for useful commands:
- `make shell` - Opens Django shell
- `make lint` - Runs Ruff and ESLint
- `make format` - Formats code
- `make test-backend` - Runs Pytest
- `make test-frontend` - Runs Vitest
