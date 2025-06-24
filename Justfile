# Boot / env
# Install the development environment
install-dev:
    @echo "install-dev \u2192 TODO (will call bootstrap.sh)"

# Test suite
# Run the test suite
test:
    uv run nox -s tests

# Coverage
# Run tests with coverage and show results
coverage:
    @echo "🧪 Running tests with coverage..."
    @uv run pytest tests/ -v --cov=src/econexyz --cov-report=term-missing --cov-report=html
    @echo ""
    @echo "📊 Coverage report generated in htmlcov/index.html"
    @echo "🔗 Open coverage report: file://$(pwd)/htmlcov/index.html"

# Coverage upload
# Run tests with coverage and upload to codecov
coverage-upload:
    @echo "🧪 Running tests with coverage and uploading to codecov..."
    @uv run pytest tests/ -v --cov=src/econexyz --cov-report=xml
    @uv run codecov
    @echo "✅ Coverage uploaded to codecov.io"

# Lint / format
# Check code style
lint:
    uv run nox -s lint

# Type-check
# Static type analysis
types:
    uv run nox -s types

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

# Commit alias
c:
    just commit

# Check commit style
# Validate commit message format
commit-style:
    @echo "🔍 Checking commit style..."
    @cz check --rev-range HEAD~1..HEAD || (echo "❌ Commit style check failed" && exit 1)
    @echo "✅ Commit style check passed"

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
    @.venv/bin/python scripts/dev_health_check.py

# Build all
# Run complete build pipeline: bootstrap, health check, tests, lint, types
ball:
    @echo "🚀 Starting complete build pipeline..."
    @echo ""
    @echo "0️⃣  Bootstrapping environment..."
    @./bootstrap.sh --yes-hooks || (echo "❌ Bootstrap failed" && exit 1)
    @echo "✅ Bootstrap complete"
    @echo ""
    @echo "1️⃣  Checking dev environment..."
    @just health-check || (echo "❌ Health check failed" && exit 1)
    @echo "✅ Health check passed"
    @echo ""
    @echo "2️⃣  Running tests..."
    @just test || (echo "❌ Tests failed" && exit 1)
    @echo "✅ Tests passed"
    @echo ""
    @echo "3️⃣  Running linting..."
    @just lint || (echo "❌ Linting failed" && exit 1)
    @echo "✅ Linting passed"
    @echo ""
    @echo "4️⃣  Running type checking..."
    @just types || (echo "❌ Type checking failed" && exit 1)
    @echo "✅ Type checking passed"
    @echo ""
    @echo "🎉 All checks passed! Build successful!"

# Run all checks: health, tests, lint, types, security, secrets (no bootstrap)
check:
    @echo "🔍 Running all checks..."
    @just health-check || (echo "❌ Health check failed" && exit 1)
    @just test || (echo "❌ Tests failed" && exit 1)
    @just lint || (echo "❌ Linting failed" && exit 1)
    @just types || (echo "❌ Type checking failed" && exit 1)
    @just security || (echo "❌ Security audit failed" && exit 1)
    @just secrets || (echo "❌ Secret scanning failed" && exit 1)
    @echo "✅ All checks passed!"

# Security audit
# Run security vulnerability scan
security:
    uv run nox -s security

# Secret scanning
# Run gitleaks secret detection
secrets:
    uv run nox -s secrets
