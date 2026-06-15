# NY Rides Transformations

Python project for ingesting NYC Yellow Taxi trip files, storing them in a partitioned raw layout, and validating tabular contracts with lightweight unit tests.

## What Exists Today

The current repository implements:

- Monthly file generation for NYC Yellow Taxi parquet files.
- Download job with error handling and execution summary.
- Local raw storage partitioned as `year=YYYY/month=MM`.
- Ingestion manifest generation in `artifacts/ingestion/`.
- Contract validation for required columns and expected column types.
- Unit test suite covering ingestion, jobs, storage, metadata, and quality validation.

## Current Flow

The implemented ingestion flow is:

1. Generate the list of monthly TLC files between a start date and end date.
2. Download each parquet file from the public TLC distribution endpoint.
3. Save each file under the configured raw output directory using partitioned paths.
4. Write a manifest JSON artifact summarizing success and failure results.

Example raw file layout:

```text
data/raw/
	year=2025/
		month=03/
			yellow_tripdata_2025-03.parquet
```

Example manifest layout:

```text
artifacts/ingestion/
	manifest_YYYYMMDD_HHMMSS.json
```

## Project Structure

```text
ny_rides/
	contracts/       Contract definitions
	ingestion/       TLC download logic
	jobs/            Executable jobs and orchestration
	metadata/        Manifest generation
	quality/         Validators for schema and quality checks
	shared/          Shared utilities such as logging
	storage/         Storage abstractions and local storage
tests/unit/        Unit tests by module
```

## Data Contract

The Yellow Taxi contract currently expects these columns:

- `VendorID`
- `passenger_count`
- `total_amount`
- `tpep_pickup_datetime`
- `tpep_dropoff_datetime`

The contract validator checks:

- Presence of all required columns.
- Expected column types defined in `YellowTaxiContract.COLUMN_TYPE_RULES`.

## Quality Assessment

The Silver pipeline executes a set of quality validations before publishing data.

**Validation Rules:**
- Required columns presence
- Data types correctness
- Null checks in required columns
- Duplicate record detection
- Temporal consistency checks (pickup <= dropoff)
- Negative amount detection

**Results for Jan-May 2023:**
- **19.7M rows** analyzed
- **159 duplicated records** detected (0.0008%)
- **562 records** with invalid pickup/dropoff ordering (0.0028%)
- **372k records** with negative total_amount values (1.88%)

Quality reports are generated as JSON artifacts in `artifacts/quality/silver/` with detailed check results and failure percentages.

## Local Commands

Install dependencies:

```bash
make install
```

Run all tests:

```bash
make test
```

Run coverage:

```bash
make coverage
```

Run lint checks:

```bash
make lint
```

Format the codebase:

```bash
make format
```

Clean local caches and build artifacts:

```bash
make clean
```

## Download Files Locally

Default run:

```bash
make download-files
```

Custom raw output directory:

```bash
make download-files OUTPUT_DIR=data/raw/custom
```

The `download-files` target runs:

```bash
poetry run python -m ny_rides.jobs.download_files \
	--start-date 2025-01-01 \
	--end-date 2025-05-31 \
	--output-dir data/raw
```

## Requirements

- Python 3.12+
- Poetry

Optional but useful depending on future expansion:

- Java, if you later reintroduce Spark-based execution paths.

## Notes

- Raw data is ignored by Git through `data/`.
- Manifest artifacts are ignored by Git through `artifacts/`.
- There is an early `build_silver` job scaffold in the repository, but the main working flow today is the raw ingestion path.