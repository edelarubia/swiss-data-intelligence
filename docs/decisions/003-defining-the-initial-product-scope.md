# ADR-003 - Defining the Initial Product Scope

## Status

Accepted

## Category

Product

## Date

2026-06-30

## Context

Swiss Data Intelligence is intended to become a modular AI platform for exploring Swiss public datasets through natural language, analytics, machine learning and visualization.

During the initial design phase, several possible directions were considered.

One option was to build a platform supporting multiple domains from the beginning, including housing, labour market, demographics, health insurance and cost of living.

Another option was to focus on a single domain for the first MVP while designing the architecture to support future expansion.

The project is constrained by an estimated development effort of approximately 100–150 hours, making careful scope management essential.

## Decision

The project will be developed as a modular platform, but the initial MVP will focus on a single domain.

The first implementation will concentrate on Swiss public datasets related to **Housing and Demographics**, while keeping the architecture sufficiently modular to support additional domains in future iterations.

Insurance, labour market and other intelligence modules are considered part of the long-term vision but are explicitly outside the scope of the first MVP.

## Rationale

A focused MVP significantly increases the probability of delivering a complete, high-quality product within the available time.

Housing and demographic datasets offer several advantages:

- good availability of official public data;
- strong opportunities for data visualization;
- meaningful analytical use cases;
- potential for machine learning applications;
- relevance for both academic evaluation and professional portfolio development.

Designing the platform with modularity in mind preserves future extensibility without introducing unnecessary implementation complexity during the first iteration.

## Alternatives Considered

### Multi-domain MVP

Advantages

- Broader platform vision.
- Demonstrates multiple use cases.
- More ambitious project scope.

Drawbacks

- Higher implementation complexity.
- Greater integration effort.
- Increased risk of not completing the MVP.
- Reduced implementation quality across domains.

---

### Insurance-first MVP

Advantages

- Strong relevance for the Swiss insurance industry.
- High employability value.
- Interesting opportunities for future AI applications.

Drawbacks

- Public datasets are relatively limited.
- Data sources are fragmented.
- Higher data preparation effort.
- Increased project risk within the available timeframe.

---

### Single-domain MVP with Modular Architecture (Selected)

Advantages

- Clear and achievable scope.
- Better implementation quality.
- Easier testing and validation.
- Reduced project risk.
- Natural path for future expansion.

Drawbacks

- Initial functionality is limited to one domain.
- Some planned modules are postponed.

## Consequences

### Positive

- Higher probability of delivering a complete MVP.
- Better balance between engineering quality and project scope.
- Stronger foundation for future platform growth.
- Easier academic defence due to a well-defined scope.

### Negative

- Some envisioned functionality will not be available in the first release.
- Future modules will require additional integration work.

## Review

This decision should be reviewed after the first MVP has been completed.

If additional development time becomes available, new intelligence modules may be incorporated without requiring significant architectural changes, provided they remain aligned with the platform's modular design.