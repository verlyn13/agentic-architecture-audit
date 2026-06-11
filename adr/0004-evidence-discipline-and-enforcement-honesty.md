# ADR 0004 — Evidence gets typed freshness and durable ids; enforcement claims get tested against implemented gates

- **Status:** Accepted — 2026-06-11 (operator-approved; applied via Audit Spec v3.5 /
  Profile Directive v1.6, PR #13 / package 1.5.0)
- **Decider:** Jeffrey V. Johnson
- **Source:** the thirteen proposals queued by
  `adr/0003-cross-application-review-dispositions.md` (P-001..P-010 and P-012's
  evidence-target half; P-011 remains queued post-cut, P-013 shipped earlier as package
  tooling), as restated in `DECISIONS.md` D-001..D-010/D-012. Before drafting, every
  proposal's premise was re-verified against the v3.4/v1.5 texts by twelve parallel
  adversarial verification agents (2026-06-10) — the same discipline that previously
  killed two confidence-1.0 claims. All premises held; four held only in reshaped form,
  and the reshapes below are theirs.
- **Affects:** both authority texts. Agentic Architecture Audit Specification v3.4 → v3.5
  and Project Profile Discovery Directive v1.5 → v1.6 (package 1.4.0 → 1.5.0). All
  changes additive; no phase removed, no scored dimension added, no renumbering.

## Context

The 2026-06-10 cross-application review ran this package's texts against an
independently governed agentic repo and surfaced failure classes the spec had no
vocabulary for. ADR 0003 confirmed the package-level instances, queued the
authority-text generalizations, and `DECISIONS.md` carried the drafting constraints.
Three clusters survived premise re-verification:

1. **Evidence discipline.** Per-cycle ids collide across cycles on long-lived surfaces
   (proven in this package: R-001/R-002); citations carry revision identity
   (`snapshot_ref`/`current_ref`) but no capture time, trust horizon, or re-verification
   channel, so steady-state consumers of prior findings inherit an invisible staleness
   window; and the package's own proven negative-self-test pattern (the drift linter's
   always-run self-test) was stated nowhere as a rule for adopters.
2. **Enforcement honesty.** Three instances across two well-governed repos of governance
   text claiming automation that does not exist; instruction contracts citing artifacts
   absent from the tree; and a real gap that hid in the *ratio* between mandated review
   friction and actual enforcement power (a repo whose only merge-blocking directory
   appeared in no review lens while warn-only surfaces carried two).
3. **Boundary hygiene.** The audit's own taxonomy can contaminate a project with a
   controlled vocabulary; operating-agent model aliases can be repointed vendor-side
   with no repo change; agent memory can hold claims the repo has outgrown, with no
   recorded correction path; trap corpora seeded from observed agent failures had no
   suite class; and no evidence target asked whether a project keeps a standing
   decision ledger distinct from its ADRs.

**Premise reshapes from re-verification (recorded so the cut is sourced honestly):**

- **P-006:** the closed eval-mode list is declared in *four* places, not the queued two —
  audit spec Phase 9 prose and §8.10, plus directive Phase F prose and
  `baselines.evals.modes_present` — so the cut extends all four in the same commit.
- **P-009:** the claim "nothing records an invalidation path" was overstated — Phase 5
  and §8.6 already record `invalidation_trigger`, and §11.5 level 3 already scores
  invalidation enforcement. The genuine gap is the *discipline* question (does any
  correction path for agent-held claims exist when repo facts change) and a flag for its
  absence; the edit extends `invalidation_trigger` rather than duplicating it.
- **P-005:** the D-017 drop condition (cannot be worded operationally and tool-neutrally)
  was tested and **not met**: two short ordered scales and a decidable pairwise
  inversion condition ship as §9.9. The sole-source caveat stands: the motivating
  evidence is one external repo, never independently re-verified here.
- **P-012b:** the §11.10-L3 ADR-template item predates ADR 0001 — it shipped with the
  spec's initial public release; ADR 0001 brought this package into compliance with it.
  The provenance is corrected here rather than repeated wrong.

## Decides

1. **Ids carry a recorded per-cycle discipline** (audit spec Phase 10 step 4, §10.2):
   either monotonic-never-reused across cycles, or cycle-qualified (`YYYY-MM-DD/`)
   wherever cited in artifacts that outlive the cycle. Either discipline satisfies the
   rule — this resolves the open D-016 by admitting both, recorded once per project.
   The anchored in-run id patterns in §8.11/§8.12 are unchanged; an optional `cycle`
   field carries the qualifier in structured outputs. Dated cycle artifacts keep bare
   ids.
2. **Citations carry typed freshness** (§8.1): optional `observed_at`, `valid_until`,
   and `evidence_lane` (`repo-local | host-verifiable | unavailable`) extend
   `snapshot_ref`/`current_ref` — which revision vs. when captured, how long trustable,
   through what channel re-verifiable. Phase 10.5 records `not-run` through the lane.
   The lane enum is self-contained and tool-neutral; it is a re-verification lane,
   deliberately not named a "provenance" class (§9.8 owns that word).
3. **Two named flags test enforcement claims on the contract surface** (Phase 4, §8.5):
   `claimed-automation-absent` (text claims automation no implemented gate backs;
   honestly-manual rules are not flagged; approval-gate claims on principals stay with
   Phase 6's `approval-not-enforced`) and `instruction-reference-broken` (instruction
   contracts citing repository artifacts that do not resolve; environment-resolved
   commands out of scope; content staleness stays Phase 8).
4. **Review-power proportionality becomes a decision matrix** (§9.9, Phase 6, §8.7
   `review-power-inversion`): ordered enforcement-power and mandated-review scales with
   a decidable inversion condition; Phase 4's gate confirmation uses the same power
   classes, so the cut defines enforcement power exactly once. This resolves the open
   D-017 as **ship**.
5. **`regression-trap` joins the eval-suite modes in all four declarations** (audit spec
   Phase 9 + §8.10; directive Phase F + `modes_present`), with the existing Phase 10.5
   demotion rule applied by reference: an unharnessed trap corpus is
   `manual-review-only`, not coverage.
6. **The audit contains its own metalanguage** (Prime Directive 16, Phase 1 step 6 +
   `audit-taxonomy-collision` in §8.2, Phase 5 note; directive
   `conventions.forbidden_terms` + Phase D discovery + §7 validation): audit-internal
   taxonomy is never exported into a project's controlled vocabulary; prose artifacts
   restate banned terms in the project's canonical vocabulary while machine-readable
   schema fields keep taxonomy values.
7. **Operating-agent baselines become drift-checkable** (directive
   `agent_surface.operating_agents` + Phase E + §7; audit Phase 6 + §8.7
   `model-alias-resolution-drift`): observed CLI versions, model posture, and alias pins
   with resolutions and observation dates, citing the committed agent configuration
   Phase F already inventories; the audit confirms pins still resolve to the recorded
   baseline, conditionally on the profile recording them.
8. **Agent-memory truth maintenance becomes an evidence target** (Phase 5, §8.6 optional
   `truth_maintenance`, prose flag `memory-truth-maintenance-absent`): whether agent-held
   claims have a correction path when repository facts change — extending
   `invalidation_trigger`, with staleness-of-authored-files left to Phase 8 and
   tested-ness left to Phase 9.
9. **Negative self-tests for implemented fitness functions become a stated rule**
   (Phase 10 step 8, §8.12 optional `negative_self_test`, §11.11 note): an implemented
   fitness function with non-trivial matching logic and no negative self-test earns
   reduced credit. This names the package's own proven pattern for adopters.
10. **A standing decision ledger becomes a governance evidence target** (§11.10 note;
    decision ledgers join the Phase 8.1 policy-artifact locate list): durable
    never-reused ids with queued/rejected/open statuses, distinct from ADRs and from
    audit-cycle history, cross-referencing both.

## Scopes to

