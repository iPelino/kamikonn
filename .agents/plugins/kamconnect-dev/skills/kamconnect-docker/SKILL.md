---
name: kamconnect-docker
description: Standardized way to build and run the KamConnect Docker environment.
---

# KamConnect Docker Workflow

When managing the KamConnect environment, use these standards:

1. Use `docker compose up --build -d` to spin up both frontend and backend.
2. The backend runs on port 8000.
3. The frontend runs on port 5173.
4. Always tail logs using `docker compose logs -f <service_name>`.
