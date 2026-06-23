# Security Policy

## Supported Versions

The following versions of KamiKonn are currently receiving security updates:

| Version | Supported          |
| ------- | ------------------ |
| main    | :white_check_mark: |

## Reporting a Vulnerability

We take the security of KamiKonn seriously. If you discover a security vulnerability, please **do not** open a public GitHub issue.

### How to Report

1. **Email**: Send a detailed report to the maintainers via the email listed on the repository profile.
2. **GitHub Private Vulnerability Reporting**: Use GitHub's built-in [private vulnerability reporting](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability) feature available in the **Security** tab of this repository.

### What to Include

Please include the following in your report:

- A clear description of the vulnerability and its potential impact.
- Steps to reproduce the vulnerability (proof of concept if possible).
- The version(s) of KamiKonn affected.
- Any suggested mitigations or fixes.

### Our Commitment

- We will acknowledge receipt of your report within **48 hours**.
- We will provide an initial assessment within **5 business days**.
- We will work with you to understand the issue and coordinate a fix and disclosure timeline.
- We will credit you in the security advisory (unless you prefer to remain anonymous).

### Scope

Security issues in scope include:

- Authentication and authorization flaws (JWT, OAuth, role escalation).
- SQL injection or data exposure via the PostgreSQL backend.
- Cross-site scripting (XSS) or Cross-site request forgery (CSRF).
- Insecure direct object references (IDOR).
- Sensitive data exposure (credentials, PII).
- Remote code execution.
- Denial of service vulnerabilities in critical paths.

### Out of Scope

- Issues in third-party dependencies that have already been publicly disclosed (please report those upstream).
- Issues that require physical access to a user's device.
- Social engineering attacks.

## Security Best Practices for Contributors

- Never commit secrets, credentials, or `.env` files. Use `.env.example` as a template.
- All API endpoints must be authenticated unless explicitly designed to be public.
- User-supplied input must be sanitized using `nh3` (HTML) and DRF serializer validation.
- Keep dependencies up to date; Dependabot is enabled on this repository.
