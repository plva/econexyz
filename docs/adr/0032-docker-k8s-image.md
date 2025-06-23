# 0032 – Docker + K8s Image

*Status*: **Accepted**

## Context

Prod deploy will run in Kubernetes. Image size and provenance matter.

## Decision

* Base: `gcr.io/distroless/python3-debian12`
* Build multi-stage: wheels → distroless.
* Sign image with **cosign**; generate CycloneDX SBOM via Trivy.
* Tag scheme: `ghcr.io/org/app:${SEMVER}`

## Alternatives Considered

\| Option | Pros | Cons |
\| Alpine Python | Small | Segfault risk with glibc wheels |
\| Full Debian | Familiar | 3× size |
\| Kaniko build | Rootless | Needs extra infra |

## Consequences

* 70 MB image, verifiable signature, SBOM attached.
* Slight complexity in Dockerfile; hidden by `just image`.
