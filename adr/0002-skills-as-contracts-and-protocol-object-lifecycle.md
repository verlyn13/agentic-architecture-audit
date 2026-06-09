# ADR 0002 — Agent-skill packages are contracts; protocol objects carry lifecycle status

- **Status:** Accepted — 2026-06-09 (operator-approved; applied via Audit Spec v3.4 / Profile Directive v1.5 / package 1.4.0)
- **Decider:** Jeffrey V. Johnson
- **Source:** standards-currency review, 2026-06-09 — five parallel research sweeps (MCP; inter-agent and instruction standards; observability/evals/provenance; agent security and identity; repo-level operability layers), each verified against primary sources dated through 2026-06-09. The review tested Audit Spec v3.3's claims about the mid-2026 agentic landscape rather than trusting either the spec or model training data.
- **Affects:** both authority texts. Agentic Architecture Audit Specification v3.3 → v3.4 and Project Profile Discovery Directive v1.4 → v1.5 (package 1.3.0 → 1.4.0). All changes additive; no phase removed, no scored dimension added, no renumbering.

## Context

Two structural findings emerged from the currency review; the rest of the spec's design held up (notably: semantic-convention version+stability pinning, the authority matrix, the three-way provenance split, and the v3.2 cross-agent instruction contract — `AGENTS.md` is now foundation-stewarded and the canonical↔bridge model remains the correct, current pattern).

1. **Agent skills became a cross-tool standard with authority semantics.** Since the v3.3 cut, skill packages (`SKILL.md` directories) are specified by an open, multi-vendor standard adopted by dozens of agent clients. The machine-readable surface is no longer prose: required frontmatter fields, an experimental capability pre-approval field (`allowed-tools`), and bundled executable scripts/assets. A skill that pre-approves tools and ships scripts is an authority grant plus an executable payload — and a documented supply-chain risk class now exists for exactly this surface (malicious and over-privileged skills; vendor lockdown/marketplace controls shipped in response). v3.3 classified SKILL.md only as `governance` / `skill-or-sop` prose, so an audit following it verbatim would under-inventory an authority-bearing contract surface.
2. **The spec's protocol-object list was rotting.** v3.3 hard-codes the MCP object list (tools, resources, resource templates, prompts, roots, sampling, elicitation, completion). The protocol has since added first-class tasks, an extensions framework (including server-delivered UI extensions rendered in sandboxed iframes), and registry/discovery metadata — while the next revision (release candidate locked 2026-05-21) **deprecates roots, sampling, and logging** and reworks tasks into an extension. Any fixed object list embedded in the authority text is guaranteed to drift again; worse, a verbatim reading would soon flag the *absence of deprecated objects* as gaps.

A third, smaller cluster (agent identity attestation, delegated commerce, hosted-eval platform churn, isolation-baseline calibration) is evidence-target material that fits existing structures without new machinery.

## Decides

1. **Agent-skill packages are inventoried as contracts and authority surfaces, not only prose governance.** The machine-readable surface — frontmatter contract, capability pre-approvals, bundled executables, source/marketplace provenance — is a Phase 4 contract (audit spec §8.5 `agent-skill` surface, `agent-skill-package` format) and a Phase 6 authority input (§8.7 flags). Prose instructions remain `governance` and are still checked in Phase 8. This mirrors the v3.2 elevation of `AGENTS.md` (cross-agent instruction contract), one layer up the customization stack.
2. **Protocol objects carry a lifecycle status recorded against the pinned protocol revision** (`core | extension | experimental | deprecated | not-protocol-object | unknown`, audit spec §8.5 `protocol_object_status`). Phase 0 already pins protocol revisions per §14; Phase 4 now closes the loop. The spec stops chasing object lists: enumerated objects (tasks, extensions, server-delivered UI, registry/discovery metadata) are *examples of inventoryable objects*, and the lifecycle-status requirement is the durable mechanism that absorbs future protocol churn.
3. **Agent identity and delegated commerce become authority-matrix evidence targets** (audit spec §9.7 rows), not new phases or dimensions. Commerce checks are conditional — they apply only where an agent can initiate or approve payments — and are deliberately protocol-agnostic (verifiable intent mandate, bounded delegation, settlement identity binding) rather than naming a winner in a churning protocol field.
4. **The customization supply chain joins the agent-operability lens** (audit spec §2.3 theme wording, §11.6 note): source pinning, marketplace controls, and lockdown configuration for skills/hooks/plugins/protocol-server configuration consumed by repo-operating agents.
5. **The profile directive mirrors the discovery side additively** (directive §5 schema: `agent_surface.skills`, MCP task/extension/UI/deprecated-objects fields, `commerce` block, committed agent-config and identity-attestation baselines; directive §7 validation rules require search notes when the new fields are unknown).

