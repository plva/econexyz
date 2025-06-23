# 0028 – Sphinx + MyST + Furo Docs

*Status*: **Accepted**

## Context

We want a documentation site that accepts Markdown, supports API auto-docs, and
can publish to GitHub Pages.

## Decision

* **Sphinx** as engine.
* **MyST** for GitHub-flavoured Markdown.
* **Furo** for accessible dark/light theme.

`docs/Makefile html` or `just docs` builds site; a GitHub Pages workflow deploys
on `main`.

## Alternatives Considered

\| Option | Pros | Cons |
\| MkDocs Material | Beautiful | Autodoc via plugins, less mature |
\| Docusaurus | React, MDX | Node build, heavier |

## Consequences

* Authors write Markdown in the repo they already use.
* Adds \~20 s build step; acceptable.
