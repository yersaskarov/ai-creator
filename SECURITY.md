# Security Policy

## Supported Versions

Only the latest release receives security fixes.

| Version | Supported |
|---------|-----------|
| 0.7.x   | ✅        |
| < 0.7   | ❌        |

---

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report privately by email: **yersultanaskarov@gmail.com**

Include in your report:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (optional)

We will acknowledge receipt within **48 hours** and aim to release a fix within
**14 days** for critical issues.

---

## Disclosure Policy

- We follow [responsible disclosure](https://en.wikipedia.org/wiki/Responsible_disclosure).
- Please give us reasonable time to fix before public disclosure.
- Do not access other users' data or disrupt the service during testing.

---

## Security Design

AI Creator implements several layers of protection. See
[README.md — Security And Safety](README.md#security-and-safety) for details:

- Path traversal protection (two independent layers via `path_safety.py`)
- ZIP root validation
- AI output file count and size limits
- Provider timeout settings
- Invalid AI JSON fallback to safe templates
- Optional access control via `ALLOWED_TELEGRAM_IDS`
- Per-user generation lock and cooldown
- Full pipeline timeout
- Secrets exclusively via `.env` — never committed
- Gitleaks scanning on every push and PR
