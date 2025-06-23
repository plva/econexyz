# 0029 – Autodoc + Napoleon

*Status*: **Accepted**

## Context

API reference should generate from docstrings—once—without duplicate typing.

## Decision

Enable Sphinx extensions:

```
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]
napoleon_google_docstring = True
```

Napoleon parses Google/NumPy style strings; autosummary stubs are generated
during `make html`.

## Alternatives Considered

* pdoc | Simple CLI | Limited cross-linking
* MkDocs-gen-docs | Works | Same Node concern as above

## Consequences

* Accurate, versioned API docs; docstring drift spotted in PR diff.