Audit spec: §1.2, §3 (Prime Directive 16), Phases 1, 4, 5, 6, 8.1, 9, 10, 10.5 gain
steps, flag bullets, locate-list items, notes, or exit-check lines; schemas §8.1, §8.2, §8.5, §8.6, §8.7, §8.10,
§8.11, §8.12 gain optional fields or enum values; §9.9 is appended after §9.8; §11.10
and §11.11 gain italic notes; §16 gains the v3.5 changes block; Appendix F is appended.
Profile directive: header and §13 lineage; §5 schema gains `conventions.forbidden_terms`
and `agent_surface.operating_agents` and extends `modes_present`; Phases D, E, F gain
discovery steps; §7 gains three validation rules; §10's consumption list gains two
lines (per the v1.5 precedent). The `meta` example bumps `profile_version`/
`directive_version`; `audit_spec_target` stays `"agentic-audit-spec-v3.1"`. Nothing is
removed or renumbered in either text. Package ceremony (companions, MANIFEST hashes,
README, AGENTS.md item-4 literal, CITATION.cff, CHANGELOG 1.5.0, DECISIONS.md statuses)
ships in the same revision — the step-2 gates (content-hash binding, AGENTS literal
check) force the atomicity.

## Does not decide

- **Does not ship P-011** (profile JSON Schema): queued post-cut as a package patch
  authored against v1.6, per `DECISIONS.md` D-011.
- **Does not add a directive-side decision-ledger field.** D-012's queued scope was the
  audit-spec evidence target only; Phase D's governance discovery and the audit's §11.10
  note suffice. A `governance.decision_ledger` profile field is a separate, currently
  unqueued decision.
- **Does not prescribe an id format for audited projects' ledgers or cycles** beyond the
  two admissible disciplines; project-internal ledger ids are the project's own.
- **Does not import the package's `CONTRIBUTING.md` lane names into the spec.** The
  `evidence_lane` enum is self-contained; "GitHub-hosted" was deliberately generalized
  to `host-verifiable` (tool-neutral), with vendor surfaces as prose examples only.

## Carve-outs

1. **Machine fields are exempt from vocabulary containment.** Taxonomy values stay legal
   inside JSON/YAML schema fields — including the directive's own
   `memory_surfaces_detected[].class`, which already emits store classes into profile
   artifacts; the restatement rule governs prose. Without this exemption the package's
   own profile artifacts would violate part (c) of the containment rule.
2. **`claimed-automation-absent` never fires on honest manual rules.** A rule documented
   as manual review is §11.11 level-1 material, not a flag; the flag exists for claims
   of automation that nothing implements.
3. **The inversion check ships on sole-source evidence, recorded as such.** Its
   motivating gap was observed in one external repo and not independently re-verified
   here; it shipped because the D-017 drop condition (no operational, tool-neutral
   wording) was tested and not met. If field use shows the §9.9 classes don't decide
   real cases, the revival path is a superseding ADR, not silent reinterpretation.
4. **Alias-drift checks are conditional on profile evidence.** Where a profile records
   no operating-agent baselines (every v1.5 profile), Phase 6 has nothing to confirm and
   flags nothing — keeping v1.5 profiles fully valid under v3.5.
5. **Worked examples are not retro-edited.** The §10 worked mini-example and prior
   appendices keep their original vocabulary and bare ids; they are historical
   illustrations, not live surfaces.

## Consequences

- The failure classes the cross-application surfaced now have named homes: an audit can
  flag a stale enforcement claim, a broken instruction reference, a review-power
  inversion, a silently repointed model alias, an uncorrectable agent memory, an
  unharnessed trap corpus, and an exported taxonomy term — none of which v3.4 could
  name.
- The package now eats its own cooking both ways: the id discipline, negative-self-test
  rule, and decision-ledger target codify what this repo already practices
  (`MANIFEST.md` identifier convention, the drift-linter self-test, `DECISIONS.md`).
- v3.4 audits and v1.5 profiles remain valid; every new field is optional, every new
  enum value additive, and Appendix F makes lazy backfill explicit.
- `DECISIONS.md` D-001..D-010 and D-012 flip to shipped at this cut; D-016 and D-017
  are resolved as recorded above; D-011 (post-cut JSON Schema) and the package-side
  cycle-3 self-audit are the remaining queued work.
- The next self-audit cycle runs under v3.5 and is the first whose ids are born under a
  recorded discipline — and the first that can score this package against the
  enforcement-honesty flags it just adopted.
