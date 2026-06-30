# ADR-004 - Data Discovery Strategy

## Status

Accepted

## Category

Data

## Date

2026-06-30

## Context

Swiss Data Intelligence is fundamentally a data-driven platform. The quality, coverage and usability of the available public datasets will directly determine the platform's capabilities.

During the planning phase, two possible approaches were considered.

The first approach was to immediately begin implementing data pipelines and application components, discovering potential issues as development progressed.

The alternative approach was to first perform a structured data discovery phase, identifying and assessing candidate datasets before writing any production code.

Given the limited project duration and the importance of selecting reliable public data sources, an early investment in data understanding was considered essential.

## Decision

Before implementing data pipelines or machine learning components, the project will include a dedicated Data Discovery phase.

During this phase, candidate datasets will be:

- identified;
- documented;
- assessed;
- prioritised.

The project will maintain a lightweight **Data Inventory & Assessment Catalog** to document each dataset using a consistent structure.

The catalog will support dataset selection while remaining simple enough to maintain throughout the project.

## Rationale

Understanding the available data before implementation reduces project risk and improves technical decision-making.

This approach helps identify:

- suitable data sources;
- potential data quality issues;
- licensing constraints;
- update frequency;
- geographical coverage;
- opportunities for analytics and machine learning.

It also ensures that architectural decisions are driven by available data rather than assumptions.

## Alternatives Considered

### Implementation First

Advantages

- Immediate development.
- Faster initial progress.
- Earlier prototype.

Drawbacks

- Higher risk of selecting unsuitable datasets.
- Potential rework.
- Greater uncertainty during implementation.

---

### Comprehensive Enterprise Data Catalog

Advantages

- Complete dataset documentation.
- Maximum traceability.
- Highly structured metadata.

Drawbacks

- Significant documentation effort.
- Unnecessary complexity for the project scope.
- Low return on investment.

---

### Lightweight Data Discovery Strategy (Selected)

Advantages

- Better understanding of available data.
- Reduced implementation risk.
- Supports informed architectural decisions.
- Minimal maintenance effort.
- Useful input for the final report.

Drawbacks

- Small delay before implementation begins.
- Requires discipline to keep the catalog updated.

## Consequences

### Positive

- Better dataset selection.
- Reduced implementation risk.
- Improved understanding of data limitations.
- More robust architecture.
- Better justification of project decisions.

### Negative

- Small upfront investment before coding begins.
- Initial project progress may appear slower.

## Review

This decision should be reviewed after the Data Discovery phase has been completed.

At that point, the selected datasets should provide sufficient confidence to begin implementing the MVP with minimal changes to the overall data strategy.