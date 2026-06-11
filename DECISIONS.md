# Decisions ledger

Standing record of package-level decisions: queued proposals, rejections with reasons,
and open questions. `D-NNN` ids are **durable** — never reused, never renumbered; a
reversed decision keeps its id and gains a superseding entry. Decision *events* are
still recorded as ADRs in `adr/` (the ADR carries the full rationale; this ledger is the
"is this settled?" index). Adopted as package practice 2026-06-10 via
`adr/0003-cross-application-review-dispositions.md` (the review's P-012, part (a));
making such a ledger an audit evidence target is itself queued below (D-012).

Substance below is **restated in this package's terms** from its sources — the P-NNN /
R-NNN ids are the 2026-06-10 cross-application review's namespace, transcribed through
ADR 0003 (the report itself is untracked input evidence per `MANIFEST.md`, "Not
bundled"). No automated check polices that a ledger entry faithfully restates its
source; that restatement-policing check is **not built**. (Stating that here keeps this
file out of the over-claim class recorded in ADR 0001's Consequences, where `MANIFEST.md`
once promised automation the drift linter did not implement.) Entries also carrying
drafting constraints from the *2026-06-10 forward plan* — an operator-session plan, not
a tracked artifact — name it in their Source line; the ledger entry itself is that
plan's durable record.

## Queued — authority-text proposals (next deliberate cut: Audit Spec v3.5 / Profile Directive v1.6)

All additive: no phase renumbering, no new scored dimension, new fields optional; a
v3.4 audit and a v1.5 profile stay valid. Before drafting, each premise is
adversarially re-verified against the then-current texts (two of the source review's
confidence-1.0 claims died exactly that way — see D-014/D-015).

### D-001 — Durable or cycle-qualified finding/fitness-function ids as a spec rule
- **Status:** Queued (Audit Spec v3.5) · **Source:** ADR 0003 (P-001) · **Priority:** High
- The audit spec's Phase 10 gains a rule (the sources write "Audit Spec §10"; this
  ledger normalizes to the Phase 10 rule cluster — its numbered 10.1/10.2 subsections —
  since the §10 worked example carries no rules): per-cycle finding and fitness-function
  ids are either monotonic and never reused across cycles (the strong form), or
  mandatorily cycle-qualified (`YYYY-MM-DD/` prefix) in any artifact that outlives its
  cycle — READMEs, configs, instruction files, commit messages. (The source proposal
  also listed ADRs; this package's own convention exempts ADRs as dated artifacts —
  the spec rule's final scope is decided at the cut.) The rule governs ids **as cited**
  in long-lived artifacts; the anchored in-run id patterns in the audit spec's
  §8.11/§8.12 schemas stay unchanged (a qualified id would violate them — at most an
  optional sibling cycle field is added). The package already practices and mechanically
  enforces the weak form (see `MANIFEST.md`, "Identifier convention"). Strong-vs-weak is
  open as D-016.

### D-002 — Typed citation provenance (freshness as data, not ceremony)
- **Status:** Queued (Audit Spec v3.5) · **Source:** ADR 0003 (P-002) + the 2026-06-10
  forward plan · **Priority:** Medium
- The citation schema (path / lines / evidence / method, plus the existing
  `snapshot_ref`/`current_ref` pair) gains optional observed-at, valid-until, and
  evidence-lane fields, promoting the three release-provenance lanes (repo-local /
  GitHub-hosted / unavailable, already in `CONTRIBUTING.md`; the spec enum will need
  tool-neutral lane naming per ADR 0001's drafting carve-out) from prose into the
  schema — so steady-state and focused-diff consumers of prior findings see a staleness
  window per citation instead of trusting one ship-time re-verification. Designed
  **jointly with D-008**; the new fields extend `snapshot_ref`/`current_ref`, never
  duplicate them.

### D-003 — Named claimed-automation-absent flag
- **Status:** Queued (Audit Spec v3.5) · **Source:** ADR 0003 (P-003) · **Priority:** High
- A named flag for governance or instruction text that claims automated enforcement
  which does not exist: every "CI-enforced", "blocked at merge", "automated by X" claim
  must map to an implemented gate, else it is flagged. The class is proven three times
  across two governed repos (this package's own over-claim recorded in ADR 0001's
  Consequences; two instances in the reviewed substrate repo); today it is only found
  incidentally.

### D-004 — Named instruction-reference-broken flag
- **Status:** Queued (Audit Spec v3.5) · **Source:** ADR 0003 (P-004) · **Priority:** High
- The cross-agent instruction-contract checks gain a flag for instruction contracts
  citing artifacts that do not exist in the tree (e.g. a definition-of-done requiring a
  checklist from a template the repo does not contain). An unsatisfiable checklist item
  silently trains agents to skip checklist items.

### D-005 — Review-power proportionality inversion check
- **Status:** Queued (Audit Spec v3.5, **drafted last, with drop authority**) ·
  **Source:** ADR 0003 (P-005) + the 2026-06-10 forward plan · **Priority:** High
- Map mandated review/approval friction against actual enforcement power per surface and
  flag inversions: hard-enforcing surfaces (e.g. scripts whose gates block merges) that
  carry no review requirement while weaker, warn-only surfaces carry heavy ones. The
  audit records authority facets and governance separately today; the *ratio* is where
  the reviewed repo's real gap hid. **Caveat:** sole-source evidence from one external
  repo, never independently re-verified here. If it cannot be worded operationally
  (blocks-merge / blocks-commit / warn-only / prose) **and** tool-neutrally at drafting
  time, it is moved to this ledger as Dropped with revival condition "corroborated by a
  second target repo" (open as D-017).

### D-006 — Regression-trap corpora as a first-class suite class
- **Status:** Queued (Audit Spec v3.5) · **Source:** ADR 0003 (P-006) · **Priority:** Medium
- The Phase 9 suite classification gains a regression-trap class: behavioral traps
  seeded from *observed agent failures* (distinct from code regression tests), with the
  existing fitness-function demotion rule applied honestly — a trap corpus with no
  runnable harness is recorded as manual-review-only, not as coverage. **Drafting
  constraint:** the suite-mode enum is closed and declared twice — in the audit spec's
  §8.10 EvalSuite schema *and* in the Phase 9 prose — so both are extended in the same
  commit.

### D-007 — Metalanguage containment (vocabulary-collision safety)
- **Status:** Queued (Audit Spec v3.5 + Profile Directive v1.6) · **Source:** ADR 0003 (P-007) · **Priority:** High
- Three parts, shipped together: (a) a Phase 5 note that the audit's store-class enum
  values (`long-term-memory`, `operator-rules-memory`, …) are audit-internal taxonomy,
  never recommended project vocabulary; (b) the profile directive's §5 schema may
  declare forbidden terms the project's governance bans; (c) audit artifacts must
  restate such terms in the project's canonical vocabulary, and the Phase 1 collision
  check includes collisions between the audit's taxonomy and the project's controlled
  vocabulary. A project that hard-bans a term (the reviewed repo bans calling shared
  state "memory") must never have it injected by the audit's own artifacts.

### D-008 — Operating agents' model/CLI baseline and alias-resolution drift
- **Status:** Queued (Profile Directive v1.6 + Audit Spec v3.5) · **Source:** ADR 0003
  (P-008) + the 2026-06-10 forward plan · **Priority:** High
- The profile's agent surface gains: observed agent CLI version(s), observed model
  posture, and any alias pins (e.g. a settings file pinning a model alias) with what the
  alias currently resolves to; the audit gains a drift check for alias pins that no
  longer resolve to the recorded baseline. Silent vendor-side repointing of an alias is
  a failure class for every agent-operated repo, and the profile currently has no field
  where it would surface. Designed **jointly with D-002** (same freshness machinery).

### D-009 — Agent-memory-vs-repo-truth drift as an evidence target
- **Status:** Queued (Audit Spec v3.5) · **Source:** ADR 0003 (P-009) · **Priority:** High
- Where operator-rules/agent-memory stores exist, the audit records whether the project
  has an invalidation discipline — how agent-held claims get corrected when repo facts
  change — and flags memory surfaces with no such path. The spec inventories memory
  stores' owners and retention, but not their truth-maintenance relationship to the
  repo.

### D-010 — Negative self-tests for implemented fitness functions as a stated rule
- **Status:** Queued (Audit Spec v3.5) · **Source:** ADR 0003 (P-010) · **Priority:** Medium
- An implemented fitness function with non-trivial matching logic should ship a negative
  self-test wired to run wherever the fitness function runs; one without it carries
  reduced confidence in scoring. This names the package's own proven in-house pattern
  (the always-run drift-linter self-test hook) as a rule for adopters.

## Queued — package tooling (no authority-text change required)

### D-011 — JSON Schema for the profile artifact, validated mechanically
- **Status:** Queued (package patch, authored **after** the v1.6 cut so the new fields
  are included) · **Source:** ADR 0003 (P-011) + the 2026-06-10 forward plan ·
  **Priority:** Medium
- Ship a JSON Schema for `project_profile.yaml` as a derived artifact and validate it in
  the quality gate, with known-good and poisoned fixtures in the linter's `--self-test`.
  The profile schema currently exists only as prose in the profile directive's §5; the
  directive's procedural validations (citation fidelity, lockfile-over-manifest) stay
  agent-side — structural validity becomes mechanical.

### D-012 — Standing decision ledger
- **Status:** Practice **implemented** 2026-06-10 (this file); the audit-spec evidence
  target (does the project maintain a standing open-question queue distinct from its
  ADRs? — a §11.10 governance item) is Queued (Audit Spec v3.5) · **Source:** ADR 0003
  (P-012) · **Priority:** Medium

### D-013 — Content-hash binding of derived files to the authority texts
- **Status:** **Implemented** 2026-06-10 (gate hardening; `MANIFEST.md` "Content-hash
  binding" + drift-linter check with negative self-test) · **Source:** ADR 0003 (P-013) ·
  **Priority:** Medium
- Each derived file is attested against the sha256 of the authority texts it was last
  synced to; the linter fails on divergence; a cut re-attests after re-syncing. Absorbs
  the residual of D-015: the inline `(per AGENTS.md)` cites were added 2026-06-10, and
  what the binding deliberately does **not** prove (semantic agreement of restatements)
  stays human review, per `MANIFEST.md`.

## Rejected (do not re-raise without new evidence)

### D-014 — Review claim R-003 (non-portable local hook wiring) — Rejected 2026-06-10
- The cited absolute-path file is gitignored personal scaffolding that never ships; the
  tracked wiring already uses the portable form; the harm premise ("breaks on any other
  clone") fails because the file does not exist on any other clone. Mistaking local
  machine state for repo content is a recorded false-positive class. Full refutation in
  ADR 0003, Context.

### D-015 — Review claim R-004 (rule restated five times, no canonical source) — Rejected as stated 2026-06-10
- The hook-bypass ban appears in at least eight tracked statements, not five; a
  canonical source **is** named: `.gitmessage` cites `AGENTS.md` by name, and the skill
  labels its list a reminder checklist with its own source-of-truth section (two
  separate mitigations, per ADR 0003). Residual accepted, not the claim: three restatements lacked
  inline cites (added 2026-06-10, per ADR 0003 through D-013's scope), and no automated
  check polices the restatement *set* — that check remains unbuilt (see the header
  note). Full refutation in ADR 0003, Context.

## Open

### D-016 — Strong vs. weak form of the id rule (decides D-001's final shape)
- **Status:** Open; decided at the v3.5 cut · **Source:** ADR 0003 ("Does not decide")
- Monotonic never-reused ids versus mandatory cycle-qualification. The package's adopted
  convention (cycle-qualification on undated surfaces) is compatible with either.

### D-017 — Ship or drop the proportionality-inversion check (D-005)
- **Status:** Open; decided last during v3.5 drafting, with drop authority · **Source:**
  ADR 0003 + the 2026-06-10 forward plan
- Drop condition: cannot be worded operationally and tool-neutrally. Revival condition
  if dropped: corroborated by a second target repo.

### D-018 — Tag `v1.4.1` if the cut stalls
- **Status:** Open; tripwire date 2026-06-24 · **Source:** 2026-06-10 forward plan
- The landed patches (PR #11, gate hardening) ride untagged into the next minor by
  precedent. If the v3.5/v1.6 cut has not started by the tripwire date, propose tag
  `v1.4.1` so they do not sit unreleased.
