ifneq (${DJANGO_SECRET_KEY},)
  override DJANGO_SECRET_KEY:=${DJANGO_SECRET_KEY}
endif

ifneq (${SOCIAL_AUTH_GOOGLE_OAUTH2_KEY},)
  override SOCIAL_AUTH_GOOGLE_OAUTH2_KEY:=${SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}
endif

ifneq (${SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET},)
  override SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET:=${SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET}
endif

-include app.env

export DJANGO_SECRET_KEY
export SOCIAL_AUTH_GOOGLE_OAUTH2_KEY
export SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET


# LOCAL DEVELOPMENT COMMANDS #

build:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml build

up:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml up -d

down:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml down

migrate:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py migrate

local:
	cd kaye_tech && pipenv run python manage.py runserver 0.0.0.0:8000

test:
	cd kaye_tech && pipenv run python manage.py test --keepdb

check-migrations:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py makemigrations --check

makemigrations:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py makemigrations

superuser:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py createsuperuser

restart-django:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml up --no-deps --force-recreate -d django

npm-install:
	cd kaye_tech/frontend; npm install

npm-build:
	npm run --prefix kaye_tech/frontend build

frontend-dev:
	cd kaye_tech/frontend; npm run dev

collect-static:
	pipenv run python kaye_tech/manage.py collectstatic

rollback-backend:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py migrate backend zero

lint:
	cd kaye_tech/frontend; npm run format

data-dump:
	cd kaye_tech && pipenv run python manage.py dumpdata --exclude=contenttypes --all --output backend/fixtures/dump.json

db-backup:
	cd kaye_tech/backend/fixtures/ && scp mattalexkaye:/home/projects/kaye-tech/kaye_tech/backend/fixtures/db.sqlite3 db-copy

# PRODUCTION COMMANDS #

build-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml build

up-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml up -d

migrate-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml exec django python manage.py migrate

down-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml down

requirements:
	pipenv run pip freeze > kaye_tech/requirements.txt

lint-python:
	pipenv run isort .
	pipenv run black --exclude migrations .

check-mypy:
	pipenv run mypy offline_conversions/backend/platforms offline_conversions/backend/job.py

check-isort:
	pipenv run isort . --check --skip migrations

check-flake8:
	pipenv run flake8 offline_conversions/backend/ --extend-exclude=migrations,imports.py

check-black:
	pipenv run black --check --exclude migrations .

check-python:
	make check-mypy
	make check-isort
	make check-black
	make check-flake8
	@printf '\033[92m\033[1m ✅  All Python Checks Passed 👍\033[0m\n'
