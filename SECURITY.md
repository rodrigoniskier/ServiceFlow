# Security Policy

ServiceFlow contains synthetic demo data only.

- Require authenticated access in production.
- Keep SECRET_KEY, database credentials and backups outside Git.
- Use DEBUG=0, HTTPS, secure cookies and least-privilege database accounts.
- Historical spreadsheets may contain personal data; keep originals private and use dry-run before import.
- Never publish production exports, backups or requester identifiers.
- Prefer PostgreSQL when scaling beyond a small single-instance deployment.

Report vulnerabilities privately through GitHub Security Advisories / Private Vulnerability Reporting.
