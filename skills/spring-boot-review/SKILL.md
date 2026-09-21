---
name: spring-boot-review
description: Review Spring Boot projects for architecture, security, API design, data access, performance, and maintainability. Use when a user asks for a Spring Boot code review, audit, risk assessment, or pre-release check; do not use for ordinary feature implementation.
---

# Spring Boot Review

Review the project and report evidence-backed findings. Diagnose first; do not modify code unless the user also asks for fixes.

## Scope the review

Start with the build files, runtime configuration, application entry point, and package structure. Then inspect the layers and cross-cutting code that are relevant to the request, such as controllers, services, repositories, security configuration, filters, interceptors, exception handlers, migrations, and tests.

Adapt the depth to the repository and the user's goal. Do not require a layer or file merely because it is common in Spring Boot.

For a broad audit, read [references/review-checklist.md](references/review-checklist.md). For a focused request, read only the relevant section.

## Review rules

- Support each finding with a concrete file and tight line range when available.
- Distinguish demonstrated defects from risks that depend on runtime configuration or deployment context.
- Prioritize exploitable security issues, data corruption, availability failures, and broken public contracts.
- Avoid style-only findings unless they materially reduce maintainability or violate an explicit project convention.
- Check existing tests and configuration before claiming behavior is missing.
- Never expose credentials or secret values found during inspection; identify their location and type instead.

## Output

Lead with the overall risk and the highest-impact findings. Group findings by severity:

- Critical: immediate compromise, destructive data loss, or production-wide failure.
- High: likely security, correctness, or availability failure with substantial impact.
- Medium: real defect or maintainability risk with bounded impact.
- Low: worthwhile improvement with limited current impact.

For each finding include the severity, location, observed problem, impact, and a practical recommendation. If no actionable findings are supported by the inspected code, say so and note any important coverage gaps or unverified assumptions.
