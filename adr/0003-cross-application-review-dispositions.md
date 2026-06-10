# ADR 0003 — Identifiers are cycle-qualified now; thirteen cross-application proposals are queued for the next cuts

- **Status:** Proposed — 2026-06-10 (package-level patch fixes applied with this ADR; the
  queued authority-text proposals await an operator-approved Audit Spec v3.5 / Profile
  Directive v1.6 cut)
- **Decider:** Jeffrey V. Johnson
- **Source:** cross-application review, 2026-06-10 — the spec and directive were run in
  comparison against an independently governed agentic substrate repo ("HCS": a typed
  ontology + policy substrate with charter invariants, a decision ledger, CI gates, and
  reviewer subagents); each mechanism was tested in both directions and adversarially
  critiqued. The review report is input evidence per `MANIFEST.md` ("Not bundled") and
  stays untracked; this ADR transcribes everything with standing. Before transcription,
  each of the report's four package-defect claims (all asserted at confidence 1.0) was
  independently re-verified against HEAD `5688a0a` by a second, adversarial agent pass on
  2026-06-10: two confirmed (R-001, R-002), two refuted (R-003, R-004).
- **Affects:** package only at this revision (patch-level): `README.md`,
  `.pre-commit-config.yaml`, `CONTRIBUTING.md`, `MANIFEST.md`, `.gitignore`,
  `scripts/check_drift.py` display strings, plus instruction-file currency in `AGENTS.md`
  and `CLAUDE.md`. No authority text is touched. The queued proposals would affect both
  authority texts in a future deliberate cut (Audit Spec v3.4 → v3.5, Profile Directive
  v1.5 → v1.6).

## Context

**What held up (recorded before the critique, per the finding discipline).** The
cross-application validated the package's core design choices, and nothing below weakens
them: the discover-then-judge split (HCS's worst governance failure — stale milestone
prose surviving five document generations — is exactly the failure class the split
catches); the drift linter's design (HCS independently reinvented two of its signature
moves, consumer-scope exclusions and quoted-content escapes — convergent evolution under
different pressures); the self-test-for-the-fitness-function pattern (the always-run
`drift-check-selftest` hook); and ADR 0001's proportionality reasoning together with the
fully closed self-audit loop.

**The four defect claims, adversarially re-verified.** The review asserted four package
defects at confidence 1.0. A second, independent pass instructed to *refute* each claim
against HEAD confirmed two and refuted two:

1. **R-001 confirmed.** `README.md` labeled `scripts/check_drift.py` with the bare
   cycle-1 id FF-004 while cycle 2 (2026-06-08) restarted the FF namespace. The ambiguity
   is not hypothetical: cycle-1 FF-001 ("cross-agent instruction presence") and cycle-2
   FF-001 ("authority-specific section-reference validation") are different rules, and
   the defining artifacts live in gitignored `audit/<date>/` directories, so at HEAD a
   bare FF id resolves to nothing in-repo.
2. **R-002 confirmed.** `.pre-commit-config.yaml` named the drift hook "(FF-004)"
   (cycle-1 id) a few lines above its self-test "(FF-001)" (cycle-2 id), unqualified —
   violating the package's own recorded hygiene rule (ADR 0001, Carve-out 2, "ID
   hygiene"). The root cause is structural (per-cycle namespaces), which is why P-001
   stays queued even after the patch fix.
