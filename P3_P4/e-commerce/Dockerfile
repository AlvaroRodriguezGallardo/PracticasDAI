# Dockerfile
FROM python:3.11-alpine

WORKDIR /e-commerce
COPY . /e-commerce

RUN apk add zlib-dev jpeg-dev gcc musl-dev
RUN pip install -r requirements.txt

