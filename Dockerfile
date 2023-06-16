FROM python:3.10-alpine

COPY . .

RUN apk add --no-cache --virtual .build-deps python3 py3-pip false musl-dev postgresql-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt