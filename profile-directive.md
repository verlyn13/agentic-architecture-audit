# Project Profile Discovery Directive v1.3

**Version:** v1.3
**Directive date:** 2026-05-23
**Status:** Operator-to-agent instruction document
**Scope:** Project-agnostic and tooling-agnostic
**Lineage:** Supersedes Project Profile Discovery Directive v1.2. Preserves the dated-snapshot model and all v1.2 fields while hardening citation fidelity (the cited excerpt/symbol must actually appear at the cited lines, not merely a valid in-bounds range), requiring lockfile reconciliation for installed versions, and adding cross-field consistency checks (e.g., `access_via` versus the hosted/local authority baseline). These additions are validation clarifications, not schema-field changes, so a v1.2 snapshot needs no field migration to satisfy v1.3. This revision was prompted by a real first-profile run whose Phase-H check passed on path/range bounds yet still shipped two evidence excerpts naming classes that did not exist at the cited lines.

---

## 0. Purpose

Produce a dated, evidence-backed project profile that can be consumed by the Agentic Architecture Audit Specification v3.1.

The profile records what the repository, workspace, governance artifacts, and operator **claim** about the project. The later audit tests those claims against code and runtime evidence.

The profile directive does **not** audit, refactor, score, or remediate. It discovers, cites, records, and routes audit-attention flags.

This directive is project-agnostic and tooling-agnostic. It does not require any particular language, framework, agent platform, repository layout, build system, or hosting model.

---

## 1. Snapshot Model

Profiles are dated snapshots, not living documents.

Each run writes:

```text
profile/<date>/project_profile.yaml
profile/<date>/profile-discovery.md
profile/<date>/profile-diff.md          # when a previous profile exists
profile/<date>/profile-diff.json        # when a previous profile exists
```

The project may also maintain:

```text
profile/cycle-history.md
```

The snapshot date is the operator-selected profile date. If the operator provides a target date, use it exactly and record it. If not, use the current local date.

### 1.1 Dated-snapshot rationale

A profile captures a point-in-time claim set. In active projects, code, governance files, prompts, conventions, and architecture can change between profile discovery, audit execution, and remediation. A dated snapshot preserves reproducibility while profile diffs reveal drift.

### 1.2 Profile mode

Every profile run declares one of:

- `first-profile` — no prior profile exists.
- `refresh` — prior profile exists; run all phases against current evidence and emit a diff.
- `focused-refresh` — prior profile exists and only specific phases need re-running (e.g., a single framework was swapped, only conventions changed). The diff still covers all categories — unchanged categories are recorded as "no changes" rather than omitted.

The mode is recorded in `meta.profile_mode`.

### 1.3 Diff mode

If a previous profile exists, diff mode is mandatory. The agent compares the new profile to the most recent prior profile and emits `profile-diff.md` and `profile-diff.json`.

The diff is consumed by audit Phase 0. It helps decide whether the audit should run as `first-cycle`, `steady-state`, or `focused-diff`.

### 1.4 Cycle history

`profile/cycle-history.md` accumulates operator-ratified conventions established by prior audit/remediation cycles.

It is not a scratchpad and not a source of unreviewed agent memory. It records only conventions, decision patterns, artifact naming rules, branch/PR practices, halt/rescope patterns, ADR template decisions, and other process rules that the operator wants future cycles to inherit.

The audit directive v3.1 may emit `cycle-history-notes.md` proposing additions; the profile directive commits approved entries to `profile/cycle-history.md` here in Phase I, with explicit operator permission.

---

## 2. Prime Directives

1. **Infer before asking.** Read repository, workspace, manifests, governance docs, agent instructions, ADRs, README files, CI, and configuration before asking the operator.
2. **Evidence-first, and citations must be faithful.** Every output field must cite source files and line ranges, be marked `source: operator-interview`, or be marked `source: unknown` with a reason. A path that exists and an in-bounds line range are necessary but not sufficient: when an `evidence` excerpt names a code symbol (class, function, method, constant, config key) or quotes text, that symbol or text must actually appear within the cited lines, and a single-line citation must point at the construct it names — not an adjacent comment, blank line, container, or import. Never paraphrase a symbol you have not confirmed is present. Inventing or approximating a citation is forbidden (§12).
3. **Separate claims from confirmations.** Claimed bounded contexts, ownership, conventions, and architecture are never upgraded to confirmed in this directive.
4. **Snapshot, do not mutate.** Do not modify source code. Write only profile artifacts under `profile/<date>/` and cycle-history additions if explicitly approved.
5. **Ask in batches.** Operator questions are batched once per phase. Avoid ping-pong.
6. **Route audit-attention flags.** Potential findings discovered during profile creation are not findings. Route them to audit phases.
7. **Diff prior snapshots.** If a prior profile exists, produce a diff. Do not treat diff mode as optional.
8. **Record drift honestly.** If repository state contradicts a prior profile, governance claim, or profile evidence, record the drift. Do not silently reconcile.
9. **Use project-neutral categories.** Classify stack and tools by role, not by vendor identity alone.
10. **Boundary declarations apply locally.** Each phase says what the agent must resist while performing that phase.
11. **Protocol surfaces are evidence surfaces.** MCP, A2A, workflow-description, callback, hosted-tool, and remote-agent objects are inventoried by concrete surface type when present.
12. **Authority baselines are matrix-shaped.** Capture approvals, precedence, bypass modes, protected paths, secondary credentials, callback authentication, and hosted/local boundaries when evidence exists.

---

## 3. Halt and Escalation Conditions

Halt and produce `profile/<date>/halt.md` when:

- Two governance or agent-instruction files give contradictory rules on the same topic.
- The repository has no readable anchors: no README or equivalent, no obvious entrypoint, no manifests, no governance docs, and operator input cannot identify scope.
- Multiple projects appear in one path and the operator has not named which one to profile.
- A manifest declares a framework, runtime, or platform that appears absent from code, while code imports or uses a different undeclared one in a way that changes scope.
- ADRs explicitly supersede each other in a chain the agent cannot linearize.
- Scope includes regions the agent cannot read but that are material to profile claims.
- Existing profile and current repo disagree on root identity, default branch, or target workspace and the operator has not authorized treating this as drift.
- The strategic theme supplied by the operator references a structural concern with no detectable evidence in the repo (e.g., theme is `multi-tenant-isolation` but there is no tenant model anywhere) — confirm with operator before proceeding.
- A protocol surface is visible but its advertised capabilities, authentication model, or scope boundary cannot be safely profiled from readable evidence and the missing information changes audit scope.
- Companion audit-package files conflict on which audit spec or profile directive version is authoritative.

The halt artifact must include: condition, evidence, blocked phase, why the profile cannot proceed, and the single operator question needed to unblock.

---

## 4. Phased Workflow

### Phase A — Repository or Workspace Survey

**Input**

- Repository root or workspace path.
- Operator-provided scope, if any.

**Procedure**

1. Confirm root identity and version-control system.
2. Record current branch, current revision, and default branch if discoverable.
3. Enumerate top-level directories and depth-2 workspace structure where appropriate.
4. Detect workspace declarations, package/workspace manifests, build files, service manifests, infrastructure manifests, deployment manifests, and entrypoint indicators.
5. Count files per top-level unit approximately, excluding known build/cache/vendor/generated directories.
6. Identify candidate deployable units, libraries, services, CLIs, workers, UI apps, mobile/desktop apps, edge functions, MCP or tool servers, A2A or remote-agent services, automation bundles, agent-runtime processes, durable-workflow workers, callback receivers, and public SDK surfaces.
7. Locate previous profiles and cycle history.

**Boundary declarations**

- Do not treat a monorepo as one project if evidence shows distinct products and operator has not scoped it.
- Do not count generated/vendor/build artifacts as project structure.
- Do not ask the operator for information already evident in manifests.

**Output fragments**

- `project.repository`
- `project.deployable_units`
- `scope.include_paths`
- `scope.exclude_paths`
- `meta.previous_profile`
- `meta.repository_revision`

---

### Phase B — Stack and Runtime Fingerprinting

**Input**

- Deployable units from Phase A.

**Procedure**

For each unit, read manifests and classify stack elements by role:

- language;
- runtime;
- package manager;
- build tool;
- test framework;
- UI framework;
- HTTP/RPC framework;
- validation/schema technology;
- ORM or persistence framework;
- queue or workflow framework;
- cache or key-value system;
- object store;
- vector store or retrieval index;
- observability/tracing/logging system;
- model provider SDK;
- agent or automation framework;
- subagent or multi-agent framework;
- tool/resource/prompt protocol (e.g., MCP);
- remote-agent or A2A protocol;
- workflow-description or API-overlay technology;
- durable-execution framework;
- computer-use or browser-use harness;
- infrastructure-as-code;
- deployment target;
- security or policy framework;
- eval framework;
- custom or unknown.

Record version pins. When a lockfile is in scope (e.g., `uv.lock`, `package-lock.json`, `poetry.lock`, `Cargo.lock`, `go.sum`, `pnpm-lock.yaml`), reconcile each declared dependency range to the actual locked/installed version and cite the lockfile line for that version. A manifest range alone (`>=`, `^`, `~`) is an insufficient version fact when a lockfile is present, because the audit reasons about installed reality, not declared intent.

**Boundary declarations**

- Do not require a package manager or framework; absence is a valid profile fact.
- Do not infer runtime from file extension alone if manifests contradict it.
- Do not classify a package as an agent framework merely because it mentions AI; cite call sites or documented role.
- Do not skip lockfiles — they are evidence of actual installed versions.

**Output fragments**

- `stack.languages`
- `stack.runtimes`
- `stack.frameworks`
- `stack.package_managers`
- `stack.build_tools`
- `stack.test_frameworks`

**Evidence required**

- Manifest path and line or pattern for each role assignment.

---

### Phase C — Infrastructure and Persistence Discovery

**Input**

- Stack fingerprint;
- configuration files;
- environment examples;
- deployment files.

**Procedure**

Locate and classify:

- databases;
- caches;
- queues;
- workflow engines / durable execution;
- background, paused, resumable, or callback-mediated execution infrastructure;
- object stores;
- file stores;
- vector indexes and retrieval stores;
- search indexes;
- retrieval pipelines (chunkers, embedders, rerankers, retrieval-policy modules);
- model providers and gateways;
- external APIs;
- identity providers;
- secrets managers;
- device or hardware integrations;
- telemetry backends;
- policy engines;
- computer-use harnesses;
- browser-use harnesses;
- local development infrastructure.

For each infrastructure item, record:

- role;
- owner if evident;
- connection/config path;
- environment variable names when safe to record;
- access restrictions;
- persistence role: `authoritative-durable | derived-durable | cache | index | artifact | request-local-ephemeral | session-state | durable-conversation-state | long-term-memory | retrieval-corpus | retrieval-index | operator-rules-memory | checkpoint-state | ephemeral | unknown`;
- deletion or reset path, when evident;
- evidence.

**Boundary declarations**

- Do not expose secret values.
- Do not infer production infrastructure from local-only examples unless docs say they map to production.
- Do not treat absence of an env example as absence of infrastructure.
- Do not assume an infrastructure component is present because the dependency is installed; verify a use site or a config file.

**Output fragment**

- `infrastructure.*`

**Evidence required**

- Config or manifest evidence for each infrastructure entry, or `source: unknown` with search notes.

---

### Phase D — Conventions, Governance, Rules, and Forbidden Patterns

**Input**

- Governance files;
- agent instruction files;
- docs;
- ADRs;
- contributor guides;
- CI/release configuration.

**Procedure**

Locate and read governance anchors:

- README files;
- contributing guides;
- architecture docs;
- glossaries;
- ADRs;
- agent instruction files (CLAUDE.md, AGENTS.md, SKILL.md, .cursorrules, .windsurfrules);
- code ownership files;
- policy files;
- security docs;
- release docs;
- testing docs;
- CI workflow files;
- existing audit artifacts;
- directive-set companion files (`audit-spec.md`, `companions/kickoff-prompt.md`, `companions/explainer.md`, manifests, examples) when this directory is itself an audit-package workspace.

Extract rules in structured form:

- `required` — must, always, required, shall;
- `forbidden` — must not, never, do not, prohibited;
- `conditional` — when X, do Y;
- `precedence` — file or rule hierarchy;
- `process` — branch, PR, release, review, ADR, halt, or verification practice.

Extract project conventions:

- error-handling idiom;
- naming conventions;
- contract/versioning conventions;
- persistence conventions;
- prompt/policy conventions;
- authority and secrets conventions;
- CI/hook bypass prohibitions;
- type-check or lint practices;
- test/eval conventions;
- ADR supersession conventions;
- ADR template structure (whether it includes "Decides / Scopes to / Does not decide / Carve-outs");
- agent operating rules;
- subagent invocation conventions;
- computer-use and browser-use authority restrictions;
- provenance emission requirements.

Run a contradiction check across rules on the same topic.

**Boundary declarations**

- Do not paraphrase rules; capture verbatim.
- Do not resolve contradictory rules by choosing the newer file unless precedence is documented.
- Do not treat README as authoritative over explicit agent/governance precedence rules.
- Do not convert undocumented operator practices into documented conventions without marking source.
- Do not skip workspace-local rules in favor of root-level ones — both apply to their scopes.

**Output fragments**

- `conventions.*`
- `governance.*`

**Evidence required**

- Every extracted rule cites file and line, unless it comes from operator interview.

---

### Phase E — Agent, Automation, and Prompt Surface Inventory

**Input**

- Stack fingerprint;
- source paths;
- governance hints;
- profile scope.

**Procedure**

Locate model-mediated and automation-mediated surfaces:

- model provider SDK call sites;
- agent framework usage;
- custom model loops;
- tool/action/skill definitions;
- resource definitions;
- resource-template definitions;
- root exposure declarations;
- sampling, elicitation, and completion capability declarations;
- prompt definitions;
- server-exposed prompt definitions;
- prompt files;
- authoring prompt templates;
- subagent definitions, manifests, dispatchers, and A2A receivers;
- A2A Agent Cards, advertised skills, task-state handlers, streaming support, push-notification support, registry discovery, and authentication declarations;
- context-assembly logic (retrieval pipelines, memory assemblers, tool description registries, skill/SOP loaders);
- human-in-the-loop approval calls;
- automation scripts that modify code, infrastructure, data, or governance artifacts;
- MCP or MCP-like servers/clients and their concrete surfaces;
- retrieval/indexing flows;
- memory configuration, durable conversation stores, session state, operator-authored rules/memory, and long-term memory stores;
- guardrails;
- handoffs;
- termination logic;
- durable-execution agent surfaces (workflow handlers that include LLM calls and checkpoint state);
- background-agent triggers (schedule-driven or event-driven, off the user-request path);
- paused, resumable, durable, streaming, and callback-mediated execution paths.

Classify prompt surfaces provisionally and materialize counts by type:

- `runtime-production`;
- `runtime-nonproduction`;
- `authoring-artifact`;
- `documentation-about-prompts`;
- `skill-or-sop`;
- `server-exposed-prompt`;
- `unknown`.

Detect loops where a model, planner, script, or automation output feeds back into another action. Detect execution-mode hints: `sync`, `async`, `streaming`, `long-running`, `scheduled`, `batch`, `background`, `paused-for-approval`, `resumable`, `durable`, and `event-triggered`.

**Boundary declarations**

- Do not assume prompts are runtime prompts.
- Do not dismiss authoring artifacts as irrelevant; route them to audit Phase 8.
- Do not infer tool schema coverage from naming alone.
- Do not treat automation as non-agentic merely because it lacks an LLM.
- Do not silently merge subagent definitions with tool definitions.
- Do not flatten MCP/A2A protocol objects into a single "tool server" line when the concrete surfaces are readable.
- Do not merge session state, durable conversation state, long-term memory, retrieval corpora, retrieval indexes, and operator-authored rules/memory.

**Output fragment**

- `agent_surface.*`
- `automation_surface.*`

**Evidence required**

- Every surface cites at least one file and line or search pattern.

---

### Phase F — Evals, Observability, Authority, Provenance, and Versioning Baselines

**Input**

- All prior phases;
- CI/release files;
- test/eval directories;
- telemetry configuration;
- authority/policy files.

**Procedure**

Discover baselines:

1. **Evals and quality gates** — eval suites, benchmarks, golden datasets, fixtures, model tests, behavior tests, release gates, CI jobs, human rubrics. Distinguish `offline | online | live | calibration` modes. Distinguish CI integration from release-gate enforcement.
2. **Observability** — tracing, metrics, logs, semantic conventions (including OTel GenAI version pinning), audit logs, model telemetry, separate `cost_attribution`, `latency_attribution`, `quality_attribution`.
3. **Authority** — approval gates, approval modes, deny/ask/allow precedence, bypass or auto-approval modes, permission scopes, roles, protected paths, sandbox roots, browser scope, filesystem scope, callback authentication, secondary credential paths, secrets access, write authority, hosted-versus-local boundaries, default agent authority.
4. **Provenance** — runtime/action manifests attached to agent outputs, audit-log entries with tool/source/model/approval/task fields, content credentials or content-provenance positions, build/source attestations or release provenance, custom provenance records.
5. **Versioning** — HTTP/API versioning, schema versioning, workflow-description/overlay versioning, MCP/A2A protocol versioning, semantic-convention version and stability, prompt versioning, tool/action/resource versioning, subagent versioning, policy versioning, dataset/evaluator versioning, public SDK versioning.
6. **Fitness functions** — existing static checks, policy checks, architecture checks, schema diffs, dependency boundaries, prompt scans, eval coverage checks, telemetry linters.

Evidence for absence is allowed when it records the search locations and patterns.

**Boundary declarations**

- Do not claim absence without stating search scope.
- Do not equate unit tests with evals unless behavior-quality criteria are explicit.
- Do not equate documentation with enforcement.
- Do not assume authority from code ownership; cite runtime or policy enforcement.
- Do not assume provenance because token counts are logged — provenance is a structured record of what the agent did.
- Do not treat semantic-convention version as complete without stability status when the evidence exposes it.
- Do not treat one provenance class as evidence for another.

**Output fragments**

- `baselines.evals`
- `baselines.observability`
- `baselines.authority`
- `baselines.provenance`
- `versioning_conventions`
- `governance.existing_fitness_functions`

**Evidence required**

- Presence and absence both need evidence notes.

---

### Phase G — Operator Interview

**Input**

- Fields still unknown;
- contradictions not severe enough to halt;
- candidate strategic themes;
- candidate known debt;
- candidate audit-attention flags.

**Procedure**

Ask one batched question set. Do not ask questions already answered by evidence.

Standard topics (drop those already answered):

1. Primary purpose if README/docs are silent or vague.
2. Claimed bounded contexts, if not evident.
3. Ownership for units or contexts.
4. **Strategic themes** for audit weighting (zero, one, or many — see §5).
5. Custom or override mappings of theme → weighted dimensions, if any.
6. Known structural debt.
7. Structural questions the audit should answer.
8. Undocumented conventions.
9. Scope includes/excludes beyond defaults.
10. Audit cadence preference.
11. Provenance expectations now or in a future state.
12. Default authority model expected for agents.
13. Protocol surfaces or remote-agent capabilities the operator considers in scope when evidence is ambiguous.
14. Background/resumable execution expectations and whether callbacks or push notifications are intended to be trusted.
15. Prior-cycle conventions that should be added to cycle history (only on `refresh` runs).

Record answers verbatim with `source: operator-interview`.

On `refresh` runs, the strategic-theme question is always asked (themes can change between cycles); other questions are asked only if the underlying field changed in the diff.

**Boundary declarations**

- Do not synthesize operator answers.
- Do not ask the operator to confirm every inferred fact; ask only unresolved or decision-bearing questions.
- Do not treat operator-stated bounded contexts as confirmed.
- Do not paraphrase operator interview answers — capture verbatim.

**Output fragment**

- operator-sourced fields in `project_profile.yaml`;
- interview transcript section in `profile-discovery.md`.

---

### Phase H — Profile Assembly and Validation

**Input**

- Phase A–G fragments.

**Procedure**

1. Assemble `profile/<date>/project_profile.yaml` per schema in §5.
2. Validate all required fields per §7.
3. Validate evidence **content**, not just structure: confirm each cited path exists, each line range is in-bounds, and — for every citation whose `evidence` names a symbol or quotes text — that the symbol or text is actually present at the cited line(s). A path/range bounds check alone does not satisfy this step. Record the verification method used and any excerpt/line mismatches found and corrected in `profile-discovery.md`.
4. Ensure no claim is upgraded to confirmed.
5. Ensure contradictions are either halted or explicitly recorded as unresolved audit-attention flags.
6. Produce `profile/<date>/profile-discovery.md` with phase-by-phase narrative.
7. Produce `audit_attention_flags[]` with a target audit phase for each flag.

**Boundary declarations**

- Do not produce final files before validation passes.
- Do not omit ambiguity; route it.
- Do not write audit findings.

**Outputs**

- `profile/<date>/project_profile.yaml`
- `profile/<date>/profile-discovery.md`

**Exit check**

- All validation rules in §7 pass.
- Every unknown required field has a reason.
- Every audit-attention flag has a target audit phase.

---

### Phase I — Profile Diff and Cycle-History Update

**Input**

- Current profile;
- most recent prior profile, if present;
- prior profile diff, if present;
- audit/remediation cycle notes, if present (`audit/<date>/cycle-history-notes.md`);
- operator-approved cycle-history entries, if present.

**Procedure**

If a previous profile exists, compare current profile to it and emit per the schema in §6:

- frameworks added, removed, changed;
- deployable units added, removed, changed;
- infrastructure added, removed, changed;
- conventions added, modified, removed;
- governance files added, removed, changed;
- claimed bounded contexts added, removed, renamed, or status-changed;
- known-debt items added, resolved, carried forward;
- audit-attention flags resolved, added, carried forward;
- code-vs-profile drifts caught during the prior cycle;
- strategic themes added, removed, changed;
- scope changes;
- versioning changes;
- fitness functions added, removed, changed.

For cycle history:

1. Read `profile/cycle-history.md`, if present.
2. Read `audit/<date>/cycle-history-notes.md` from any audit cycle since the last profile run, if present.
3. Append only operator-approved conventions or process rules.
4. Propose, but do not silently append, conventions inferred only from agent behavior — write them to `profile/<date>/cycle-history-proposed-updates.md` for operator review.
5. Mark retired conventions when the operator says they no longer apply.

**Boundary declarations**

- Do not treat profile diff as audit scoring.
- Do not let `cycle-history.md` become a transcript dump.
- Do not append inferred conventions without operator approval.
- Do not hide drift that was resolved; record resolved status.

**Outputs**

- `profile/<date>/profile-diff.md`, if previous profile exists
- `profile/<date>/profile-diff.json`, if previous profile exists
- `profile/<date>/cycle-history-proposed-updates.md`, if applicable
- updated `profile/cycle-history.md`, only with explicit operator permission

**Exit check**

- Diff covers all required categories.
- Resolved and carried-forward items are distinguished.
- Cycle-history additions are operator-approved or clearly marked proposed.

---

## 5. `project_profile.yaml` Schema

This schema is intentionally role-based rather than tool-specific. Projects may add fields but should not remove required fields.

