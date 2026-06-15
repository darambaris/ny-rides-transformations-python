## NY Rides - Pipeline Transformations

Modern data platform for NYC Taxi trip analytics with layered architecture, data contracts, quality monitoring, lineage tracking, and AI-assisted pipeline health assessment.


## Running Locally

### Install dependencies

```bash
poetry install
```

### Run tests

```bash
poetry run pytest
```

### Run coverage

```bash
poetry run pytest --cov=ny_rides --cov-report=term-missing
```