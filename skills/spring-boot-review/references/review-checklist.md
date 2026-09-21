# Spring Boot review checklist

Read only the sections relevant to the requested review.

## Architecture and boundaries

- Package and module boundaries reflect business responsibilities rather than accidental framework groupings.
- Controllers handle transport concerns without owning business transactions.
- Dependency direction does not create cycles or couple domain logic to infrastructure unnecessarily.
- Transaction boundaries are explicit and cover the full unit of work.

## HTTP and API contracts

- Request validation covers nested objects and domain constraints.
- Status codes, error bodies, pagination, and idempotency behavior are consistent.
- Domain entities are not unintentionally exposed as public request or response contracts.
- Exception handling does not leak stack traces, SQL details, or secrets.

## Security

- Authentication and authorization rules cover every sensitive route and method.
- Method security, path matchers, CORS, CSRF, session policy, and password handling match the application type.
- Inputs used in SQL, file paths, templates, redirects, logs, or outbound requests are constrained appropriately.
- Secrets are not committed, logged, returned, or embedded in images and build artifacts.
- Dependency or configuration findings are tied to the versions and deployment mode actually in use.

## Persistence and data integrity

- Queries avoid unbounded reads, N+1 access, and missing pagination where data can grow.
- Entity equality, lazy loading, cascading, and serialization do not create correctness or performance hazards.
- Migrations are safe for existing data and compatible with rolling deployment when required.
- Concurrency-sensitive updates use appropriate constraints, locking, or optimistic versioning.

## Reliability and operations

- Timeouts, retries, circuit breaking, and connection pools are configured for external dependencies.
- Retry behavior is idempotent and does not multiply side effects.
- Logs are actionable without exposing personal data, tokens, or credentials.
- Health checks distinguish liveness from readiness and do not overload dependencies.
- Shutdown, scheduled jobs, async execution, and thread pools have explicit lifecycle and capacity behavior.

## Tests and maintainability

- Tests cover authorization boundaries, validation, error contracts, transactions, and failure paths.
- Integration tests exercise important framework configuration that unit tests cannot validate.
- Configuration profiles do not silently weaken production behavior.
- Custom abstractions remove real duplication without obscuring standard Spring behavior.
