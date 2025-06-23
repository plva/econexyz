# Boot / env
# Install the development environment
install-dev:
    @echo "install-dev \u2192 TODO (will call bootstrap.sh)"

# Test suite
# Run the test suite
test:
    @echo "test \u2192 TODO (will call nox -s tests)"

# Lint / format
# Check code style
lint:
    @echo "lint \u2192 TODO (will call ruff check . && ruff format --check .)"

# Type-check
# Static type analysis
types:
    @echo "types \u2192 TODO (will call ty --strict src/)"

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

# Agent scaffolding
# Scaffold a new agent
new-agent name slug:
    @echo "new-agent name={{name}} slug={{slug}} \u2192 TODO (will scaffold agent template)"

# Export SDL
# Generate GraphQL schema
export-sdl:
    @echo "export-sdl \u2192 TODO (will export SDL)"
