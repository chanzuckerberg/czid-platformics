FROM python:3.11-slim-bookworm 

RUN apt-get update && \
    apt-get install -y \
      python3-pip nginx nginx-extras procps git

ENV POETRY_VERSION=1.5
# Some base python dependencies to kickstart our container build.
RUN python3 -m pip install --no-cache-dir poetry==$POETRY_VERSION supervisor

RUN poetry config virtualenvs.create false 

RUN mkdir -p /workflows
WORKDIR /workflows

ENV PYTHONPATH=.

COPY workflows/pyproject.toml workflows/poetry.lock ./
RUN poetry install

# Ordering is important here. Entities first!
COPY workflows/ .
COPY platformics ./platformics

RUN pip install plugins/*/*
RUN pip install git+https://github.com/chanzuckerberg/miniwdl-viz.git

CMD ["/usr/local/bin/supervisord", "-c", "/workflows/etc/supervisord.conf"]