```yaml
# ---------- META ----------
meta:
  profile_version: "1.3"
  generated_at: <ISO-8601 datetime>
  snapshot_date: <YYYY-MM-DD>
  generated_by: <agent identifier>
  directive_version: "project-profile-directive-v1.3"
  audit_spec_target: "agentic-audit-spec-v3.1"
  profile_mode: <first-profile | refresh | focused-refresh>
  previous_profile:
    path: <path or none>
    snapshot_date: <YYYY-MM-DD or none>
  repository_revision:
    vcs: <git | hg | other | none | unknown>
    branch: <string or unknown>
    revision: <string or unknown>
  source_confidence: <high | medium | low>

# ---------- PROJECT ----------
project:
  name: <string>
  kind: <app | service | library | monorepo | platform | automation | data-system | mobile-app | desktop-app | mixed | unknown>
  primary_purpose: |
    <1-3 sentences>
  repository:
    root: <absolute path>
    remote: <url | local-only | unknown>
    default_branch: <string | unknown>
  deployable_units:
    - name: <string>
      path: <relative path>
      kind: <http-service | rpc-service | queue-worker | cli | scheduled-job | batch-job | static-site | mobile-app | desktop-app | library | public-sdk | tool-server | mcp-server | a2a-service | remote-agent-service | callback-receiver | agent-runtime | durable-workflow-worker | edge-function | data-pipeline | other | unknown>
      runtime: <string | unknown>
      entrypoint: <relative path | unknown | n/a>
      evidence:
        - path: <file>
          lines: <range>
          evidence: <short excerpt or pattern>

# ---------- STACK ----------
stack:
  languages:
    - name: <string>
      share: <primary | secondary | supporting | unknown>
      evidence: [{path: <file>, lines: <range>}]
  runtimes:
    - name: <string>
      version: <string | unknown>
      applies_to: [<unit_name>]
      evidence: {path: <file>, lines: <range>}
  frameworks:
    - name: <string>
      version: <string | unknown>
      role: <http-framework | rpc-framework | orm | validation | schema | workflow-description | api-overlay | model-provider-sdk | agent-framework | subagent-framework | automation-framework | queue | workflow | durable-execution | cache | object-store | vector-store | observability | eval-framework | test | build | lint | policy | security | iac | ui-framework | mobile-framework | data-processing | mcp-sdk | mcp-server-sdk | a2a-sdk | remote-agent-protocol | computer-use | browser-use | other>
      applies_to: [<unit_name>]
      evidence: {path: <file>, lines: <range>}
  package_managers: [<string>]
  build_tools: [<string>]
  test_frameworks: [<string>]
  eval_frameworks: [<string>]

# ---------- INFRASTRUCTURE ----------
infrastructure:
  data_stores:
    - name: <string>
      engine_or_type: <string>
      role: <authoritative-durable | derived-durable | cache | index | artifact | request-local-ephemeral | session-state | durable-conversation-state | long-term-memory | retrieval-corpus | retrieval-index | operator-rules-memory | checkpoint-state | ephemeral | unknown>
      connection_config_path: <string | unknown>
      access_rules: [<string>]
      deletion_or_reset_path: <string | unknown>
      owner_hint: <string | unknown>
      evidence: {path: <file>, lines: <range>}
  caches: []
  queues: []
  workflow_engines: []
  durable_execution: []
  background_execution: []
  callback_receivers: []
  object_stores: []
  vector_stores:
    - engine_or_type: <string>
      role: <retrieval-corpus | derived-index | scratch | unknown>
      evidence: {path: <file>, lines: <range>}
  retrieval_pipelines:
    - id: <string>
      stages: [<chunker | embedder | reranker | filter | policy>]
      entry_path: <string>
      evidence: {path: <file>, lines: <range>}
  external_services: []
  model_providers:
    - provider: <string>
      access_via: <direct-sdk | gateway | proxy | hosted-platform | unknown>
      evidence: {path: <file>, lines: <range>}
  secrets_managers: []
  observability_backends: []
  policy_engines: []
  computer_use_harnesses: [<string>]
  browser_use_harnesses: [<string>]
  local_development_infrastructure: []

# ---------- AGENT AND AUTOMATION SURFACE ----------
agent_surface:
  model_call_sites:
    - provider_or_sdk: <string>
      path: <file>
      line: <integer>
      evidence: <short excerpt>
  agent_frameworks:
    - name: <string>
      version: <string | unknown>
      evidence: {path: <file>, lines: <range>}
  tools:
    count: <integer>
    locations: [<path>]
    schemas_defined: <true | false | partial | unknown>
    schema_tech: <json-schema | openapi | protobuf | type-system | validation-library | ad-hoc | absent | mixed | unknown>
    registry_path: <path | none | unknown>
  protocol_surfaces:
    mcp:
      present: <true | false | unknown>
      protocol_version: <string | unknown>
      tools: <integer | unknown>
      resources: <integer | unknown>
      resource_templates: <integer | unknown>
      prompts: <integer | unknown>
      roots_exposed: <true | false | unknown>
      sampling_supported: <true | false | unknown>
      elicitation_supported: <true | false | unknown>
      completion_supported: <true | false | unknown>
      authorization_metadata: <present | absent | partial | unknown>
      evidence: [{path: <file>, lines: <range>}]
    a2a:
      present: <true | false | unknown>
      protocol_version: <string | unknown>
      agent_cards: [<path>]
      advertised_skills: <integer | unknown>
      task_state_contracts: <present | absent | partial | unknown>
      streaming_supported: <true | false | unknown>
      push_notifications_supported: <true | false | unknown>
      registry_discovery: <present | absent | partial | unknown>
      authentication_schemes: [<string>]
      evidence: [{path: <file>, lines: <range>}]
    workflow_contracts:
      api_descriptions: [<path>]
      workflow_descriptions: [<path>]
      overlays: [<path>]
      schema_dialects: [<string>]
  subagents:
    count: <integer>
    locations: [<path>]
    typed_boundaries: <true | false | partial | unknown>
    manifest_path: <path | none | unknown>
  resources:
    count: <integer>
    locations: [<path>]
  prompts:
    count: <integer>
    locations: [<path>]
    surface_types:
      runtime_production: <integer>
      runtime_nonproduction: <integer>
      authoring_artifact: <integer>
      documentation_about_prompts: <integer>
      skill_or_sop: <integer>
      server_exposed_prompt: <integer>
      unknown: <integer>
    templating_tech: <string | none | mixed | unknown>
  context_assembly:
    retrieval_modules: [<path>]
    memory_assemblers: [<path>]
    tool_description_registries: [<path>]
    skill_loaders: [<path>]
  loops_detected:
    - id: <string>
      path: <string>
      termination_hint: <max-iterations | timeout | budget-exhaustion | evaluator-approval | explicit-stop | scheduler-bound | human-approval | none-detected | unknown>
  guardrails_detected: []
  handoffs_detected: []
  memory_surfaces_detected:
    - id: <string>
      class: <request-local-ephemeral | session-state | durable-conversation-state | long-term-memory | retrieval-corpus | retrieval-index | artifact-store | operator-rules-memory | checkpoint-state | unknown>
      location: <path | unknown>
      deletion_or_reset_hint: <string | unknown>
      evidence: {path: <file>, lines: <range>}
  execution_modes_detected:
    - id: <string>
      mode: <sync | async | streaming | long-running | scheduled | batch | background | paused-for-approval | resumable | durable | event-triggered | unknown>
      lifecycle_hint: <string | unknown>
      callback_or_resume_hint: <string | unknown>
      evidence: {path: <file>, lines: <range>}
  background_agents:
    - id: <string>
      trigger: <cron | event | webhook | callback | registry | unknown>
      path: <string>

automation_surface:
  scripts_or_workflows:
    - name: <string>
      path: <string>
      can_modify: <code | data | infra | governance | artifacts | unknown | none>
      approval_hint: <string | unknown>
      evidence: {path: <file>, lines: <range>}

# ---------- CONVENTIONS ----------
conventions:
  rules:
    - classification: <required | forbidden | conditional | precedence | process>
      text: <string>
      topic: <error-handling | persistence | git-hooks | schema | protocol-surface | prompt-policy | auth | approval | testing | naming | telemetry | provenance | evals | adr | release | secrets | branching | agent-behavior | subagent-policy | companion-docs | other>
      source:
        type: <file | operator-interview | unknown>
        path: <file | null>
        lines: <range | null>
  result_or_error_pattern:
    in_use: <true | false | mixed | unknown>
    access_field: <value | data | ok | result | n/a | other | unknown>
    base_type: <string | n/a | unknown>
    evidence: {path: <file>, lines: <range>}
  error_handling_style: <result | exceptions | mixed | n/a | unknown>
  git_hooks_policy: <enforced-no-bypass | warn-only | none | unknown>
  type_check_policy: <per-function | per-file | per-module | ci-only | none | unknown>
  documented_language_style_guide: <path | none | unknown>

# ---------- GOVERNANCE ----------
governance:
  readme_paths: [<path>]
  contributing_paths: [<path>]
  architecture_docs: [<path>]
  glossary_paths: [<path>]
  security_docs: [<path>]
  release_docs: [<path>]
  adr:
    directories: [<path>]
    count: <integer>
    naming_convention: <numbered | dated | mixed | none | unknown>
    supersession_chain_clean: <true | false | unknown>
    template_includes_does_not_decide: <true | false | unknown>
  agent_instruction_files: [<path>]
  skill_md_files: [<path>]
  ci_workflows: [<path>]
  existing_fitness_functions:
    - name: <string>
      enforcement_category: <dependency-boundary | schema-diff | static-analysis | policy-as-code | prompt-scan | authority-manifest | telemetry-lint | eval-coverage | adr-template | release-gate | custom | unknown>
      config: <path | unknown>
  existing_audit_artifacts:
    - path: <path>
      role: <input-context | prior-audit | remediation-record | unknown>
  companion_artifacts:
    - path: <path>
      role: <authority-spec | profile-directive | kickoff-prompt | friendly-explainer | manifest | example | schema | other>
      targets_spec_version: <string | unknown | n/a>
      drift_status: <aligned | drift-suspected | unknown>
  cycle_history_path: <path | none>

# ---------- CLAIMED STRUCTURE ----------
claimed_bounded_contexts:
  - name: <string>
    directory_hints: [<path>]
    owner: <string | unknown>
    source:
      type: <docs | operator-interview | inferred-from-folder-name | registry | unknown>
      path: <file | null>
      lines: <range | null>
    status: claimed

claimed_ownership:
  - unit_or_context: <string>
    owner: <string | unknown>
    source: <codeowners | docs | operator-interview | inferred | unknown>

# ---------- BASELINES ----------
baselines:
  evals:
    suites_directory: <path | none | unknown>
    suite_count: <integer | unknown>
    modes_present: [<offline | online | live | calibration>]
    golden_datasets_present: <true | false | unknown>
    ci_integrated: <true | false | partial | unknown>
    release_gate: <true | false | partial | unknown>
    scoring_methods: [<string>]
    judge_calibration_present: <true | false | unknown>
    last_known_pass_rate: <number | unknown>
  observability:
    tracing: <otel | vendor-sdk | custom | none | unknown>
    semantic_conventions_used: <full | partial | none | unknown>
    semantic_convention_version: <string | unknown | n/a>
    semantic_convention_stability: <stable | development | experimental | deprecated | mixed | unknown | n/a>
    genai_semconv_used: <full | partial | none | n/a | unknown>
    agent_or_mcp_semconv_used: <full | partial | none | n/a | unknown>
    cost_attribution: <per-feature | per-tenant | per-tool | per-workflow | global | none | unknown>
    latency_attribution: <per-tool | per-model-call | per-workflow | global | none | unknown>
    quality_attribution: <eval-linked | manual | none | unknown>
  authority:
    approval_gates:
      - tool_or_action: <string>
        policy: <human-in-loop | auto-approved | blocked | none-required | unknown>
        approval_mode: <deny | ask | allow | auto-approved | human-in-loop | blocked | none-required | unknown>
        precedence_hint: <string | unknown>
        bypass_modes: [<string>]
        evidence: {path: <file>, lines: <range>}
    protected_paths: [<path pattern>]
    sandbox_roots: [<path pattern>]
    browser_scope: [<domain pattern>]
    filesystem_scope: [<path pattern>]
    callback_authentication: <present | absent | partial | n/a | unknown>
    secondary_credentials: [<string>]
    hosted_or_local_agent_execution: <hosted | local | hybrid | n/a | unknown>
    default_agent_authority: <read-only | read-write | admin | sandboxed | unknown>
  provenance:
    runtime_action_emission: <full | partial | none | unknown>
    content_provenance_position: <implemented | not-applicable | planned | absent | unknown>
    build_source_provenance_position: <implemented | not-applicable | planned | absent | unknown>
    format: <c2pa | slsa | custom | audit-log | none | mixed | unknown>
    evidence: {path: <file>, lines: <range>}

# ---------- VERSIONING ----------
versioning_conventions:
  http_apis: <url-versioned | header-versioned | schema-versioned | unversioned | n/a | unknown>
  schemas: <semver | hash | date | schema-version | none | unknown>
  workflow_contracts: <semver | hash | date | schema-version | none | n/a | unknown>
  protocol_surfaces: <semver | protocol-version | date | none | n/a | unknown>
  semantic_conventions: <version-pinned | unpinned | n/a | unknown>
  prompts: <semver | hash | date | none | n/a | unknown>
  tools: <semver | hash | date | none | n/a | unknown>
  resources: <semver | hash | date | none | n/a | unknown>
  subagents: <semver | hash | date | none | n/a | unknown>
  policies: <semver | hash | date | none | n/a | unknown>
  provenance_records: <semver | hash | date | attestation-version | none | n/a | unknown>
  eval_datasets: <semver | hash | date | none | n/a | unknown>
  public_sdks: <semver | date | none | n/a | unknown>
  evidence: {path: <file>, lines: <range>}

# ---------- SCOPE, STRATEGY, AND DEBT ----------
scope:
  include_paths: [<string>]
  exclude_paths: [<string>]
  focus_question: |
    <operator's specific concern, or "none">
  audit_cadence: <one-off | monthly | quarterly | post-refactor | release-gated | unknown>

strategic_themes:
  - name: <string>
    description: <string>
    weighting:
      dimensions: [<audit dimension reference, e.g., "11.3 Contract discipline">]
      multiplier: <number>
    source: <operator-interview | docs | unknown>
    evidence: {path: <file | null>, lines: <range | null>}
    unchanged_since: <YYYY-MM-DD | first-snapshot>

known_debt:
  - area: <string>
    description: <string>
    raised_at: <ISO-8601 date | unknown>
    source: <docs | operator-interview | prior-audit | unknown>
    status: <open | resolved | carried-forward | unknown>
    resolved_in_cycle: <YYYY-MM-DD | null>

open_questions:
  - <string>

audit_attention_flags:
  - id: <string>
    description: <string>
    evidence: [{path: <file>, lines: <range>}]
    target_audit_phase: <0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10>
    reason: <string>
    raised_at: <YYYY-MM-DD>
    resolved_in_cycle: <YYYY-MM-DD | null>

# ---------- SOURCES ----------
sources_summary:
  files_read: <integer>
  files_grepped: <integer>
  commands_run: [<string>]
  operator_questions_asked: <integer>
  operator_questions_answered: <integer>
  halt_conditions_triggered: <integer>
  limitations: [<string>]
```

