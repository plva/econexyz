# 0024 – License Compliance

*Status*: **Accepted**

## Context

Some licences (e.g., GPL-3.0) conflict with planned distribution models.
Compliance must be automated.

## Decision

Run `pip-licenses --format=json` in Nox; compare IDs against
`licenses_allowlist.txt` (SPDX identifiers). Fail CI if new package is not
approved. Manual review + ADR required to add an exception.

## Alternatives Considered

* FOSSA SaaS – rich UI, paid tier needed.
* Manual spreadsheet – error-prone.

## Consequences

* Early alert on incompatible licences.
* Requires periodic update of allow-list as SPDX adds new IDs.
