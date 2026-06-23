# KamiKonn Agent Instructions

This file contains the core context, architectural boundaries, and guidelines for AI coding agents working on the KamiKonn monorepo.

## 1. Project Context
* **What it is:** KamiKonn is a cross-university academic event discovery platform for Rwanda's 10 major Kigali universities.
* **Architecture:** A monorepo combining a Django REST Framework backend with a React + TypeScript frontend (Vite), deployed on DigitalOcean VPS with Docker.

## 2. Tech Stack Constraints
### Backend (Django REST Framework)
* **Framework:** Django 5.2 LTS + DRF 3.15 (Python 3.12+)
* **Database:** PostgreSQL 16 (Use `SearchVector` and `pg_trgm` for search; no Elasticsearch)
* **Auth:** djangorestframework-simplejwt (Stateless JWT) + django-allauth + dj-rest-auth (Google OAuth)
* **Security:** django-ratelimit, django-cors-headers, nh3 (HTML sanitization), CSP headers, email verification required
* **Background Tasks:** Celery + Redis
* **Documentation:** drf-spectacular for OpenAPI docs
* **Dependencies:** Managed via `uv` (not pip)

### Frontend (React + TypeScript)
* **Framework:** React 19 + Vite 6.x
* **Language:** TypeScript 5.6+ (Strict mode must be maintained, avoid `any`)
* **Styling:** Tailwind CSS 4.x + shadcn/ui. **DO NOT** use Material UI or Bootstrap.
* **State Management:** TanStack Query v5 (server state) + Zustand 5.x (client state). **DO NOT** use Redux.
* **Routing:** React Router v7
* **Forms:** React Hook Form + Zod for validation
* **i18n:** react-i18next (English only for v1, scaffolded for Kinyarwanda/French)
* **PWA:** vite-plugin-pwa for service worker and Add to Home Screen
* **Theme:** Light + Dark mode with system preference toggle

## 3. Workflow & Guidelines
* **Structure:** `backend/` contains Django project; `frontend/` contains React app.
* **UI/UX:** Always adhere to `kamikonn_brand_identity.md` for styling and color palettes.
* **Testing:** pytest + factory-boy (backend), Vitest + React Testing Library (frontend), Playwright E2E (Phase 3+).
* **Docker:** Ensure new services are added to `docker-compose.yml`.

## 4. Communication Rules
* **Never use emojis** in responses, code comments, commit messages, or documentation unless the user explicitly instructs otherwise.

## 5. Key Architecture Decisions
* **User Roles:** User, Organizer (profile add-on flag), University Moderator (Django group), Admin.
* **Event-University Relationship:** ManyToMany (supports joint cross-university events).
* **Event Publishing:** Hybrid model -- anyone submits drafts, university moderators + admins approve, auto-trust after 3+ clean events.
* **University Management:** Full CRUD API + frontend UI (not just Django Admin).
* **Payments:** Display price + external payment link only. Full MoMo integration deferred.
* **Event Media:** Single banner image for v1. Gallery + video deferred.
* **Event Ingestion:** Manual wizard + CSV bulk import. Public API deferred.

## 6. CI/CD & Operations Rules
* **Pre-commit Hooks:** Always run `pre-commit run --all-files` locally and explicitly stage/commit any files that are auto-fixed by hooks (like `ruff`, `end-of-file-fixer`, `trailing-whitespace`) before pushing.
* **Pytest Discovery & Coverage:**
  * Always ensure new test files are discoverable by configuring `python_files` in `pyproject.toml` (e.g., to include `tests.py`).
  * Never leave a test suite completely empty as Pytest will exit with code 5, failing the CI.
  * Ensure scaffolding and config files (`manage.py`, `asgi.py`, `settings/*`) are excluded from coverage calculations to prevent false-positive coverage drops.
* **GitHub Actions:** Do not use `paths` filters on `pull_request` triggers if branch protection mandates those status checks to pass. This causes PRs (like those from Dependabot) to hang indefinitely in a "Pending" state if they modify unfiltered files.
* **Branch Discipline:** Never commit directly to `main` or `develop` (which triggers the `no-commit-to-branch` pre-commit hook failure). Always create a feature or chore branch and open a PR.

## 7. AI Agent PR Workflow
To prevent persistent merge conflicts (especially with `pnpm-lock.yaml`, `package.json`, and `.secrets.baseline`) caused by rapidly creating multiple parallel pull requests:
* **The "Stacked PRs" Strategy:** If executing a sequence of tasks that touch overlapping configs, branch off the *previous feature branch* rather than `develop` so changes accumulate linearly.
* **The "Batched Epic" Strategy:** Alternatively, group multiple related smaller issues into a single branch (e.g. `feature/issues-44-45-46-setup`) and open one consolidated PR.
* **Baseline Discipline:** Do not arbitrarily regenerate `.secrets.baseline` using `detect-secrets scan` on feature branches if `pre-commit` fails. If a false positive is introduced, mark it inline with `# pragma: allowlist secret`. Baseline regeneration should generally be restricted to the `develop` branch or automated CI.
