ADR-001 - Three-layer architecture (Raw/Silver/Gold)

Decision:
Adopt a three-layer architecture instead of Raw/Bronze/Silver/Gold.

Rationale:
The source data is already delivered in Parquet format with a stable schema. Introducing a Bronze layer would not add a distinct responsibility in this scenario.

Consequences:
Simpler architecture with lower operational complexity while preserving data quality and governance requirements.