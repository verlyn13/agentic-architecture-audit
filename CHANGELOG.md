# Changelog

All notable changes to this package are recorded here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the package follows
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

The package version tracks the directive set as a whole. Each authority text also
carries its own version inside its header. The versioning rule (see `MANIFEST.md`):
a change to an authority text bumps the package **minor** or **major**; a
companion-only edit bumps the **patch**.

## [Unreleased]

## [1.5.0] - 2026-06-10

Cuts **Agentic Architecture Audit Specification v3.5** (was v3.4) and **Project Profile
Discovery Directive v1.6** (was v1.5) — the second dual-authority cut. Sources the
proposals queued by the 2026-06-10 cross-application review (ADR 0003), each premise
adversarially re-verified against the v3.4/v1.5 texts before drafting; one proposal
(the profile JSON Schema) remains queued as a post-cut package patch. All changes
additive; **minor** package bump per the versioning rule. Companions, `MANIFEST.md`
(including the content-hash binding re-attestation), `README.md`, `AGENTS.md`, and
`CITATION.cff` are synced; the drift linter verifies the sync. Rationale recorded in
`adr/0004-evidence-discipline-and-enforcement-honesty.md`.

### Agentic Architecture Audit Specification — v3.4 → v3.5 (2026-06-10)

- **Per-cycle id durability** (Phase 10, §10.2; optional `cycle` field in §8.11/§8.12):
  ids are monotonic-never-reused across cycles or cycle-qualified wherever cited in
  artifacts that outlive their cycle; the anchored in-run id patterns are unchanged and
  dated cycle artifacts keep bare ids.
- **Typed citation provenance** (§8.1): optional `observed_at`, `valid_until`, and
  `evidence_lane` (`repo-local | host-verifiable | unavailable`) extending
  `snapshot_ref`/`current_ref`; Phase 10.5 re-verifies through the lane and records
  `not-run` for `unavailable`.
- **Enforcement-honesty flags** (Phase 4, §8.5): `claimed-automation-absent` —
  governance/instruction text claiming automated enforcement no implemented gate backs —
  and `instruction-reference-broken` — instruction contracts citing repository artifacts
  that do not resolve in the tree.
- **Review-power proportionality** (§9.9, Phase 6, §8.7 `review-power-inversion`):
  ordered enforcement-power (`blocks-merge > blocks-commit > warn-only > prose-only`)
  and mandated-review scales with a decidable pairwise inversion condition.
- **`regression-trap` eval-suite mode** (Phase 9, §8.10): behavioral traps seeded from
  observed agent failures, with the existing demotion rule applied — an unharnessed trap
  corpus is `manual-review-only`, not coverage.
- **Metalanguage containment** (Prime Directive 16, Phase 1, Phase 5, §8.2
  `audit-taxonomy-collision`): audit-internal taxonomy is never exported into a
  project's controlled vocabulary; machine-readable schema fields stay exempt.
- **Operating-agent baseline drift** (Phase 6, §8.7 `model-alias-resolution-drift`):
  where the profile records CLI versions, model posture, and alias pins, the audit
  confirms each pin still resolves to the recorded baseline.
- **Agent-memory truth maintenance** (Phase 5, §8.6 optional `truth_maintenance`, prose
  flag `memory-truth-maintenance-absent`): whether agent-held claims have a correction
  path when repository facts change.
- **Negative-self-test rule** for implemented fitness functions (Phase 10 step 8, §8.12
  optional `negative_self_test`, §11.11 note) and a **standing-decision-ledger**
  evidence target (§11.10 note).

### Project Profile Discovery Directive — v1.5 → v1.6 (2026-06-10)

- Adds `conventions.forbidden_terms` (a structured projection of vocabulary-banning
  rules), an optional `agent_surface.operating_agents` block (observed agent CLI
  versions, model posture, and model-alias pins with resolutions and observation dates,
  citing the committed agent configuration), and `regression-trap` in the evals
  baseline — with matching Phase D/E/F discovery steps and §7 validation rules. Purely
  additive: v1.5 snapshots need no migration.

### Also included (companion/tooling, shipped unreleased on `main` before this cut)

