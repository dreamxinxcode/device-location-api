FROM python:3.11.0a1-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="${PYTHONPATH}:/usr/src/app"

WORKDIR /code

COPY . /code

RUN apt-get update \
    && pip3 install -r build/requirements.txt