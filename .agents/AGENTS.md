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
