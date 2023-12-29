FROM python:3.11.6

ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get install -y gettext wkhtmltopdf

COPY poetry.lock pyproject.toml /usr/src/app/

RUN pip3 install poetry --only main

RUN poetry install

COPY . .

RUN poetry run django-admin compilemessages
