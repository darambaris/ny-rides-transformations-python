# Architecture Decisions and Assumptions

## Overview

This project implements a batch data pipeline to ingest, validate, transform, and analyze the NYC TLC Yellow Taxi dataset.

The architecture follows a layered data platform approach:

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

The design prioritizes simplicity, reproducibility, data quality visibility, and ease of execution.

---

# Architecture Decisions

## 1. Layered Data Architecture

The pipeline was organized into Raw, Silver, and Gold layers.

### Raw

Purpose:

* Preserve downloaded source files
* Avoid modifying source data
* Enable reproducibility

Characteristics:

* Original parquet files
* Partitioned by year and month
* No transformations applied

---

### Silver

Purpose:

* Standardize data
* Apply contract validation
* Execute quality checks
* Create a trusted dataset

Characteristics:

* Required columns selected
* Type standardization
* Derived columns added:

  * pickup_year
  * pickup_month
  * trip_duration_minutes
* Partitioned by pickup_year and pickup_month

---

### Gold

Purpose:

* Provide business-ready datasets
* Support analytical consumption

Generated datasets:

#### monthly_average_total_amount

Average total trip amount by month.

#### hourly_average_passenger_count

Average passenger count by hour of day.

---

## 2. Contract Validation

A Contract Validator was implemented between Raw and Silver.

The validator verifies:

* Required columns existence
* Expected column data types

Required columns:

* VendorID
* passenger_count
* total_amount
* tpep_pickup_datetime
* tpep_dropoff_datetime

The contract acts as a schema gate before data is published to Silver.

---

## 3. Data Quality Validation

A dedicated Quality Validator was implemented separately from the contract validation.

Quality rules include:

* Negative total_amount detection
* Pickup timestamp before dropoff timestamp
* Null detection in required columns
* Duplicate record detection

Results are stored as JSON quality reports.

This separation was intentional:

* Contract Validation → Schema correctness
* Quality Validation → Data correctness

---

## 4. Metadata and Observability

The pipeline generates metadata artifacts.

### Ingestion Manifest

Generated after Raw ingestion.

Contains:

* Downloaded files
* Execution timestamp
* Download status

### Quality Report

Generated after Silver processing.

Contains:

* Validation results
* Failure counts
* Failure percentages
* Dataset statistics

These artifacts enable future monitoring and lineage use cases.

---

## 5. Storage Abstraction

A Storage abstraction was introduced.

Current implementation:

* LocalStorage

Future implementations may include:

* Amazon S3
* Google Cloud Storage
* Azure Data Lake Storage

The pipeline logic is independent of the underlying storage technology.

---

## 6. Spark Usage

Apache Spark was chosen because:

* The challenge explicitly requested Spark/Databricks compatibility
* The dataset contains millions of records
* The architecture should scale beyond local execution

Spark configuration was centralized in a shared module.

---

## 7. Quality Issues Found

During execution, the following anomalies were identified:

* Negative total_amount values
* Pickup timestamps greater than dropoff timestamps
* Duplicate records
* Records outside the expected analysis period

These records were preserved in Silver and surfaced through quality reports rather than being silently removed.

---

# Assumptions

## Dataset Trustworthiness

The source dataset is treated as authoritative and immutable.

Raw data is never modified.

---

## Data Retention

Raw files are retained after processing.

This enables:

* Reprocessing
* Auditability
* Reproducibility

---

## Analytical Scope

Business questions are answered from Gold datasets.

Challenge-specific filters (such as restricting analysis to May 2025) are applied in the Analysis layer rather than embedded in reusable Gold datasets.

---

## Testing Strategy

The project prioritizes unit testing for:

* Download logic
* Storage
* Validators
* Transformers
* Jobs

Current test coverage is approximately 84%.

Integration and end-to-end tests were identified as future improvements.

---

# Future Improvements

Potential future enhancements include:

* End-to-end integration tests
* Cloud object storage support
* CI/CD pipeline execution
* Data lineage tracking
* Incremental processing
* Expanded monitoring and observability over quality and metadata artifacts
