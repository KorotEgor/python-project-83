PORT ?= 8000

install:
	poetry install

lint:
	poetry run ruff format && uv run ruff check

db:
	sudo service postgresql start

build:
	./build.sh

dev:
	poetry run flask --app page_analyzer:app run

start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
