export DJANGO_ENV=development

migrate:
	cd kaye_tech && pipenv run python manage.py migrate

local:
	cd kaye_tech && pipenv run python manage.py runserver 0.0.0.0:8000

test:
	cd kaye_tech && pipenv run python manage.py test --keepdb

check-migrations:
	cd kaye_tech && pipenv run python manage.py makemigrations --check

makemigrations:
	cd kaye_tech && pipenv run python manage.py makemigrations

superuser:
	cd kaye_tech && pipenv run python manage.py createsuperuser


npm-install:
	cd kaye_tech/frontend; npm install

npm-build:
	npm run --prefix kaye_tech/frontend build

frontend-dev:
	npm run --prefix kaye_tech/frontend dev

collect-static:
	pipenv run python kaye_tech/manage.py collectstatic

rollback-backend:
	cd kaye_tech && pipenv run python manage.py migrate backend zero

lint:
	cd kaye_tech/frontend; npm run format

data-dump:
	cd kaye_tech && pipenv run python manage.py dumpdata --exclude=contenttypes backend.vendor backend.highscore --output backend/fixtures/dump.json

loaddata:
	cd kaye_tech && pipenv run python manage.py loaddata backend/fixtures/dump.json

db-backup:
	cd kaye_tech/backend/fixtures/ && scp mattalexkaye:/home/projects/kaye-tech/kaye_tech/backend/fixtures/db.sqlite3 db-copy

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

deploy:
	cd kaye_tech && eb deploy

browse:
	cd kaye_tech && eb open
