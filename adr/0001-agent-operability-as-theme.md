# ADR 0001 — Agent-operability is a strategic-theme lens, not a scored dimension

- **Status:** Accepted — 2026-06-08 (operator-approved; applied via Audit Spec v3.3 / package 1.3.0)
- **Decider:** Jeffrey V. Johnson
- **Source:** self-audit 2026-06-07, finding **F-008** (severity 2, confidence 0.70)
- **Affects:** Agentic Architecture Audit Specification (would ship in **v3.2 → v3.3**, package 1.2.0 → 1.3.0). The Project Profile Discovery Directive is untouched (stays v1.4, consumed unchanged; this theme addition needs no profile-schema change).
- **First ADR in this package** (verified: `adr/` previously absent); it also establishes the §11.10-L3 ADR convention the audit flagged as missing.

## Context

F-008 asks whether the field guide's **eight operating layers** (instructions, settings/config, permissions/sandbox, skills, MCP, subagents/parallelism, hooks/tests, worktrees-CLI-SDK) should become a first-class **scored §11 dimension** measuring "can a 2026 agent navigate and operate this repo."

Three facts shape the decision:

1. **Coverage is already high after v3.2 (F-007).** The eight layers are largely scored today, scattered across existing dimensions: instructions → §11.3 (cross-agent instruction *contract*, added in v3.2) + §11.10; permissions/sandbox/hooks → §11.6 + §11.11; tests → §11.9/§11.11; governance → §11.10. The highest-value slice (instructions-as-contract) was just absorbed in v3.2, so a new dimension's *marginal* coverage is mostly re-scoring.
2. **A new dimension corrupts the min-aggregation rule.** §11 states "the lowest dimensions matter most." A dimension re-scoring the same evidence means one underlying fact (e.g., prose-only permissions) would suppress **two** dimensions — double-penalizing a single fact and distorting the aggregate. This is the decisive structural objection, beyond mere redundancy.
3. **Proportionality.** F-008 is the audit's lowest-confidence finding (0.70). A scored dimension is the highest-cost, least-reversible response available: it renumbers §11, ripples into the §11.12 theme table and the profile schema's `weighting.dimensions` strings, and changes aggregation semantics permanently. A strategic theme is additive/removable without renumbering — the confidence-appropriate instrument.

The contrary pull is real: the self-audit found F-001/F-002/F-003 but had to scatter them across three dimensions, so the operator never saw the coherent story ("this repo isn't agent-operable"). A theme resolves exactly that — it groups and narrates existing dimensions into one operator-legible story **without** adding a re-scored dimension.

**Evidence verified for this ADR (2026-06-07, read-only):**
- No prior ADRs (`adr/` absent) — this is the first.
- Only the wired drift linter (FF-004 / `scripts/check_drift.py`) is implemented. The **proposed AGENTS-presence gate** and **proposed committed-permission-budget gate** exist only as definitions in the gitignored findings file; the permission-budget gate has no automated check, and the AGENTS-presence gate is only *incidentally* enforced via check_drift.py's `@AGENTS.md` resolution.
- `check_drift.py` does **not** validate `§N.N` prose references (its checks are title-agreement, MANIFEST-authority, current-targets, no-conflicting-versions, old-filenames, links/@imports). Yet `MANIFEST.md` states "Steps 1–3 … automated" where Step 3 includes "outdated section numbers." **This is a confirmed manifest/tooling over-claim** — see Consequences.

## Decides

1. **Agent-operability is a strategic-theme lens, not a scored §11 dimension.** It is added to the strategic-theme machinery (§2.3 examples + §11.12 default-mapping) and affects **§10.1 priority weighting only** — it never changes any dimension's 0–3 score. Each underlying fact stays scored exactly once.
2. **One principal-scoped clause is added to §11.6** so that a repo's *committed authority configuration for its own operating agents* (a distinct principal from product-runtime principals) is assessed under Authority where repo-operating agents are in scope.
3. **Developer-agent workflow preference is declared out of scope** (see Carve-outs).
4. **The standalone-dimension alternative (Diff B) is declined** and retained only as the "considered and declined" comparison recorded here.

## Scopes to

