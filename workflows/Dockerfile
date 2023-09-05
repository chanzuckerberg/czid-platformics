FROM python:3.11-slim-bookworm 

RUN apt-get update && \
    apt-get install -y \
      python3-pip \
      postgresql-15

ENV POETRY_VERSION=1.5
# Some base python dependencies to kickstart our container build.
RUN python3 -m pip install --no-cache-dir poetry==$POETRY_VERSION supervisor

RUN poetry config virtualenvs.create false 

RUN mkdir -p /workflows
WORKDIR /workflows

ENV PYTHONPATH=.

COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY . ./

RUN pip install plugins/*/*
