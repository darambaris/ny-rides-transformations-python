.PHONY: install test coverage lint format download-files build-silver

RAW_PATH ?= data/raw
SILVER_PATH ?= data/silver

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

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info

download-files:
	poetry run python -m ny_rides.jobs.download_files \
		--start-date 2025-01-01 \
		--end-date 2025-05-31 \
		--output-dir $(RAW_PATH)

build-silver:
	poetry run python -m ny_rides.jobs.build_silver \
		--raw-path $(RAW_PATH) \
		--silver-path $(SILVER_PATH)