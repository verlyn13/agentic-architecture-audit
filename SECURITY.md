# Security Policy

## Scope

The Agentic Architecture Audit is a **documentation/methodology package**, not an
application. There is no service to attack and no runtime to exploit. The only executable
code in the repository is [`scripts/check_drift.py`](scripts/check_drift.py), a
standard-library-only hygiene linter run by pre-commit and CI.

In scope for a security report:

- A vulnerability in `scripts/check_drift.py` or in the repository's CI / pre-commit
  configuration (for example, arbitrary code execution, or a check that can be silently
  bypassed).
- Guidance in the authority texts or companions that, if followed, would lead an operator
  or a coding agent to take an unsafe action.

Out of scope:

- The prose methodology itself (open an issue or PR for errors or gaps).
- Findings produced by *running* the audit on your own project — those belong to that
  project, not here.

## Supported versions

Fixes land on the latest released version. Older tags are historical and are not patched
in place; upgrade to the most recent tag rather than expecting a backport.

| Version | Supported |
| --- | --- |
| Latest release | Yes |
| Older tags | No (historical) |

## Reporting a vulnerability

Please report privately rather than opening a public issue:

- Use GitHub's **private vulnerability reporting**: the repository's **Security** tab →
  **Report a vulnerability**.

Include the affected file and lines, what an attacker could do, and a reproduction if you
have one. This is a single-maintainer project, so responses are best-effort; you can
expect an acknowledgement and, for confirmed issues, a fix or documented mitigation in a
subsequent release. Coordinated disclosure is appreciated — please give a reasonable
window before any public write-up.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the general change and release process. The
package is licensed under [Apache-2.0](LICENSE).
