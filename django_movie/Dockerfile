FROM python:3.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /track

COPY requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install --upgrade pip \
    && pip install --default-timeout=100 -r requirements.txt


COPY . .

ENV DJANGO_SETTINGS_MODULE track.settings

EXPOSE 8000