.PHONY: install test coverage lint format download-files

install:
	poetry install

test:
	poetry run pytest -vv

coverage:
	poetry run pytest --cov=ny_rides --cov-report=term-missing

lint:
	poetry run ruff check .

format:
	poetry run ruff format .

download-files:
	poetry run python -m ny_rides.jobs.download_files \
		--start-date 2021-01-01 \
		--end-date 2021-12-31