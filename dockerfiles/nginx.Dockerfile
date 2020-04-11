FROM node:10-slim AS vue-compiler

WORKDIR /usr/src/app
COPY ./project_name/frontend/package* ./

RUN npm ci

COPY ./project_name/frontend .

RUN npm run build



FROM python:3.7-slim AS static-collector
ENV DJANGO_SETTINGS_MODULE project_name.custom_settings.static
ARG DJANGO_SECRET_KEY
ENV DJANGO_SECRET_KEY $DJANGO_SECRET_KEY
RUN pip install django djangorestframework

WORKDIR /project_name
COPY ./project_name /project_name
COPY --from=vue-compiler /usr/src/app/static frontend/static

RUN python manage.py collectstatic --no-input



FROM nginx:alpine

COPY --from=static-collector /project_name/project_name/static_root /var/project_name/static_root
COPY nginx_static.conf /etc/nginx/conf.d/project_name_static.conf
