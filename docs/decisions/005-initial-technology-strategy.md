# ADR-005 - Initial Technology Strategy

## Status

Accepted

## Category

Engineering

## Date

2026-06-30

## Context

Swiss Data Intelligence aims to demonstrate sound engineering practices while remaining achievable within the project's estimated duration of approximately 100–150 hours.

Several modern data engineering and MLOps frameworks were considered during the initial design phase, including tools such as Docker, Kedro, MLflow, LangChain and vector databases.

Although these technologies provide significant value in larger production environments, introducing them too early would increase the project's complexity without necessarily improving the first MVP.

The challenge is therefore to select a technology stack that maximises value while minimising unnecessary complexity.

## Decision

The project will adopt a lightweight, incremental technology strategy.

The initial implementation will use a minimal set of technologies that directly support the MVP.

The initial stack consists of:

- Python
- Pandas
- NumPy
- Scikit-learn
- Streamlit
- Plotly
- Git
- GitHub

Additional technologies will only be introduced when they solve a concrete problem that cannot reasonably be addressed using the existing stack.

## Rationale

The objective is to maximise the amount of working functionality delivered within the available project time.

A lightweight technology stack reduces:

- implementation effort;
- learning overhead;
- maintenance complexity;
- integration risk.

This approach also aligns with the project's engineering principles, particularly:

- MVP First;
- Simplicity over Complexity;
- Every Dependency Must Justify Its Existence.

## Alternatives Considered

### Full Modern AI Stack

Examples include:

- Docker
- Kedro
- MLflow
- LangChain
- ChromaDB
- Airflow

Advantages

- Production-oriented architecture.
- Demonstrates familiarity with modern tooling.
- Easier future scaling.

Drawbacks

- Significant increase in complexity.
- Larger learning curve.
- More configuration than product development.
- Higher maintenance effort.

---

### Minimal Python-Based Stack (Selected)

Advantages

- Faster implementation.
- Easier debugging.
- Lower cognitive load.
- Better focus on solving the actual problem.
- Technologies already well understood.

Drawbacks

- Some engineering capabilities may be introduced later.
- Future refactoring may be required if the platform evolves significantly.

## Consequences

### Positive

- Faster development.
- Lower technical complexity.
- Better focus on delivering the MVP.
- Easier maintenance.
- More time available for data exploration and machine learning.

### Negative

- Some production-oriented tooling is intentionally postponed.
- Future iterations may require additional engineering work.

## Review

This decision should be reviewed after the MVP has been completed.

Additional technologies should only be introduced when they provide measurable value or solve clearly identified limitations in the existing architecture.