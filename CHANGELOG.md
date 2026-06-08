# Changelog

All notable changes to this package are recorded here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the package follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The package version tracks the directive set as a whole. Each authority text also
carries its own version inside its header. The versioning rule (see `MANIFEST.md`):
a change to an authority text bumps the package **minor** or **major**; a
companion-only edit bumps the **patch**.

## [1.2.0] - 2026-06-07

Cuts **Agentic Architecture Audit Specification v3.2** (was v3.1). Additive change: recognizes
`AGENTS.md` as the canonical cross-agent instruction standard, with tool-specific files
(`CLAUDE.md`, `GEMINI.md`, `.cursor/rules`) treated as bridges that should import or defer to it.
Phase 4 now inventories this cross-agent instruction contract and flags `cross-agent-instruction-drift`;
the Contract schema (§8.5) and Contract-discipline rubric (§11.3) gain the corresponding surface, flag,
and scoring language.

No phase was removed and no behavior changed for existing surfaces, so v3.1 audits remain valid. The
Profile Directive stays at **v1.4** and its profiles are consumed unchanged — its spec references are
left at their v3.1 baseline, which is additively compatible. Companions, `MANIFEST.md`, and
`CITATION.cff` are synced; the FF-004 drift linter verifies the sync. **Minor** package bump per the
versioning rule.

### Agentic Architecture Audit Specification — v3.1 → v3.2 (2026-06-07)

Additive: first-class cross-agent instruction contract handling. Surfaced by F-007 from running the
audit on this package itself — the spec had treated `AGENTS.md` as interchangeable governance rather
than the AAIF/Linux-Foundation canonical standard with a canonical↔bridge structure.

## [1.1.0] - 2026-06-07

Cuts **Project Profile Discovery Directive v1.4** (was v1.3). Additive vocabulary change: adds a
`documentation` value to the `project.kind` enum so documentation, specification, and methodology
packages classify cleanly instead of being coerced to `library`. No schema fields added or removed
and no validation behavior changed, so a v1.3 profile snapshot needs no migration.

The Agentic Architecture Audit Specification is unaffected and stays at **v3.1**. Companions,
`MANIFEST.md`, and `CITATION.cff` are synced to the new directive version; the FF-004 drift linter
(`scripts/check_drift.py`) verifies the sync. This is a **minor** package bump (an authority-text
change that is backward-compatible) per the versioning rule.

### Project Profile Discovery Directive — v1.3 → v1.4 (2026-06-07)

Additive: `project.kind` gains `documentation`. The gap was surfaced by running the audit on this
package itself — a documentation/methodology package had no fitting `project.kind` value and was
coerced to `library`.

## [1.0.0] - 2026-06-06

First public release. No code or directive behavior changed from the internal
package; this release renames the files to stable names, reconciles the internal
cross-references to those names, and adds the public-repo scaffolding (license,
citation, manifest, examples, hygiene baseline).

Contents at this release:

- **Agentic Architecture Audit Specification v3.1** (2026-05-08) — `audit-spec.md`
- **Project Profile Discovery Directive v1.3** (2026-05-23) — `profile-directive.md`
- Companions — `companions/explainer.md`, `companions/kickoff-prompt.md`
- Drift-control manifest — `MANIFEST.md`

File renames from the internal package (content preserved):

- `agentic-audit-spec-v3.md` → `audit-spec.md`
- `project-profile-directive.md` → `profile-directive.md`
- `audit-spec-friendly-explainer.md` → `companions/explainer.md`
- `audit-kickoff-prompt.md` → `companions/kickoff-prompt.md`
- `audit-directive-set-manifest.md` → `MANIFEST.md`

## Authority-text lineage

The package's first public version is 1.0.0, but the authority texts have their own
history. The relevant lineage carried into this release:

### Project Profile Discovery Directive — v1.2 → v1.3 (2026-05-23)

Validation clarifications only; no schema fields added or removed, so a v1.2 snapshot
needs no field migration. The audit specification was unaffected and stayed at v3.1.

- Citation fidelity is enforced: a cited `evidence` excerpt that names a symbol or
  quotes text must actually appear at the cited lines, and a single-line citation must
  point at the named construct, not an adjacent comment, import, or enclosing block.
- Phase H performs a content-level evidence check, not just path-exists/range-in-bounds,
  and records the verification method and any corrected mismatches.
- Dependency versions are reconciled from lockfiles when a lockfile is in scope, rather
  than cited as manifest ranges.
- `model_providers[].access_via` is checked for consistency with the hosted/local
  authority baseline, with added guidance for mapping local model execution onto the enum.

Prompted by a real first-profile run that passed path/range validation yet still shipped
two evidence excerpts naming classes absent at the cited lines and one off-by-many line
number — the exact failure mode the audit's "do not trust profile claims" rule exists
to catch downstream, now also caught upstream at profile time.

### Agentic Architecture Audit Specification — v3.0 → v3.1 (2026-05-08)

Preserves the v3 audit philosophy and adds targeted coverage for:

- protocol-specific contract surfaces, especially MCP and A2A;
- workflow descriptions, overlays, schema dialects, and protocol versions;
- background, paused, resumable, durable, callback-mediated, and event-triggered execution;
- authority matrices covering approval mode, precedence, bypass modes, protected paths,
  secondary credentials, callbacks, hosted/local boundaries, and token delegation;
- separate state and memory classes;
- separate runtime/action, content, and build/source provenance classes;
- semantic-convention version and stability pinning;
- server-exposed prompts and privileged-context injection boundaries;
- eval coverage for protocol surfaces, approval paths, async lifecycle, and memory lifecycle.

[1.2.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.2.0
[1.1.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.1.0
[1.0.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.0.0
