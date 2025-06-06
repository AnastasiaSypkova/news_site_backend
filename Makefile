.PHONY: run-server
run-server:
	poetry run python manage.py runserver

.PHONY: install
install:
	poetry install

.PHONY: migrate
migrate:
	poetry run python manage.py migrate

.PHONY: makemigrations
makemigrations:
	poetry run python manage.py makemigrations

.PHONY: update
update: install migrate;

.PHONY: startapp
startapp:
	poetry run python manage.py startapp $(name)

.PHONY: run-tests
run-tests:
	poetry run python manage.py test $(name)

.PHONY: createsuperuser
createsuperuser:
	poetry run python manage.py createsuperuser
