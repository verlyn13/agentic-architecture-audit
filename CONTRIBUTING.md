# Contributing

Thanks for your interest in the Agentic Architecture Audit. This is a **documentation
package, not an application** — the prose is the product. There is no build, no `src/`,
and no runtime. Contributions are edits to text and to the small hygiene tooling that
keeps the text consistent.

The canonical, cross-agent working rules live in [`AGENTS.md`](AGENTS.md) (which
`CLAUDE.md` imports). This file is the human-facing summary; **if it ever conflicts with
`AGENTS.md`, `AGENTS.md` wins.** Read `AGENTS.md` first.

## What has authority

Two files are **authority texts** and are revised only as a deliberate, version-bumped
event — never as a cleanup:

- [`audit-spec.md`](audit-spec.md) — Agentic Architecture Audit Specification.
- [`profile-directive.md`](profile-directive.md) — Project Profile Discovery Directive.

These two are canonical; **everything else is non-authority** — the `companions/`, plus
`MANIFEST.md`, `README.md`, and the scripts. If a non-authority file conflicts with an
authority text, fix the non-authority file — never the authority text.
[`MANIFEST.md`](MANIFEST.md) records the authority/derived mapping and the drift procedure.

Do not rename the authority or companion files, and do not put versions in filenames —
versions are declared inside each text's header and carried by signed git tags.

## Setup and the quality gate

The single quality gate is repo hygiene, enforced both locally and in CI:

```bash
pipx install pre-commit   # once
pre-commit install        # once, per clone — wires the git hook
pre-commit run --all-files
```

CI (`.github/workflows/hygiene.yml`) runs the same `pre-commit run --all-files`, so the
gate is enforced whether or not you installed the local hook. The gate includes
[`scripts/check_drift.py`](scripts/check_drift.py) (the companion/version drift linter,
self-audit 2026-06-07/FF-004) and its self-test (self-audit 2026-06-08/FF-001;
`python3 scripts/check_drift.py --self-test`). Fitness-function ids are per-cycle, so
they are cycle-qualified wherever they outlive their cycle (see `MANIFEST.md`).

Also wire the commit-message template once per clone:

```bash
git config commit.template .gitmessage
```

## Making a change

1. Branch from `main` (`type/short-description`). `main` is protected: no direct pushes,
   no force-pushes, no deletions.
2. Make the change. Keep diffs atomic and reviewable; do not reformat unrelated text.
   Line endings are LF everywhere and enforced — never hand-fix them.
3. Run `pre-commit run --all-files` until it is clean.
4. Use [Conventional Commits](https://www.conventionalcommits.org/) (`type(scope):
   description`) and **sign** your commits. Never use `--no-verify` or any hook bypass
   (per [`AGENTS.md`](AGENTS.md)).
5. Open a PR with the provided template and let CI go green before merge.

A change to an authority text is a **minor** or **major** bump; any other (non-authority)
edit — companions, tooling, or governance — is a **patch** (see [`AGENTS.md`](AGENTS.md),
[`MANIFEST.md`](MANIFEST.md), and `CHANGELOG.md`).

## Releasing and provenance verification

Before tagging a release, run the `MANIFEST.md` drift check, then **record which release
claims were verified through which evidence lane** — these are different facts and must
not be conflated (this is the 2026-06-08/FF-002 discipline):

- **Repo-local, verifiable now:** authority versions/dates parsed from the headers, the
  drift linter and its self-test, signed tags (`git tag -v <tag>`), and local commit
  signatures (`git log --show-signature`).
- **GitHub-hosted, verifiable only via GitHub:** branch-protection settings, PR check
  rollups (Hygiene status), and merge-commit signatures (GitHub's signing key is not
  available for local verification).
- **Unavailable / not asserted:** anything that cannot be checked from either lane should
  be stated as a caveat rather than claimed.

A release note or self-audit that claims "protected `main`, green CI, signed commits"
must separate these lanes instead of asserting them as one verified fact. Every release
is a **signed** git tag whose message names the contained authority versions, with a
matching `CHANGELOG.md` entry.

An **authority cut** additionally re-attests the content-hash binding: after re-syncing
the companions and the skill to the new authority texts, regenerate the "Content-hash
binding" lines in `MANIFEST.md` with `python3 scripts/check_drift.py --print-bindings`,
**replacing** the previous lines (a duplicate line per derived file fails the gate).
The drift linter fails until the recorded hashes match the new authority content, so a
cut cannot ship a stale attestation — but the hashes only prove *when* each derived file
was last attested, not that its prose is right; semantic agreement stays on the human
reviewer (drift-check steps 4–5).

## Reporting problems

- Methodology gaps, drift, or doc errors: open an issue or PR.
- Security concerns: see [`SECURITY.md`](SECURITY.md).
