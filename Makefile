start:
	@manage.py runserver 0.0.0.0:8000 --settings=config.settings.base

start-prod:
	@gunicorn --bind 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=config.settings.production config.wsgi --daemon
	@echo "Started gunicorn server"

stop-prod:
	@pkill -f gunicorn

migration:
	@manage.py makemigrations

migrate:
	@manage.py migrate

test:
	@coverage erase
	@coverage run -m pytest
	@coverage html
	@coverage report -m
	@flake8
