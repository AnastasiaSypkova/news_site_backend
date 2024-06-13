# pull base python image
FROM python:3.12

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PIP_NO_CACHE_DIR=True
ENV POETRY_VIRTUALENVS_CREATE=False

RUN pip install \
    setuptools \
    wheel \
    poetry

# set work directory
WORKDIR /app

# create group and user without roots rights
RUN addgroup --system app && adduser --system --group app && \
    chown app /app && chgrp app /app

# install python dependences for django project via poetry
COPY ./pyproject.toml ./poetry.lock .
RUN poetry install && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts}

# copy files of django project
COPY . .

RUN chown -R app /app && chgrp -R app /app
USER app

# open port 8000
EXPOSE 8000
