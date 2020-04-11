FROM node:10-slim AS vue-compiler

WORKDIR /usr/src/app
COPY ./kaye_tech/frontend/package* ./

RUN npm ci

COPY ./kaye_tech/frontend .

RUN npm run build



FROM python:3-slim AS static-collector
ENV DJANGO_SETTINGS_MODULE kaye_tech.custom_settings.static
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
RUN pip install django djangorestframework

WORKDIR /kaye_tech
COPY ./kaye_tech /kaye_tech
COPY --from=vue-compiler /usr/src/app/static frontend/static

RUN python3 manage.py collectstatic --no-input



FROM nginx:alpine

COPY --from=static-collector /kaye_tech/kaye_tech/static_root /var/kaye_tech/static_root
COPY nginx_static.conf /etc/nginx/conf.d/kaye_tech_static.conf
