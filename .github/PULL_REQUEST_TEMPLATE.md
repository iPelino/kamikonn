## Description

<!-- Provide a concise description of what this PR does and why. Link the related issue. -->

Closes #<!-- issue number -->

## Type of change

- [ ] Bug fix (non-breaking change that fixes an issue)
- [ ] New feature (non-breaking change that adds functionality)
- [ ] Breaking change (fix or feature that causes existing functionality to break)
- [ ] Refactor (no functional changes)
- [ ] Documentation update
- [ ] Dependency update
- [ ] CI / Infrastructure change

## Changes made

<!-- Bullet-point summary of the key changes. -->

-
-

## How to test

<!-- Step-by-step instructions to verify the change works correctly. -->

1.
2.

## Screenshots / recordings (if UI change)

<!-- Attach before/after screenshots or a short screen recording. -->

## Checklist

- [ ] My branch is up to date with the target branch.
- [ ] I followed the [Conventional Commits](https://www.conventionalcommits.org/) format for my commit messages and this PR title.
- [ ] I ran `make lint` locally and there are no errors.
- [ ] I ran the relevant tests (`make test-backend` / `make test-frontend`) and they pass.
- [ ] I added or updated tests for the code I changed.
- [ ] I updated documentation (docstrings, README, API docs) where necessary.
- [ ] No secrets, credentials, or `.env` files are included in this PR.
- [ ] For backend changes: new endpoints are authenticated and validated through DRF serializers.
- [ ] For frontend changes: TypeScript strict mode is maintained (no `any`).
