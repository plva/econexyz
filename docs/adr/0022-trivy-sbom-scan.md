# 0022 – Trivy SBOM & Image Scan

*Status*: **Accepted**

## Context

Container images must be scanned for OS-level CVEs and accompanied by a
Software Bill of Materials (SBOM) for supply-chain audits.

## Decision

Add **Trivy** GH Action step:

```
trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE
trivy image --format cyclonedx --output sbom.xml $IMAGE
```

Results are uploaded as artifacts; CI fails on unpatched High/Critical CVEs.

## Alternatives Considered

\| Option | Pros | Cons |
\| Anchore Grype | Good SBOM | Heavier image, slower |
\| Dockle + Clair | Granular checks | Multiple tools to maintain |

## Consequences

* Provides CycloneDX SBOM for downstream consumers.
* Adds ≈ 30 s to container workflow.
