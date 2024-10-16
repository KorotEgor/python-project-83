PORT ?= 8000

install:
	curl -LsSf https://astral.sh/uv/install.sh | sh

lint:
	uv run ruff format && uv run ruff check

dev:
	uv run flask --app page_analyzer:app run

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
