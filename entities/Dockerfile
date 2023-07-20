FROM python:3.11-slim-bookworm AS build
RUN apt-get update && apt-get install -y vim wget nginx nginx-extras procps ripgrep make && apt-get clean
ENV POETRY_VERSION=1.5
# Some base python dependencies to kickstart our container build.
RUN python3 -m pip install --no-cache-dir poetry==$POETRY_VERSION supervisor

RUN mkdir -p /czid-platformics/entities
WORKDIR /czid-platformics/entities

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false

ENV PYTHONPATH=.

COPY . .
RUN poetry install
CMD ["/usr/local/bin/supervisord", "-c", "/czid-platformics/entities/etc/supervisord.conf"]
