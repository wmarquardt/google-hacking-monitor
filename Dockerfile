FROM python:3.9-alpine

WORKDIR /code
COPY . /code

RUN apk update\
    && apk add --virtual build-dependencies libxml2-dev libxslt-dev gcc python3-dev libevent-dev g++\
    && pip install --upgrade pip\
    && pip install -r requirements.txt
