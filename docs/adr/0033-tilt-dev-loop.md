# 0033 – Tilt Dev Loop

*Status*: **Accepted**

## Context

Waiting 20 s for `kubectl apply` kills feedback loops. We want < 2 s local sync.

## Decision

Introduce **Tilt** with `Tiltfile`:

```python
k8s_yaml('manifests/')
docker_build('app', '.', live_update=[sync('.', '/app'), run('bootstrap.sh')])
```

Auto-reload when Python files change.

## Alternatives Considered

\| Option | Pros | Cons |
\| Skaffold | Google-backed | Slower live sync (\~5 s) |
\| Telepresence | Full remote | Network complexity |

## Consequences

* Devs run `tilt up`; browser dashboard shows live logs.
* Requires Docker Desktop or Colima.
