FROM node:10-slim AS vue-compiler

WORKDIR /usr/src/app
COPY ./project_name/frontend/package* ./

RUN npm ci

COPY ./project_name/frontend .

RUN npm run build



FROM python:3.7-slim

RUN apt-get update && apt-get install -y gcc python3-dev

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /project_name

RUN pip install black
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv install --dev --system --ignore-pipfile --deploy

COPY ./project_name .
COPY --from=vue-compiler /usr/src/app/webpack-stats.json ./frontend/webpack-stats.json
