# Swiss Data Intelligence — Project Principles

> *These principles define how technical and product decisions are made throughout the project. They are intended to guide development, reduce unnecessary complexity, and keep the project focused on delivering a valuable and achievable MVP.*

---

# Purpose

Swiss Data Intelligence is developed as part of the CAS in Machine Learning at HSLU. While the project has academic objectives, it is also intended to become a high-quality engineering portfolio that demonstrates sound technical reasoning, architectural thinking and applied AI skills.

These principles provide a consistent decision-making framework throughout the project.

Whenever a significant decision is made, it should align with these principles.

---

# 1. MVP First

## Principle

Deliver a complete, working Minimum Viable Product before expanding the project's scope.

## Why

A finished MVP provides significantly more value than an ambitious but incomplete platform.

The primary objective is to demonstrate the ability to design, build and deliver an end-to-end AI product within realistic constraints.

## Implications

- Prioritize core functionality.
- Deliver vertical slices rather than isolated components.
- Avoid implementing features that are not required for the MVP.
- Expand the platform only after the MVP has been completed.

---

# 2. Simplicity over Complexity

## Principle

Choose the simplest solution that correctly solves the problem.

## Why

Simple systems are easier to understand, maintain, explain and extend.

Complexity should only be introduced when it provides measurable value.

## Implications

- Prefer straightforward implementations.
- Avoid unnecessary abstractions.
- Resist overengineering.
- Optimize for clarity rather than cleverness.

---

# 3. Data Before Models

## Principle

Understand the data before building machine learning models.

## Why

The quality of the data has a greater impact on the final product than the complexity of the model.

A sophisticated model cannot compensate for poor or misunderstood data.

## Implications

- Invest time in data discovery.
- Validate datasets before implementation.
- Document assumptions about the data.
- Build models only when the data supports them.

---

# 4. Evidence over Assumptions

## Principle

Base decisions on evidence rather than intuition whenever possible.

## Why

Engineering decisions should be supported by facts, experiments, public documentation or measurable results.

## Implications

- Validate assumptions.
- Compare alternatives objectively.
- Prefer reproducible results.
- Revisit decisions if new evidence becomes available.

---

# 5. Document Decisions, Not Conversations

## Principle

Document important decisions and their rationale—not the discussions that led to them.

## Why

Future readers should understand *why* a decision was made without reading the history of every conversation.

## Implications

- Use Architecture Decision Records (ADRs) for significant decisions.
- Record context, alternatives and rationale.
- Avoid documenting implementation details or meeting notes.
- Keep documentation concise and actionable.

---

# 6. Every Dependency Must Justify Its Existence

## Principle

No external dependency should be added unless it provides clear value.

## Why

Every dependency increases maintenance effort, learning overhead and long-term complexity.

## Implications

- Prefer the Python standard library when appropriate.
- Reuse existing project dependencies.
- Introduce new libraries only when they solve a real problem.
- Avoid adding tools simply because they are popular.

---

# 7. Every Feature Must Justify Its Existence

## Principle

Every new feature should solve a real user or project need.

## Why

Features require implementation, testing, documentation and long-term maintenance.

If a feature does not contribute to the MVP or the long-term vision, it should be postponed.

## Implications

Before implementing a feature, ask:

- Does it improve the MVP?
- Does it solve an actual problem?
- Is it worth maintaining?
- Can it wait until a later version?

If the answer is uncertain, postpone it.

---

# 8. Design for Evolution

## Principle

Design systems that can evolve without trying to predict every future requirement.

## Why

Requirements change. Premature architecture often introduces unnecessary complexity.

The project should be easy to extend, not fully built for hypothetical future needs.

## Implications

- Keep components modular.
- Separate responsibilities clearly.
- Allow future extensions without implementing them today.
- Avoid speculative architecture.

---

# 9. Build Once, Reuse Often

## Principle

Reusable solutions should be preferred over duplicated implementations.

## Why

Reusability improves consistency, reduces maintenance and simplifies future development.

## Implications

- Reuse utility functions.
- Centralize configuration.
- Keep components independent where possible.
- Avoid copy-and-paste implementations.

---

# 10. Finish Before Perfect

## Principle

Prioritize completion over perfection.

## Why

Perfection is rarely achievable within limited time.

A finished product that works and is well documented provides more value than an unfinished system with ambitious goals.

## Implications

- Deliver incremental improvements.
- Accept reasonable trade-offs.
- Avoid endless refinement.
- Iterate after the MVP.

---

# Decision Checklist

Before introducing a new feature, dependency, architectural component or significant change, consider the following questions:

- Does this help deliver the MVP?
- Is there a simpler solution?
- Does this introduce unnecessary complexity?
- Can an existing solution be reused?
- Is there evidence supporting this decision?
- Will I be able to justify this choice during the CAS defence or a technical interview?
- If this had to be maintained for the next two years, would I still make the same decision?

If several answers are **No**, the decision should be reconsidered.

---

# Continuous Improvement

These principles are intended to guide the project, not constrain it.

They may evolve as the project progresses, provided that any changes are supported by practical experience rather than speculation.

The goal is continuous improvement while preserving consistency in engineering decisions throughout the project.