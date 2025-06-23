# 0030 – sphinx-click CLI Docs

*Status*: **Accepted**

## Context

Our Typer CLI should appear in docs without hand-written tables.

## Decision

Add **`sphinx-click`**. In `docs/cli.md`:

````
```{autocli} app.cli:app
:prog: mycli
````

```

Build renders commands, options, env-vars.

## Alternatives Considered  
* Manually copy `--help` output – stale quickly.  
* Typer’s built-in doc generator – creates extra files, harder integration.

## Consequences  
* CLI docs update automatically when code changes.  
* Requires `sphinx-click` extension import; negligible cost.
