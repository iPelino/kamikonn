FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install uv
RUN pip install uv

COPY pyproject.toml ./

# Install dependencies using uv
RUN uv sync --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