3. **R-003 refuted.** The cited `.codex/hooks.json` absolute path is real, but the file
   is gitignored personal scaffolding ("Local, personal agent settings — never
   committed") and never ships; the tracked Claude wiring already uses the portable
   `$CLAUDE_PROJECT_DIR` form. The harm premise — "breaks on any clone path other than
   the author's" — fails because on any other clone the file does not exist. The
   2026-06-08 self-audit had already recorded `.codex/` as correctly local-only;
   mistaking local machine state for repo content is a known false-positive class.
4. **R-004 refuted as stated.** The `--no-verify` ban appears in at least eight places,
   not five — the review missed the three most significant, including `AGENTS.md` (the
   declared canonical cross-agent instruction file) and a statement in the audit spec
   itself — and a canonical source IS named: `.gitmessage` cites AGENTS.md by name, and
   the skill labels its list a "reminder checklist" with a "Source of truth" section.
   Residual, non-defect observation: three restatements carry no inline cite, and the
   drift linter does not police the restatement set; both fold into P-013's scope.

That two confidence-1.0 claims failed adversarial re-verification is itself a live
demonstration of the discover-then-judge split: the report was discovery; this ADR is
judgment. (Note the failures were *inference* errors on accurate observations — tracked
state and rule-source were misjudged, not stale — so they motivate the judgment split,
not P-002's freshness fields; P-002 stands on its own evidence.)

## Decides

1. **FF and finding ids are cycle-qualified in any artifact that outlives its cycle**
   (the form is `2026-06-07/FF-004`, `2026-06-08/FF-001`), effective now at package
   level. Applied to `README.md`, the `.pre-commit-config.yaml` hook display names (hook
   ids `drift-check`/`drift-check-selftest` unchanged — CI behavior is identical),
   `CONTRIBUTING.md`, and the `scripts/check_drift.py` docstring and printed summary
   strings. The convention is recorded in `MANIFEST.md` ("Identifier convention"). This
   is the weak form of P-001; the strong form — a rule in Audit Spec §10 making ids
   monotonic-never-reused or mandatorily cycle-qualified — remains queued for v3.5.
2. **R-003 and R-004 are rejected as package defects**, with the refutations recorded in
   Context so they are not re-raised. R-004's residual folds into P-013.
3. **The review report stays untracked**, per `MANIFEST.md` ("Not bundled"):
   `.gitignore` now excludes `improvement-report-*.md`, `AGENTS.md` documents the
   convention, and this ADR is the durable transcription.
4. **The thirteen authority-text proposals are queued, not cut**, with these
   dispositions:

| Item | Substance | Vehicle | Priority |
| --- | --- | --- | --- |
| P-001 | Durable (never-reused) or cycle-qualified FF/finding ids as a rule in Audit Spec §10 | v3.5 cut | High |
| P-003 | Named claimed-automation-absent flag: every "CI-enforced / blocked at merge" claim must map to an implemented gate | v3.5 cut | High |
| P-004 | Named instruction-reference-broken flag: instruction contracts citing artifacts that do not exist in the tree | v3.5 cut | High |
| P-005 | Review-power proportionality inversion check: mandated review friction vs actual enforcement power per surface | v3.5 cut | High |
| P-007 | Metalanguage containment: audit-internal taxonomy never injected into a project with a controlled vocabulary; the profile may declare forbidden terms | v3.5 + v1.6 cut | High |
| P-008 | Operating agents' model/CLI baseline and alias-resolution drift captured in the profile's agent surface, checked for drift in the audit | v1.6 + v3.5 cut | High |
| P-009 | Agent-memory-vs-repo-truth drift: memory stores' invalidation discipline as an evidence target | v3.5 cut | High |
| P-002 | Typed citation provenance: observed-at / valid-until / evidence-lane fields in the citation schema | v3.5 cut | Medium |
| P-006 | Regression-trap corpora as a first-class suite class, with the FF demotion rule applied honestly | v3.5 cut | Medium |
| P-010 | Negative self-tests for implemented fitness functions as a stated rule (names the package's own proven pattern) | v3.5 cut | Medium |
| P-011 | JSON Schema for the profile artifact, validated mechanically in the quality gate | Tooling + derived artifact (package patch) | Medium |
| P-013 | Content-hash binding of companions to authority texts, checked by the drift linter; absorbs R-004's residual | Tooling (package patch) | Medium |
| P-012 | Standing decision ledger: package practice now; an evidence target at the next cut | Practice now; v3.5 evidence target | Medium |

## Scopes to

This revision edits: `README.md` (cycle-qualified drift-linter row),
`.pre-commit-config.yaml` (hook display names and comments), `CONTRIBUTING.md` (qualified
ids plus the convention pointer), `MANIFEST.md` (identifier convention), `.gitignore`
(review-input pattern), `scripts/check_drift.py` (docstring and printed summary strings
only; no check logic changed), and `AGENTS.md`/`CLAUDE.md` (instruction-file currency:
the stale `directive_version` example literal updated to the v1.5 value, the pinned
consumption baseline explained, drift-linter behavior and the ADR/release/review-input
conventions documented). Authority texts untouched; the package bump is a **patch**.

## Does not decide

- **Does not cut Audit Spec v3.5 or Profile Directive v1.6.** Authority revisions are
  deliberate, operator-approved events; this ADR queues and shapes them. A future cut
  would follow the ADR 0002 pattern: additive, no renumbering, nothing breaking a v3.4
  audit or a v1.5 profile.
- **Does not choose between the strong and weak id forms.** Monotonic never-reused ids
  versus mandatory cycle qualification is a v3.5 decision; the package convention adopted
  here is compatible with either.
- **Does not import HCS vocabulary or mechanisms wholesale.** Each proposal was restated
  in this package's terms; what HCS bans or builds is evidence, not authority.

## Carve-outs

1. **Bare ids remain valid inside their own dated context.** `CHANGELOG.md` entries sit
   under dated release headings, and the gitignored `audit/<date>/` and `profile/<date>/`
   artifacts are frozen cycle records — rewriting them would conflict with the
   provenance discipline. Only undated, long-lived surfaces cycle-qualify.
2. **Third-party FF namespaces are out of scope.** `examples/README.md` cites the
   shelltutor run's adopted FF-001..FF-007 — that is the target project's namespace,
   contextualized by its own documentation, and not this package's to rename.
3. **The local `.codex/` wiring stays personal.** If shared Codex wiring is ever wanted,
   it is promoted deliberately — un-ignored, tracked, and made path-portable — not
   patched in place while untracked.

## Consequences

- The package now exhibits the identifier discipline it audits for; future cycles' ids
  are born qualified, and the structural fix (P-001) has a recorded landing site.
- Two refuted defects are on record with reasons, so the review's defect section cannot
  be re-raised wholesale; the surviving residuals have a named home (P-013).
- The verification asymmetry is explicit: package-defect claims were re-verified
  firsthand at HEAD; the HCS-side evidence (its trap corpus, its ledger, its CI gaps)
  was *not* independently re-verified here and enters only as motivation for queued
  proposals, never as fact about this package.
- `AGENTS.md` and `CLAUDE.md` now document the conventions agents kept tripping over
  (drift-linter scope and rules, the pinned v3.1 consumption baseline, review-input
  handling), shrinking the most likely class of future false-positive drift reports.
- Acting on the queued table is the next deliberate event; when it happens, this ADR is
  its source and the sourcing line mirrors ADR 0002's: an external review tested the
  texts' claims — here against a live, governance-heavy agentic repo — rather than
  trusting either the texts or model training data.