### Local model execution and `access_via`

`infrastructure.model_providers[].access_via` must reflect the call mechanism and must agree with `baselines.authority.hosted_or_local_agent_execution`:

- in-process library inference (a model loaded and run inside the process) → `direct-sdk`;
- a local server reached over HTTP (e.g., a localhost model daemon) → `gateway`;
- a managed remote platform → `hosted-platform`;
- a routing/forwarding layer in front of another backend → `proxy`.

Do not tag a locally executed model as `hosted-platform`. If none fit cleanly, use `unknown` with a search note rather than forcing a misleading value.

### Citation-fidelity notes

Evidence is verified by content, not just structure (§7; Phase H step 3). Before emitting a citation, open the cited lines and confirm the named symbol or quoted text is present there. Symbol line numbers drift as files change, so a construct that sat at one line in a prior snapshot may have moved — re-resolve it rather than copying a remembered line. When the value being cited is an installed dependency version, the faithful evidence is the lockfile entry, not a manifest range (Phase B).

### Strategic-themes notes

`strategic_themes` is a list. A project may have zero, one, or many themes. Each theme carries its own weighted-dimension list and multiplier; the audit consumes them to weight Phase 10 prioritization.

If the operator supplies a theme name without a custom weighting, the audit applies the default mapping from §11.12 of `audit-spec.md`. The profile records `weighting.dimensions: []` and `weighting.multiplier: 1.5` to indicate "use default mapping for this theme name."

When the strategic theme changes between cycles, the profile-diff flags it, and the audit may need to re-run prioritization.

---

## 6. Profile Diff Schema

When a previous profile exists, emit both markdown and JSON diff artifacts.

```yaml
profile_diff:
  from_snapshot: <YYYY-MM-DD>
  to_snapshot: <YYYY-MM-DD>
  mode: <full | focused>
  repository_revision:
    from: <string | unknown>
    to: <string | unknown>
  deployable_units:
    added: []
    removed: []
    changed: []
  frameworks:
    added: []
    removed: []
    changed: []
  infrastructure:
    added: []
    removed: []
    changed: []
  conventions:
    added: []
    removed: []
    modified: []
    contradictions_new: []
    contradictions_resolved: []
  governance:
    added: []
    removed: []
    changed: []
  claimed_bounded_contexts:
    added: []
    removed: []
    renamed: []
    status_changed: []
  known_debt:
    added: []
    resolved: []
    carried_forward: []
  audit_attention_flags:
    added: []
    resolved: []
    carried_forward: []
  code_vs_profile_drift:
    caught_in_prior_cycle: []
    resolved: []
    remains: []
  strategic_themes:
    added: []
    removed: []
    changed: []
  scope:
    added_includes: []
    removed_includes: []
    added_excludes: []
    removed_excludes: []
  fitness_functions:
    added: []
    removed: []
    changed: []
  audit_recommendation:
    suggested_mode: <first-cycle | steady-state | focused-diff>
    rationale: <string>
```

