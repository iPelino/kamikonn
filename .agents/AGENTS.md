# KamConnect Agent Instructions

This file contains the core context, architectural boundaries, and guidelines for AI coding agents working on the KamConnect monorepo.

## 1. Project Context
* **What it is:** KamConnect is a cross-university academic event discovery platform for Rwanda's 10 major Kigali universities.
* **Architecture:** A monorepo combining a Django REST Framework backend with a React + TypeScript frontend (Vite), deployed on DigitalOcean VPS with Docker.

## 2. Tech Stack Constraints
### Backend (Django REST Framework)
* **Framework:** Django 5.2 LTS + DRF 3.15 (Python 3.12+)
* **Database:** PostgreSQL 16 (Use `SearchVector` and `pg_trgm` for search; no Elasticsearch)
* **Auth:** djangorestframework-simplejwt (Stateless JWT)
* **Background Tasks:** Celery + Redis
* **Documentation:** drf-spectacular for OpenAPI docs

### Frontend (React + TypeScript)
* **Framework:** React 19 + Vite 6.x
* **Language:** TypeScript 5.6+ (Strict mode must be maintained, avoid `any`)
* **Styling:** Tailwind CSS 4.x + shadcn/ui. **DO NOT** use Material UI or Bootstrap.
* **State Management:** TanStack Query v5 (server state) + Zustand 5.x (client state). **DO NOT** use Redux.
* **Routing:** React Router v7
* **Forms:** React Hook Form + Zod for validation

## 3. Workflow & Guidelines
* **Structure:** `backend/` contains Django project; `frontend/` contains React app. 
* **UI/UX:** Always adhere to `kamconnect_brand_identity.md` for styling and color palettes.
* **Testing:** Use Vitest for the frontend.
* **Docker:** Ensure new services are added to `docker-compose.yml`.
