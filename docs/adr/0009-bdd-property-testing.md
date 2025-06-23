# 0009 – BDD + Property Testing

*Status*: **Accepted**

## Context

Readable behaviour specs help non-coders (and agents) understand intent; property tests expose edge cases.

## Decision

Combine **pytest-bdd** for `.feature` files with **Hypothesis** for property strategies. Example directory layout:

```
tests/
  features/
    login.feature
  test_properties.py
```

## Alternatives Considered

* **Plain pytest only** – simpler, but loses Given/When/Then clarity.
* **Behave** – pure BDD but no Hypothesis integration.
* **Gherkin + external runner** – more moving parts.

## Consequences

* Shared language between PM-style feature files and code.
* Slight learning curve; justified by increased coverage.
