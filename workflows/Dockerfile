FROM python:3.11-slim-bookworm 

RUN apt-get update && \
    apt-get install -y \
      python3-pip nginx nginx-extras procps

ENV POETRY_VERSION=1.5
# Some base python dependencies to kickstart our container build.
RUN python3 -m pip install --no-cache-dir poetry==$POETRY_VERSION supervisor

RUN poetry config virtualenvs.create false 

RUN mkdir -p /workflows
WORKDIR /workflows

ENV PYTHONPATH=.

COPY workflows/pyproject.toml workflows/poetry.lock ./
RUN poetry install

# Ordering is important here. Workflows first!
COPY workflows/ .
COPY platformics ./platformics

RUN pip install plugins/*/*

CMD ["/usr/local/bin/supervisord", "-c", "/workflows/etc/supervisord.conf"]