## Scopes to

Phases 0, 3, 4, 6, 8, and 9 of the audit spec gain inventory items, flags, or exit-check lines; schemas §8.4/§8.5/§8.7/§8.10 gain enum values and one property; matrices §9.1/§9.7 gain rows; §11.3 and the §11.6 note gain wording; §14 anchors are refreshed. The profile directive gains Phase D/E/F discovery items, §5 schema fields, and §7 validation rules. Nothing is removed or renumbered in either text.

## Does not decide

- **No new scored dimension and no rubric-level change.** Per ADR 0001, operability-adjacent evidence reweights and narrates through the theme; each fact is scored once under the existing dimensions. The skills elevation lands as Phase 4/6 inventory feeding existing dimensions (§11.3, §11.6), exactly as the cross-agent instruction contract did in v3.2.
- **No hooks-format or permission-manifest standard is assumed.** The review confirmed lifecycle hooks and committed permission budgets are universal but syntactically per-tool, with no cross-tool standard. The authority texts continue to name capabilities, not formats; a future standard would slot into the same Phase 4/6 structures.
- **No commerce-protocol winner.** Multiple delegated-payment protocols hold neutral governance as of June 2026; the audit lens stays protocol-agnostic.

## Carve-outs

1. **Vendor churn stays out of the authority texts.** The review surfaced significant vendor movement (a major CLI retired and replaced, marketplace lockdown keys, per-tool config layers). Consistent with ADR 0001's naming rule — standards may be named, vendor config may not — none of it is named normatively; vendor paths remain examples only, and none were added to the authority texts in this cut.
2. **`allowed-tools` is named as an example, not a requirement.** The capability pre-approval field is experimental in the skills standard; the spec's wording ("capability pre-approvals such as `allowed-tools`") tracks the capability, not the field name, so a rename in the standard does not invalidate the text.
3. **Deprecated protocol objects are not retro-flagged.** Roots/sampling remain in the spec's enums and examples — they are current at the 2025-11-25 stable revision and historical audits cite them. The `protocol-object-deprecated` flag fires only when a project relies on an object deprecated *at its own pinned revision* without a migration position. Removing the enum values would be a breaking change reserved for a major version.
4. **Regulatory anchors are jurisdiction-neutral.** The §14 anchor for synthetic-content transparency obligations names the obligation class, not a statute; pinning the applicable regulation happens at audit time, per run, in `00-reference-anchors.json`.

## Consequences

- **Future-proofing shifts from list-maintenance to status-recording.** The next protocol revision (already at release-candidate stage) will deprecate objects this spec names; under v3.4 that is absorbed by re-pinning and recording status, not by another authority-text cut. The object list can rot without the audit rotting.
- **Skills get the F-007 treatment before the gap bites.** Projects adopting marketplace skills get inventory, authority, and provenance checks now; the corresponding risk class (malicious/over-privileged skills) has a named home in Phase 4/6 flags instead of falling between `governance` and `tool`.
- **v3.3 audits remain valid; v1.4 profiles need no migration.** All additions are additive; new flags surface as new findings against unchanged rubrics. Migration guidance lives in the audit spec's Appendix E.
- **The directive's internal baseline references stay at v3.1** (e.g., `audit_spec_target: "agentic-audit-spec-v3.1"`), per the established convention that these are schema version-identifiers, not filenames — additively compatible across v3.x cuts.
- **Verification debt is explicit.** The currency review flagged what it could not verify (e.g., final well-known discovery paths, one extension's exact release date); none of those unverified items entered the authority texts. Anchor-pinning at audit time (§14) remains the mechanism that keeps per-run facts current.
