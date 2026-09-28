# ADR-006 - Dataset Storage and Naming Convention

## Status

Accepted

## Category

Data Engineering

## Date

2026-07-08

## Context

Swiss Data Intelligence relies on multiple public datasets obtained from different Swiss public institutions, including the Swiss Federal Statistical Office (BFS), the Federal Office of Public Health (BAG), SECO and other official data providers.

These datasets are distributed in different formats, may be updated periodically and are often accompanied by supplementary files such as appendices, lookup tables and methodological documentation.

Without a consistent storage and naming strategy, the repository would become difficult to navigate, datasets could be accidentally modified and future updates would be harder to manage.

A standard convention is therefore required to ensure consistency, reproducibility and maintainability throughout the project.

## Decision

The project will adopt a consistent storage and naming convention for all datasets.

### Directory Structure

Datasets will be organised according to their provider and business domain.

Example:

```text
data/
│
├── raw/
│   └── bfs/
│       ├── housing/
│       ├── demographics/
│       └── reference/
│
└── processed/
```

The `raw` directory will always contain the original datasets exactly as downloaded from the official source.

These files must never be modified manually.

Processed datasets will be generated separately inside the `processed` directory.

### File Naming Convention

Dataset filenames will follow the convention:

- UPPERCASE
- Words separated by underscores (`_`)
- Descriptive business-oriented names
- Temporal coverage included whenever it provides meaningful context

Examples:

```text
HOME_OWNERSHIP_RATE_BY_CANTON_2019_2024.xlsx

RESIDENT_POPULATION_BY_CANTON_2023.xlsx

AVERAGE_HOUSEHOLD_SIZE_BY_CANTON_2010_2023.csv
```

### Dataset Identifier

Each dataset will have a stable Dataset ID stored in the Data Inventory & Assessment Catalog.

Dataset IDs:

- remain stable over time;
- do not include temporal coverage;
- uniquely identify the logical dataset rather than a specific downloaded file.

Example:

Dataset ID

```text
HOME_OWNERSHIP_RATE_BY_CANTON
```

Filename

```text
HOME_OWNERSHIP_RATE_BY_CANTON_2019_2024.xlsx
```

This separation allows datasets to be updated without changing internal references throughout the project.

## Rationale

This convention improves repository organisation while preserving reproducibility.

Separating Dataset IDs from physical filenames allows new dataset versions to be incorporated without affecting project documentation or application logic.

Including temporal coverage within filenames provides immediate information about the scope of the downloaded data and simplifies version management.

Keeping the `raw` directory immutable ensures that all processing steps remain reproducible and traceable.

## Alternatives Considered

### Preserve Original Provider Filenames

Advantages

- Exact correspondence with downloaded files.
- No renaming effort.

Drawbacks

- Provider filenames are often cryptic.
- Difficult to understand without consulting documentation.
- Poor readability inside the repository.

---

### Omit Temporal Coverage from Filenames

Advantages

- Shorter filenames.
- Slightly simpler naming convention.

Drawbacks

- Difficult to identify dataset coverage.
- Harder to distinguish different dataset versions.
- Reduced traceability.

---

### Standardised Naming Convention (Selected)

Advantages

- Consistent repository organisation.
- Easy to understand.
- Supports reproducibility.
- Facilitates future updates.
- Improves readability.
- Clearly distinguishes logical datasets from physical files.

Drawbacks

- Requires renaming datasets after download.
- Naming convention must be applied consistently.

## Consequences

### Positive

- Consistent dataset organisation.
- Improved repository readability.
- Easier dataset version management.
- Better reproducibility.
- Simpler maintenance.
- Stable references within the project.

### Negative

- Small effort required when importing new datasets.
- Original filenames are not preserved as downloaded.

## Review

This decision should be reviewed if the project incorporates automated data ingestion pipelines or external data versioning tools.

Until then, this convention is expected to remain stable throughout the project.