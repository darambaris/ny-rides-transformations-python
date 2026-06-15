# NY Rides Transformations

Data Engineering challenge solution implementing a batch data pipeline for the NYC TLC Yellow Taxi dataset using Python and Apache Spark.

## Overview

The pipeline ingests raw taxi trip data, validates data contracts, executes quality checks, generates analytical datasets, and answers the business questions proposed in the challenge.

### Architecture

```text
Source
  ↓
Raw
  ↓
Silver
  ↓
Gold
  ↓
Analysis
```

A detailed explanation of the architecture, design decisions, assumptions, and trade-offs can be found in:

```text
docs/arch_decisions.md
```

---

## Features

### Ingestion

* Download TLC Yellow Taxi datasets
* Raw data preservation
* Partitioning by year and month
* Ingestion manifest generation

### Data Quality

* Contract validation
* Required column validation
* Data type validation
* Duplicate detection
* Null detection
* Temporal consistency checks
* Quality report generation

### Transformations

#### Silver Layer

* Required column selection
* Type standardization
* Derived columns:

  * pickup_year
  * pickup_month
  * trip_duration_minutes

#### Gold Layer

Generated analytical datasets:

* monthly_average_total_amount
* hourly_average_passenger_count

`hourly_average_passenger_count` is generated with:

* pickup_year
* pickup_month
* pickup_hour
* avg_passenger_count

---

## Project Structure

```text
ny-rides-transformations-python/

├── ny_rides/
│   ├── contracts/
│   ├── ingestion/
│   ├── jobs/
│   ├── metadata/
│   ├── quality/
│   ├── storage/
│   ├── data_transformations/
│   └── shared/
│
├── analysis/
├── docs/
├── tests/
│
├── data/
│   ├── raw/
│   ├── silver/
│   └── gold/
│
└── artifacts/
    ├── ingestion/
    └── quality/
```

---

## Requirements

* Python >= 3.12
* Java (set `JAVA_HOME` in `.env.local`)
* Poetry
* Docker (optional)

---

## Installation

```bash
poetry install
```

Configure environment variables for Spark/Java:

```bash
cp .env.example .env.local
# Edit .env.local and set JAVA_HOME for your machine
source .env.local
```

`JAVA_HOME` must be configured by each user/device. Typical values:

```bash
# macOS (Homebrew)
JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home

# Linux
JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
```

If `.env.local` is already tracked by git in your clone, untrack it once:

```bash
git rm --cached .env.local
```

Validate Java is available for Spark:

```bash
make setup-env
```

---

## Run Tests

```bash
make test
```

Current test coverage is approximately 84%.

---

## Execute Pipeline

Run the complete pipeline:

```bash
source .env.local
make generate-pipeline
```

Run with custom date range:

```bash
source .env.local
make generate-pipeline START_DATE=2025-05-01 END_DATE=2025-05-31
```

This command executes:

```text
Download Files
    ↓
Build Silver
    ↓
Build Gold
```

Generated outputs:

```text
data/raw
data/silver
data/gold

artifacts/ingestion
artifacts/quality
```

---

## Business Questions

### Question 1

What is the average total amount received per month considering all yellow taxis?

Answer generated from:

```text
data/gold/monthly_average_total_amount
```

---

### Question 2

What is the average passenger count by hour of day during May?

Answer generated from:

```text
data/gold/hourly_average_passenger_count
```

and analyzed in:

```text
analysis/
```

Run notebook locally:

```bash
source .env.local
# Open analysis/questions.ipynb in VS Code and run cells with the selected Poetry kernel
```

---

## Docker

Build image from Dockerfile:

```bash
docker build -f docker/Dockerfile -t ny-rides .
```

Run pipeline in a single container run:

```bash
docker run --rm ny-rides sh -lc 'make generate-pipeline START_DATE=2025-05-01 END_DATE=2025-05-31'
```

Recommended: use Docker Compose with persistent volumes (`data/` and `artifacts/`):

```bash
docker compose -f docker/docker-compose.yml run --rm ny-rides-pipeline
```

Run questions (Q1 and Q2) in Docker after pipeline:

```bash
docker compose -f docker/docker-compose.yml run --rm ny-rides-questions
```

Run pipeline with custom dates in Docker Compose:

```bash
docker compose -f docker/docker-compose.yml run --rm -e START_DATE=2025-05-01 -e END_DATE=2025-05-31 ny-rides-pipeline
```

---

## Future Improvements

* End-to-end integration tests
* Cloud object storage support (S3, GCS, ADLS)
* CI/CD pipeline
* Data lineage tracking
* Incremental processing
* Expanded monitoring and observability over quality and metadata artifacts