`profile-diff.md` should explain the high-signal changes in prose and list all machine-readable changes in tables. Empty categories are recorded as "no changes" rather than omitted.

---

## 7. Validation Rules

Reject the profile and loop back to the relevant phase if:

- Any required field is null or an empty string without `source: unknown` and reason.
- Any file-cited field lacks path and line range.
- Any `evidence` excerpt names a code symbol (class, function, method, constant, config key) that is not present within the cited line range.
- Any single-line citation (e.g., `agent_surface.model_call_sites[].line`) does not point at the construct named in its `evidence` (off-by-N to a comment, import, blank line, or enclosing block counts as a failure).
- A framework or runtime version is cited as a manifest range while a lockfile is in scope and was not consulted for the installed version.
- `infrastructure.model_providers[].access_via` contradicts `baselines.authority.hosted_or_local_agent_execution` (e.g., `hosted-platform` for a model the authority baseline records as locally executed).
- Any framework or stack role lacks evidence.
- Any rule in `conventions.rules[]` lacks source metadata.
- Any `claimed_bounded_contexts[].status` is not `claimed`.
- Contradictory rules exist without halt or explicit unresolved routing.
- Infrastructure access rules are recorded but no initial violation search was performed or limitation recorded.
- `agent_surface.tools.count > 0` and schema status is `unknown` without search notes.
- `agent_surface.protocol_surfaces.mcp.present == true` and concrete MCP surface counts, authorization metadata, or protocol-version fields are all `unknown` without search notes.
- `agent_surface.protocol_surfaces.a2a.present == true` and Agent Cards, advertised skills, task-state contracts, authentication schemes, or protocol-version fields are all `unknown` without search notes.
- `agent_surface.subagents.count > 0` and `typed_boundaries` is `unknown` without search notes.
- `agent_surface.prompts.count > 0` and prompt surface types are all `unknown` without search notes.
- `agent_surface.memory_surfaces_detected` contains durable or long-term classes without owner, deletion/reset, or authority notes.
- `baselines.observability.semantic_conventions_used` is `full` or `partial` but semantic-convention version or stability is `unknown` without search notes.
- `baselines.authority.approval_gates` are present but approval mode, bypass modes, or precedence hints are all `unknown` without search notes.
- `governance.companion_artifacts` contains derived docs targeting a different spec version without an audit-attention flag.
- Previous profile exists and diff artifacts are absent.
- Audit-attention flags exist without target audit phases.
- Operator-interview answers overwrite stronger file evidence without explanation.
- Cycle-history additions are written as accepted without operator approval.
- `strategic_themes` is non-empty but any entry lacks `weighting` or `source`.

---

## 8. `profile-discovery.md` Structure

`profile-discovery.md` must contain:

1. Snapshot metadata.
2. Phase-by-phase summary.
3. Files and directories read.
4. Searches performed and limitations.
5. Operator interview answers, verbatim.
6. Claimed bounded contexts and why they remain claims.
7. Strategic themes and weighting recommendations.
8. Known debt.
9. Audit-attention flags routed to audit phases (table mapping flag → target phase).
10. Drift against prior profile, if any.
11. Protocol-surface, authority-matrix, state/memory, provenance, and semantic-convention baseline notes.
12. Companion-artifact alignment notes when the profile workspace includes the directive set.
13. Validation checklist.
14. Halt history, if any.
15. Cycle-history proposed updates, if any.
16. On `refresh` runs only: a one-paragraph summary of the diff (the full diff lives in `profile-diff.md`).

Item 13's validation checklist must also state the citation-verification method used (path/range bounds vs. content-level symbol/text match) and list any excerpt/line mismatches found and corrected during Phase H.

The final profile-discovery narrative must be concise enough for an audit agent to read before Phase 0, but complete enough that every profile field is traceable.

---

## 9. `cycle-history.md` Structure

When maintained, `profile/cycle-history.md` uses this structure:

```markdown
# Cycle History

## Purpose

Operator-ratified conventions and process decisions that future profile, audit, planning, and remediation cycles should inherit.

## Active conventions

### Branching and PR conventions
- ...

### Commit and verification conventions
- ...

### ADR conventions
- ...

### Halt and rescope conventions
- ...

### Audit/profile artifact conventions
- ...

### Agent caveat conventions
- ...

## Retired conventions

- ...

## Per-cycle log

### <YYYY-MM-DD> cycle
- Adopted: ...
- Retired: ...
- Open question for next cycle: ...
```

Rules:

- Keep only conventions intended to persist.
- Do not paste full chat logs.
- Do not include unreviewed chain-of-thought or agent scratchpad content.
- Prefer short, durable convention statements.
- Reference artifacts by path when relevant.

---

## 10. Relation to Audit Spec v3.1

The profile is mandatory input to audit Phase 0.

Audit Spec v3.1 consumes:

- `scope.include_paths` and `scope.exclude_paths` for audit bounds;
- `claimed_bounded_contexts` as candidate contexts for Phase 2;
- `strategic_themes` for Phase 10 weighting (mandatory consumption);
- `audit_attention_flags` for phase routing;
- `agent_surface.tools`, `agent_surface.subagents`, `agent_surface.prompts`, `agent_surface.context_assembly`, and `automation_surface` for Phases 3, 4, 6, 8, and 9;
- `agent_surface.protocol_surfaces` for Phases 0, 3, 4, 6, 7, 8, and 9;
- `agent_surface.memory_surfaces_detected` and `agent_surface.execution_modes_detected` for Phases 3, 5, 6, 7, and 9;
- `baselines.evals` for Phase 9;
- `baselines.observability` for Phase 7;
- `baselines.authority` and infrastructure access rules for Phase 6;
- `baselines.provenance` for Phase 7 provenance scoring;
- `governance.companion_artifacts` for Phase 0 companion-drift checks;
- `infrastructure.vector_stores` and `infrastructure.retrieval_pipelines` for Phases 5 and 8;
- `infrastructure.durable_execution` for Phase 3 durable surfaces;
- `infrastructure.computer_use_harnesses` and `infrastructure.browser_use_harnesses` for Phase 6 sandbox declarations;
- `known_debt` for Phase 10 prioritization context;
- `profile-diff` for audit mode selection;
- `cycle-history` for inherited process conventions.

The audit must not silently accept any `status: claimed` field. It must confirm, reject, split, merge, or retain each claim with evidence.

---

## 11. Profile-to-Audit Handoff Checklist

Before invoking the audit, the profile agent or operator should confirm:

