FROM python:3.14-alpine

ENV TZ="Europe/Brussels"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apk add --no-cache --update npm

WORKDIR /app

COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev --group prod --no-install-project

COPY . /app

RUN uv run --no-sync python manage.py tailwind install
RUN uv run --no-sync python manage.py tailwind build
RUN uv run --no-sync python manage.py collectstatic --noinput

CMD ["sh", "runserver"]