Two patch batches (PRs #11 and #12), both sourced from the 2026-06-10 cross-application
review (run against an independently governed agentic repo, "HCS"); the report itself
stays untracked per `MANIFEST.md` ("Not bundled"). Rationale and the full disposition
record in `adr/0003-cross-application-review-dispositions.md`.

**Pre-cut gate hardening (2026-06-10, follow-through on ADR 0003):**

- **Drift linter, three new commit-blocking rules**, each shipped with a negative
  self-test wired into `--self-test`: bare per-cycle `FF-`/`F-` ids flagged on every
  tracked surface except the authority texts, `CHANGELOG.md`, `adr/`, and `examples/`
  (mechanizes the identifier convention); `MANIFEST.md` content-hash binding of the
  three derived files to the current authority texts (the review's P-013;
  `--print-bindings` regenerates the lines, cut-time re-attestation documented in
  `CONTRIBUTING.md`); and `AGENTS.md` must quote the directive's current
  `directive_version`/`audit_spec_target` schema-identifier literals, forcing the
  instruction file to update with any cut that changes either literal. `MANIFEST.md`'s
  automation claims updated to state exactly what is and is not gated.
- **`DECISIONS.md` standing decision ledger** (the review's P-012, part (a)): durable
  `D-NNN` ids seeding the thirteen dispositioned proposals with their current statuses
  (restated in package terms), the two rejected review defects with reasons, and the
  open decisions; the restatement-policing check is explicitly recorded as not built.
- **Inline `(per AGENTS.md)` cites** on the hook-bypass-ban restatements in
  `companions/kickoff-prompt.md`, `.github/pull_request_template.md`, and
  `CONTRIBUTING.md` (closes the residual the review's R-004 left behind).
- **ADR 0003 marked Accepted** (operator-approved; its patch scope landed via PR #11).

**Review dispositions (2026-06-10, landed via PR #11):**

- **Identifier convention adopted (weak form of the queued P-001):** self-audit FF/F ids
  are per-cycle and are now cycle-qualified on live, undated surfaces — `README.md`,
  `.pre-commit-config.yaml` hook display names (hook ids unchanged), `CONTRIBUTING.md`,
  and `scripts/check_drift.py` display strings (e.g. `2026-06-07/FF-004`,
  `2026-06-08/FF-001`). Convention recorded in `MANIFEST.md`. Resolves the review's
  confirmed defects R-001/R-002.
- **Two review defects refuted on adversarial re-verification** and recorded in ADR 0003
  so they are not re-raised: R-003 (`.codex/` is gitignored personal scaffolding, never
  shipped) and R-004 (the `--no-verify` ban has eight statements, not five, with
  `AGENTS.md` as the named canonical home).
- **Review-input handling:** `.gitignore` now excludes `/improvement-report-*.md`;
  the convention (untracked input evidence, transcribed via ADR) is documented in
  `AGENTS.md`.
- **Instruction-file currency** (`AGENTS.md`, `CLAUDE.md`): the stale
  `directive_version` example literal updated to the v1.5 value and the pinned
  `audit_spec_target` v3.1 consumption baseline explained (do not "fix" it as drift);
  drift-linter behavior, scope, and commit-blocking rules documented; the
  `.agents/skills/run-agentic-audit/SKILL.md` derived surface, ADR convention,
  release/provenance steps, and published repo slug recorded.
- **Queued for a future deliberate cut** (Audit Spec v3.5 / Profile Directive v1.6):
  thirteen additive proposals, dispositioned in ADR 0003's table — shipped by this
  release's authority cut, except the profile JSON Schema (still queued as a post-cut
  package patch) and the content-hash binding (already shipped in the gate hardening).

## [1.4.0] - 2026-06-09

Cuts **Agentic Architecture Audit Specification v3.4** (was v3.3) and **Project Profile
Discovery Directive v1.5** (was v1.4) — the first dual-authority cut. Driven by a verified
standards-currency review (2026-06-09) of the mid-2026 agentic landscape: MCP's task/extension/
deprecation lifecycle, the cross-tool Agent Skills standard, agent identity and delegated
commerce, and the customization supply chain. All changes are additive; **minor** package
bump per the versioning rule. Companions, `MANIFEST.md`, `README.md`, and `CITATION.cff`
are synced; the FF-004 drift linter verifies the sync. Rationale recorded in
`adr/0002-skills-as-contracts-and-protocol-object-lifecycle.md`.

### Agentic Architecture Audit Specification — v3.3 → v3.4 (2026-06-09)

- **Agent-skill packages become first-class contracts and authority surfaces** (§5.1, §6.3,
  Phases 4 and 6, §8.5, §8.7, §9.1, §11.3, §14): frontmatter contracts, capability
  pre-approvals (e.g., `allowed-tools`), bundled executables, and source/marketplace
  provenance are inventoried and flagged — prose instructions remain governance, checked in
  Phase 8.
- **Protocol-object lifecycle status** is recorded against the pinned protocol revision
  (Phase 0, Phase 4, §8.5 `protocol_object_status`, §14), so the inventory tracks
  deprecations and extensions instead of hard-coding an object list; protocol tasks,
  extension declarations, server-delivered UI surfaces, and registry/discovery metadata
  become inventoryable objects.
- **Agent identity and delegated commerce** join Phase 6 and the §9.7 authority matrix
  (commerce checks apply only where an agent can initiate or approve payments).
- **Customization supply-chain** checks (skills/hooks/plugins/protocol-server configuration
  consumed by repo-operating agents) join the agent-operability lens; the §11.6 isolation
  baseline is calibrated (OS-level or micro-VM sandbox, write-allowlists, default-deny egress).
- Hosted-eval **platform-lifecycle** flag (Phase 9); refreshed §14 reference anchors.
- Additive only: v3.3 audits remain valid; v1.4 profiles are consumed unchanged.

### Project Profile Discovery Directive — v1.4 → v1.5 (2026-06-09)

- Adds `agent_surface.skills`, MCP task/extension/server-delivered-UI/deprecated-objects
  fields, a `commerce` protocol-surface block, and committed repo-operating-agent
  configuration + agent-identity-attestation fields in the authority baselines, with
  matching Phase D/E/F discovery steps and validation rules. Purely additive: v1.4
  snapshots need no migration.

### Also included (companion/tooling, from the 2026-06-08 self-audit follow-ups)

Resolves the three remaining findings from the 2026-06-08 self-audit (shipped unreleased
on `main` before this cut):

- Drift linter (`scripts/check_drift.py`): the section-reference check now resolves each
  reference against the **specific** authority text its line names, instead of accepting
  any number present in either text. This closes self-audit **F-001** (FF-001), where a
  reference attributed to the profile directive but naming an audit-spec-only section
  passed. Correctly-attributed and unattributed references are unaffected.
- `scripts/check_drift.py --self-test`, wired as its own pre-commit hook, locks in the
  FF-001 negative test so the F-001 regression cannot return silently.
- `CONTRIBUTING.md` and `SECURITY.md` (self-audit **F-003** / FF-003): contribution and
  release workflow, and security scope with private vulnerability reporting.
- A release-provenance verification discipline (self-audit **F-002** / FF-002),
  documented in `CONTRIBUTING.md` and pointed to from `MANIFEST.md`: release claims must
  separate repo-local, GitHub-hosted, and unavailable evidence lanes.

## [1.3.0] - 2026-06-08

Cuts **Agentic Architecture Audit Specification v3.3** (was v3.2). Additive: adds the
`agent-operability` **strategic-theme lens** (§2.3, §11.12) — it reweights existing dimensions
(§11.3 / §11.6 / §11.10 / §11.11) at 1.5× and adds **no** scored dimension, preserving the
min-aggregation rule — plus a repo-operating-agent authority clause (§11.6), a developer-agent-workflow
scope boundary (§0), and Appendix D. The rationale (a theme, deliberately not a scored dimension) is
recorded in the package's first ADR, `adr/0001-agent-operability-as-theme.md`.

No phase or scoring change for existing surfaces, so v3.2 audits remain valid. The Profile Directive
stays **v1.4**, consumed unchanged. Companions, `MANIFEST.md`, and `CITATION.cff` are synced; the
FF-004 drift linter verifies the sync. **Minor** package bump per the versioning rule.

### Agentic Architecture Audit Specification — v3.2 → v3.3 (2026-06-08)

Resolves self-audit **F-008** by adopting agent-operability as a theme lens rather than a scored
dimension — avoiding the orthogonality / min-aggregation cost a dimension would impose. Surfaced a
separate confirmed finding **F-012** (MANIFEST over-claims `check_drift.py`'s section-number coverage),
tracked as its own workstream.

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

[Unreleased]: https://github.com/verlyn13/agentic-architecture-audit/compare/v1.5.0...HEAD
[1.5.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.5.0
[1.4.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.4.0
[1.3.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.3.0
[1.2.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.2.0
[1.1.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.1.0
[1.0.0]: https://github.com/verlyn13/agentic-architecture-audit/releases/tag/v1.0.0
