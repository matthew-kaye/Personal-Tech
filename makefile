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
	cd kaye_tech && pipenv run py manage.py runserver 0.0.0.0:8000

check-migrations:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py makemigrations --check

makemigrations:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py makemigrations

create-superuser:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py createsuperuser

restart-django:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml up --no-deps --force-recreate -d django

enums:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py runscript enum_setup

db-backup:
	bash db_backup_development.sh

npm-install:
	cd kaye_tech/frontend; npm install

frontend-dev:
	cd kaye_tech/frontend; npm run dev

rollback-backend:
	docker-compose -f docker-compose.yaml -f docker-compose.development.yaml exec django python manage.py migrate backend zero

lint:
	cd kaye_tech/frontend; npm run format


# PRODUCTION COMMANDS #

build-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml build

up-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml up -d

migrate-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml exec django python manage.py migrate

down-production:
	docker-compose -f docker-compose.yaml -f docker-compose.production.yaml down

db-backup-production:
	bash db_backup_production.sh

