# Boot / env
# Install the development environment
install-dev:
    @echo "install-dev \u2192 TODO (will call bootstrap.sh)"

# Test suite
# Run the test suite
test:
    nox -s tests

# Lint / format
# Check code style
lint:
    nox -s lint

# Type-check
# Static type analysis
types:
    nox -s types

# Security
# Run security scans
audit:
    @echo "audit \u2192 TODO (will call nox -s security)"

# Docs
# Build documentation
docs:
    @echo "docs \u2192 TODO (will call nox -s docs)"

# Dev stack
# Start local dev environment
dev:
    @echo "dev \u2192 TODO (will call tilt up)"

# Stop local dev environment
dev-stop:
    @echo "dev-stop \u2192 TODO (will call tilt down)"

# Docker build
# Build and sign Docker image
image tag="latest":
    @echo "image tag={{tag}} \u2192 TODO (will build & sign Docker image)"

# Run CLI
# Execute command-line interface
run *ARGS:
    @echo "run {{ARGS}} \u2192 TODO (will call python -m yourpackage.cli)"

# Commit helper
commit:
    cz commit            # interactive wizard

# Version bump
bump:
    cz bump --yes        # version & changelog

# Agent scaffolding
# Scaffold a new agent
new-agent name slug:
    @echo "new-agent name={{name}} slug={{slug}} \u2192 TODO (will scaffold agent template)"

# Export SDL
# Generate GraphQL schema
export-sdl:
    @echo "export-sdl \u2192 TODO (will export SDL)"

# Dev environment health check
# Check if all dev dependencies are available
health-check:
    @echo "Checking dev environment..."
    @python scripts/dev_health_check.py
