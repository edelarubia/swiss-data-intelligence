# ADR-001 - Starting the Project

## Status

Accepted

## Category

Project Setup

## Context

Several repository structures were considered before starting the implementation.

One option was to create a fully featured repository including Docker, Kedro, MLflow, CI/CD pipelines and a complete folder hierarchy.

Another option was to begin with a lightweight repository containing only the components required for the MVP.

## Decision

The project will adopt an incremental repository strategy.

Only folders, tools and configuration files that provide immediate value will be introduced.

Additional components will be incorporated when they become necessary during development.

## Rationale

This approach keeps the project focused on delivering a working MVP within the available time.

It also avoids premature optimisation and reduces unnecessary maintenance.

## Alternatives Considered

### Full architecture from day one

Pros

- Production-like structure
- Ready for future expansion

Cons

- Higher complexity
- Longer setup time
- Increased maintenance

---

### Incremental architecture

Pros

- Faster start
- Lower cognitive load
- Better focus on the MVP

Cons

- Some refactoring may be required later

## Consequences

Positive

- Faster project progress.
- Simpler repository.
- Easier onboarding.

Negative

- Repository structure will evolve during development.

## Review

This decision will be revisited after the MVP has been completed.