The `agent-operability` theme weights, at the §11.12 1.5×-direct level: **§11.3** (cross-agent instruction contract), **§11.6** (authority, incl. the new dev-time clause), **§11.10** (governance), **§11.11** (architectural fitness functions). **§11.8** (policy/prompt separation) is *indirectly* relevant when skill/SOP content carries product, authority, or release policy (recorded as a note beneath the §11.12 row, since that table is direct-relevance-only).

## Does not decide

- **No scalar operability gauge.** A single "operability: N/3" number is available *only* via a standalone dimension, at the orthogonality (min-rule) cost in Context-2. That trade was **considered and declined**; the theme delivers narrative/prioritization coherence, not a headline scalar. A future hard requirement for a single gauge reopens this ADR.
- **Does not implement an operability mandate.** Measurement (a theme) is not enforcement. See Carve-out 3.

## Carve-outs

1. **Workflow preference is out of scope.** Worktree habits, local navigation, IDE affordances, and CLI ergonomics are developer-experience, not architecture, and the audit does not assess them — **unless** an item defines authority, exposes a contract, automates a side effect, or is enforced as a fitness function. The **product's own exposed** CLI/SDK/MCP surfaces remain in scope as contracts/architecture (Phases 3/4); only *developer-agent workflow preference* is excluded. Natural seed for a separate companion "operability checklist" if ever wanted.
2. **Naming / namespacing rules.**
   - **Tool-neutrality:** the theme and §11.6 clause are worded by **capability**, never by vendor path. **Standards may be named** (`AGENTS.md` as an AAIF/Linux-Foundation standard, the way the spec names MCP or OpenAPI); **vendor config may not** (`.claude/settings.json`, `.cursor/rules` appear as *examples only*, never normatively). This reconciles tool-neutrality with v3.2 having named AGENTS.md and stops a future editor from hard-coding `.claude/` paths into the authority text.
   - **ID hygiene:** do **not** cite the bare id `FF-003` for the permission-budget gate — it collides with the published spec's §10 worked-example `FF-003` ("Subagent and protocol-boundary discipline," `audit-spec.md:1556`). Use descriptive names ("the proposed committed-permission-budget gate," "the proposed AGENTS-presence gate") or a namespaced id.
3. **The mandate, if wanted, lives in implemented fitness functions / release gates — not in a default-on theme, and it is not yet built.** "Every repo must be operable" is enforcement, not measurement. It belongs in the proposed AGENTS-presence gate and the proposed committed-permission-budget gate, which are **currently proposed, not implemented** (the permission-budget gate has no automated check). So the mandate "would live there once implemented." A default-on theme is not a mandate (it only weights/narrates; the spec records `strategic_relevance: none` when none is supplied and forbids the agent inventing one — "always-on" must come from the profile or the gate). The theme must never be mistaken for, or promoted to, an enforcement gate.

## Consequences

- **Orthogonality preserved:** each fact scored once; the min-aggregation rule stays meaningful.
- **Reversible & proportional:** a theme is add/removable without renumbering §11, the profile schema, or aggregation semantics — appropriate for a 0.70-confidence finding.
- **Tool-neutral & durable:** the authority text references capabilities, not a volatile vendor landscape.
- **Coherence gained, scalar not:** operators get a grouped, elevated story in priority weighting + the SUMMARY's active-themes section; not a single operability number.
- **Manifest/tooling-drift — registered as finding F-012 (confirmed):** `MANIFEST.md` promises that "Steps 1–3 … [are] automated by `scripts/check_drift.py`," and Step 3 includes "outdated section numbers," but the script implements no `§N.N` check (dimension 11.10/11.11, severity 2, confidence 1.0; raised 2026-06-08 during F-008 Step-0 verification). **Backlog (separate workstream, task chip):** either implement a section-reference check in `check_drift.py`, or reword the MANIFEST to stop promising automated section-number coverage — not part of the v3.3 cut. A dimension-renumber's stale section refs would pass CI silently, an independent reason to prefer the additive theme.
- **Separate workstream (not this cut):** implementing the committed-permission-budget gate as a real pre-commit/CI check is the actual lever for an *enforced* operability mandate; it is repo enforcement, not spec scoring, and is tracked separately.
- **Future risk foreclosed:** a later editor (human or agent) "helpfully promoting" the theme to a dimension would reintroduce the orthogonality corruption. That move requires superseding this ADR.