- `project_profile.yaml` exists and validates against §7.
- `profile-discovery.md` exists.
- `profile-diff.md` and `profile-diff.json` exist if a previous profile exists.
- `audit_attention_flags[]` are routed with target audit phases.
- `claimed_bounded_contexts[]` remain `status: claimed`.
- Protocol surfaces are either inventoried by concrete object type or explicitly absent/unknown with search notes.
- Authority baselines include approval mode, bypass, precedence, and callback/secondary-credential notes where applicable.
- State and memory surfaces distinguish request-local, session, durable conversation, long-term memory, retrieval corpus, retrieval index, artifact, and operator-rules classes where evidence exists.
- Semantic-convention version and stability are recorded when observability conventions are claimed.
- Provenance baselines distinguish runtime/action, content, and build/source classes.
- Scope include/exclude paths are explicit.
- Strategic themes are present or explicitly absent (`strategic_themes: []` is valid).
- Previous cycle conventions are available via `governance.cycle_history_path` or explicitly absent.
- Halt conditions are resolved or the audit is intentionally not started.

---

## 12. Global Boundary Declarations

Per-step boundaries are declared inline at each phase. The following apply globally. The profile agent must not:

- run the audit;
- upgrade claimed structure to confirmed structure;
- recommend refactors or folder moves;
- modify source code;
- invent evidence citations;
- ask the operator questions the repository already answered;
- skip Phase G by fabricating operator answers;
- produce `project_profile.yaml` before validation passes;
- skip Phase I (diff generation) on `refresh` or `focused-refresh` runs;
- ignore prior profiles when present;
- hide code-vs-profile drift;
- append to `profile/cycle-history.md` without operator approval;
- treat vendor-specific tooling as required by this directive;
- flatten MCP, A2A, workflow, callback, hosted-tool, or remote-agent surfaces into a single generic tool category when concrete evidence exists;
- conflate memory/state classes or provenance classes;
- treat companion docs as synchronized without checking target spec version/date when such metadata is present;
- ping-pong the operator with serial single-question rounds; batch all questions per phase;
- omit `strategic_themes` (use `strategic_themes: []` if none).

---

## 13. Versioning

This directive is **v1.3** dated 2026-05-23.

The minor-version bump is justified because the changes are additive relative to v1.0:

- dated snapshot is made explicit;
- diff mode is promoted to required behavior when a prior profile exists;
- `profile_mode`, `source_confidence`, and `repository_revision` blocks added to `meta`;
- cycle history is added with explicit role separation (audit proposes, profile commits);
- audit-attention routing is strengthened with structured flag schema;
- prompt-surface preclassification is added with materialized counts per type;
- strategic themes are generalized to a list with per-theme multipliers;
- `automation_surface` added as sibling to `agent_surface`;
- subagent, computer-use, browser-use, durable-workflow, vector-store, and retrieval-pipeline coverage added;
- provenance baseline added;
- separate `cost_attribution`, `latency_attribution`, `quality_attribution` fields;
- `release_gate` separated from `ci_integrated` for evals;
- ADR template `does_not_decide` field added;
- project/tooling neutrality is clarified.

Additional v1.2 changes relative to v1.1:

- added concrete MCP surface fields for tools, resources, resource templates, prompts, roots, sampling, elicitation, completion, and authorization metadata;
- added A2A Agent Card, advertised skill, task-state, streaming, push-notification, registry-discovery, and authentication fields;
- added workflow-description, API-overlay, schema-dialect, and protocol-version fields;
- added execution-mode discovery for background, paused-for-approval, resumable, durable, callback-mediated, and event-triggered paths;
- expanded authority baselines into approval mode, precedence, bypass modes, protected paths, secondary credentials, callback authentication, hosted/local boundaries, and default authority;
- split memory/state baselines into request-local, session, durable conversation, long-term memory, retrieval corpus, retrieval index, artifact store, operator-rules memory, and checkpoint classes;
- split provenance baselines into runtime/action, content, and build/source positions;
- added semantic-convention version and stability fields;
- added companion-artifact tracking so kickoff prompts and explainers can be checked against authority spec versions.

Additional v1.3 changes relative to v1.2 (all validation clarifications; no schema fields added or removed, so v1.2 snapshots need no field migration):

- citation fidelity is now a validation rule, not just a prime-directive aspiration: an `evidence` excerpt that names a symbol or quotes text must be confirmed present at the cited lines, and single-line citations must point at the named construct;
- Phase H step 3 is upgraded from "validate evidence paths and line ranges" to a content-level check, with the verification method and any corrected mismatches recorded in `profile-discovery.md`;
- lockfile reconciliation is required: when a lockfile is in scope, dependency versions are cited from the locked/installed value, not a manifest range;
- a cross-field consistency rule rejects `model_providers[].access_via` values that contradict the hosted/local authority baseline, and §5 adds guidance for mapping local model execution onto the `access_via` enum.

Breaking schema changes should become v2.0. Additive fields or validation clarifications become v1.x. Wording-only corrections become patch releases.

---

## Appendix A — Migration from v1.0 to v1.x

For projects with a v1.0 profile snapshot on file:

1. Place the v1.0 snapshot at its existing path; do not modify.
2. Run the current v1.x directive; it generates `profile/<date>/` as a new dated snapshot.
3. Phase I treats the v1.0 snapshot as the prior — generates `profile-diff.md` against it.
4. Fields absent in v1.0 (e.g., `meta.profile_mode`, `strategic_themes` as list, `agent_surface.subagents`, `automation_surface`, `baselines.provenance`) appear as additions in the diff.
5. Fields renamed since v1.0 (e.g., `strategic_theme` singular → `strategic_themes` list) are mapped in the diff narrative section.
6. The operator confirms the migration mapping in a Phase G round (one batched question per renamed field).

The diff between v1.0 and current v1.x outputs is itself useful signal — it shows what the older directive missed.

---

## Appendix B — Migration from v1.1 to v1.2

For projects with a v1.1 profile snapshot on file:

1. Preserve the v1.1 snapshot as historical evidence.
2. Run the current directive (v1.3 or later) as a new dated snapshot; do not mutate the prior profile in place.
3. Treat protocol-surface fields, authority-matrix fields, execution-mode fields, semantic-convention stability, and provenance splits as additions in `profile-diff.md`.
4. If the repo has no MCP, A2A, workflow-description, background/resumable, or durable-memory surfaces, record explicit absence with search notes rather than omitting the fields.
5. Route any unknown but visible protocol, authority, or memory surface as an audit-attention flag.

---

## Appendix C — When to use focused profile re-runs

Full re-runs (all phases) are the default. `focused-refresh` is appropriate when:

- A single deployable unit was added; profile only that unit.
- A single framework was swapped (e.g., one ORM for another); re-run Phases B and C only.
- Conventions changed (new agent-instruction file committed); re-run Phase D only.
- Strategic themes shifted; re-run Phase G only and update `strategic_themes` block.

Focused re-runs still emit a full profile (for downstream audit consumption); they reduce only the agent's work, not the artifact surface. The diff still covers all categories — unchanged categories are recorded as "no changes" rather than omitted.
