.PHONY: dev build migrate shell seed test lint format backend-shell setup

# Setup
setup:
	cp .env.example .env
	cd backend && uv sync
	cd frontend && pnpm install
	$(MAKE) hooks
	$(MAKE) migrate

hooks:
	pre-commit install
	pre-commit install --hook-type commit-msg
	git config commit.template .github/commit_template.txt

# Docker Services
dev:
	docker compose up

build:
	docker compose up --build

down:
	docker compose down

# Backend specific
migrate:
	docker compose exec backend uv run python manage.py migrate

makemigrations:
	docker compose exec backend uv run python manage.py makemigrations

shell:
	docker compose exec backend uv run python manage.py shell_plus

backend-shell:
	docker compose exec backend bash

seed:
	docker compose exec backend uv run python scripts/seed_data.py

test-backend:
	docker compose exec backend uv run pytest

# Frontend specific
test-frontend:
	docker compose exec frontend pnpm test

# Linting
lint:
	cd backend && uv run ruff check .
	cd frontend && pnpm lint

format:
	cd backend && uv run ruff format .
	cd frontend && pnpm prettier --write .
