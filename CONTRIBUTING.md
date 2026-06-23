# Contributing to KamiKonn

Thank you for your interest in contributing to KamiKonn! This document outlines the process for contributing code, reporting bugs, and suggesting features.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Branching Strategy](#branching-strategy)
- [Commit Message Convention](#commit-message-convention)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)

---

## Code of Conduct

This project adheres to our [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold these standards. Please report unacceptable behavior to the maintainers.

---

## How Can I Contribute?

### Reporting Bugs

Before filing a bug report:
- Search existing [issues](../../issues) to avoid duplicates.
- Confirm the bug is reproducible on the `main` branch.

Use the **Bug Report** issue template when creating a new issue. Include:
- A clear title and description.
- Steps to reproduce.
- Expected vs. actual behavior.
- Environment details (OS, browser, Docker version).

### Suggesting Features

Open a **Feature Request** issue using the provided template. Describe:
- The problem your feature solves.
- The proposed solution.
- Alternatives you considered.

### Submitting Code Changes

For anything beyond trivial fixes, open an issue first to discuss the approach before investing significant effort.

---

## Development Setup

1. **Fork** the repository and clone your fork:
   ```bash
   git clone https://github.com/<your-username>/kamconnect.git
   cd kamconnect
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```

3. **Install dependencies and start services**:
   ```bash
   make setup
   make build
   ```

4. **Install pre-commit hooks** (mandatory):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

5. **Verify your setup**:
   ```bash
   make test-backend
   make test-frontend
   ```

---

## Branching Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready code; protected -- no direct pushes |
| `develop` | Integration branch for ongoing work |
| `feature/<ticket-id>-short-description` | New features |
| `fix/<ticket-id>-short-description` | Bug fixes |
| `chore/<description>` | Dependency updates, tooling, config |
| `docs/<description>` | Documentation-only changes |

All work must branch from and target `develop` unless it is a hotfix targeting `main`.

---

## Commit Message Convention

This project follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification.

**Format:**
```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

**Types:**
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes only
- `style`: Formatting changes (no logic change)
- `refactor`: Code change that is neither a fix nor a feature
- `test`: Adding or updating tests
- `chore`: Build process, dependency, or tooling changes
- `perf`: Performance improvements

**Examples:**
```
feat(events): add CSV bulk import endpoint
fix(auth): resolve JWT refresh token expiry edge case
docs(readme): update quick start instructions
chore(deps): bump Django from 5.2.0 to 5.2.1
```

---

## Pull Request Process

1. Ensure your branch is up to date with the target branch.
2. All CI checks must pass (linting, tests, security scan).
3. Fill out the pull request template completely.
4. Request a review from at least one maintainer.
5. Address all review comments before merging.
6. Squash-merge is the default strategy to keep a clean history.

**PR Title** must follow the same Conventional Commits format as commit messages.

---

## Coding Standards

### Backend (Django / Python)

- **Formatter**: `ruff format` (enforced by pre-commit)
- **Linter**: `ruff check` (enforced by pre-commit)
- **Type hints**: Required for all new public functions and methods.
- **Serializers**: All API input must be validated through DRF serializers.
- **Sanitization**: Use `nh3` for any field accepting HTML content.
- **No direct `manage.py` imports**: Use `uv run python manage.py ...` inside Docker.

### Frontend (React / TypeScript)

- **Strict TypeScript**: `strict` mode must be maintained. Avoid `any`.
- **Styling**: Tailwind CSS 4.x + shadcn/ui only. No Material UI or Bootstrap.
- **State**: TanStack Query v5 for server state, Zustand 5.x for client state. No Redux.
- **Validation**: React Hook Form + Zod for all forms.
- **Linter**: ESLint (enforced by CI).

---

## Testing Requirements

All new code must be accompanied by tests:

| Layer | Framework | Minimum Requirement |
|-------|-----------|---------------------|
| Backend unit/integration | pytest + factory-boy | New endpoints: 80% coverage |
| Frontend components | Vitest + React Testing Library | Core components tested |
| E2E (Phase 3+) | Playwright | Critical user flows |

Run tests locally before opening a PR:
```bash
make test-backend
make test-frontend
```

---

## Questions?

If you have questions that are not addressed here, open a [Discussion](../../discussions) on GitHub.
