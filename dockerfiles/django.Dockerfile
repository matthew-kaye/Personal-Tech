FROM node:10-slim AS vue-compiler

WORKDIR /usr/src/app
COPY ./kaye_tech/frontend/package* ./

RUN npm ci

COPY ./kaye_tech/frontend .

RUN npm run build



FROM python:3-slim

RUN apt-get update && apt-get install -y gcc python3-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /kaye_tech

RUN pip install black
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --dev --system --ignore-pipfile --deploy

COPY ./kaye_tech .
COPY --from=vue-compiler /usr/src/app/webpack-stats.json ./frontend/webpack-stats.json
