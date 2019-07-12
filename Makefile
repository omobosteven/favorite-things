pipenv-install:
	pipenv install -e .

start:
	@cd server; manage.py runserver 0.0.0.0:8000 --settings=config.settings.base

start-gunicorn:
	@cd server; gunicorn --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi --daemon

stop-gunicorn:
	@cd server; pkill -f gunicorn

migration:
	@cd server; manage.py makemigrations

migrate:
	@cd server; manage.py migrate

test:
	@cd server; coverage erase
	@cd server; coverage run -m pytest
	@cd server; coverage report -m
	@cd server; flake8

test-html-coverage:
	@cd server; coverage html

start-client:
	@cd client; npm run serve

build-client:
	@cd client; npm run build

start-client-prod:
	@cd client; npm run start
