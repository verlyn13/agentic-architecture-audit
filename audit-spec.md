# Agentic Architecture Audit — Agent Specification v3.1

**Version:** v3.1
**Specification date:** 2026-05-08
**Status:** Operator-to-agent instruction document
**Scope:** Project-agnostic and tooling-agnostic
**Lineage:** Supersedes Agentic Architecture Audit Specification v3.0. Preserves the v3 operating model while adding protocol-aware contract inventory, authority-matrix handling, execution-mode taxonomy, state/provenance separation, semantic-convention stability pinning, and companion-artifact drift controls.

---

## 0. Purpose

Audit a codebase, workspace, platform, or automation system for 2026-level structural alignment.

The audit asks whether the system has clear boundaries among:

1. domain policy and invariants;
2. application orchestration;
3. agent or automation runtime;
4. machine-readable contracts;
5. adapters and external integrations;
6. state, memory, and artifacts;
7. authority, approval, and blast-radius controls;
8. observability, evaluation, and governance.

The audit produces **evidence-backed, machine-verifiable findings** and **candidate fitness functions**. It does not refactor code, reorganize files, silently repair drift, or decide product conventions for the operator.

This specification is intended to work across languages, frameworks, repositories, agent platforms, and hosting environments. Tool names appear only as examples of enforcement categories; they are not requirements.

The audit treats modern protocol objects as first-class architecture, not as vendor trivia. If a repository exposes MCP, A2A, workflow-description, remote-agent, hosted-tool, computer-use, browser-use, or background-agent surfaces, the audit inventories the advertised contracts, lifecycle states, authority model, and provenance behavior separately instead of collapsing them into a generic "tool" or "runtime" bucket.

---

## 1. Operating Model: Directive-as-Handoff

The audit operates as a **directive series**. Each directive moves one decision point forward and produces one or more durable artifacts. Operator decisions are captured in directive text. Agent execution is captured in files under the dated audit directory. The combined record is the audit.

The agent must treat chat as a control plane, not as the audit record. Phase gates, evidence, findings, scoring, and decisions belong in artifacts.

### 1.1 Snapshot model

The audit is anchored to a dated project profile snapshot.

- The profile states what the repository, operator, and governance documents claim at a point in time.
- The audit tests those claims against source evidence.
- The audit also performs a late smoke-test against the current working branch before findings ship.
- When the snapshot and current branch disagree, the disagreement is recorded as drift rather than silently reconciled.

### 1.2 Audit mode

Every audit declares one of:

- `first-cycle` — no prior audit on this project. Establishes conventions, branching, ADR templates, halt-recovery patterns. Highest directive overhead.
- `steady-state` — prior audit exists. Inherits cycle-history conventions; runs all phases against current evidence.
- `focused-diff` — prior audit exists and the profile diff shows narrow change. Runs only phases whose inputs changed materially. Default fallback is `steady-state` if eligibility is unclear.

The mode is recorded in `00-scope.md` and `SUMMARY.md`. The first cycle's overhead amortizes; later cycles consume the previous dated profile, the profile diff, the cycle history, and prior audit findings instead of restating them in directives.

---

## 2. Inputs

### 2.1 Required inputs

1. `profile/<date>/project_profile.yaml` produced by the profile directive.
2. `profile/<date>/profile-discovery.md`.
3. Operator-provided scope confirmation or a clear statement that profile scope is authoritative.
4. Current repository or workspace read access.

### 2.2 Conditional inputs

If present, the audit must also consume:

- `profile/<date>/profile-diff.md` and/or `profile-diff.json`;
- `profile/cycle-history.md`;
- prior audit summaries;
- remediation plans and PR summaries from previous cycles;
- ADRs created or superseded since the last audit;
- operator-specified strategic themes for prioritization.

### 2.3 Strategic themes

The operator may provide one or more strategic themes that change priority weighting in Phase 10. Themes are project-agnostic strings; common examples include:

- `sdk-extraction` — preparing for licensing, white-label, or public SDK release.
- `multi-tenant-isolation` — adding tenant boundaries to an existing system.
- `regulatory-readiness` — preparing for SOC 2, HIPAA, FedRAMP, or similar.
- `agent-safety-hardening` — tightening authority, approval gates, and provenance.
- `eval-coverage` — closing eval gaps before launch.
- `cost-attribution` — shipping per-tenant or per-feature billing.
- `agent-runtime-consolidation` — reducing tool sprawl and clarifying boundaries.
- `legacy-migration` — migrating off a deprecated framework or pattern.

If a theme is supplied without an explicit dimension mapping, use the default from the table in §11.12. A strategic theme is **not** a finding; it is a weighting signal. The agent must not invent a theme. If none is provided, all findings record `strategic_relevance: none`.

---

## 3. Prime Directives

1. **Evidence-first.** No finding is valid without a citation: file path, line range or glob, evidence excerpt, and the command or read operation that produced it. Unsupported findings are rejected.
2. **Classify before judging.** Use the taxonomy in §6. If a subject resists classification, record `unclassified` with a reason instead of inventing a category.
3. **Claims are not confirmations.** Folder names, manifest names, and governance labels are claims. The audit tests them.
4. **Halt on contradictions.** Do not guess through structural ambiguity. Produce a halt artifact when halt conditions apply.
5. **Scope before depth.** Phase 0 confirms scope and excluded regions. Do not descend into deep analysis before scope is stable.
6. **Audit, do not restructure.** Do not recommend folder moves during discovery phases. Structural moves, renames, and remediation belong to a separate planning directive.
7. **Artifacts are the record.** Each phase produces a named file under `audit/<date>/`. The operator reviews files, not chat summaries.
8. **Read-only by default.** Do not edit source code. The operator may explicitly grant write authority for audit artifacts and, if separately stated, ADR drafts.
9. **Boundary declarations are local.** Each phase states what the agent must resist while performing that phase. Honor phase-local boundaries at the decision point, not only global prohibitions.
10. **Separate current-state findings from future-state safeguards.** A finding describes the present system. A fitness function prevents recurrence. They cross-reference but do not share IDs.
11. **Smoke-test before shipping.** Findings must be rechecked against the current working branch before `SUMMARY.md` is written.
12. **Surface calibrated caveats.** Distinguish substantive deviations from cosmetic deviations and exact matches. Honest caveats are audit signal, not noise.
13. **Protocol surfaces are first-class.** MCP, A2A, workflow-description, callback, hosted-tool, and remote-agent surfaces are classified by their concrete objects and lifecycle states, not only by vendor or package name.
14. **Authority is a matrix.** Approval presence alone is insufficient. Record approval mode, deny/ask/allow precedence where applicable, bypass modes, protected-path behavior, secondary credential acquisition, network/callback authority, and enforcement evidence.
15. **Version-derived companions.** Kickoff prompts, friendly explainers, schemas, examples, and manifests derived from this specification must declare the source spec version/date they target. Inconsistency with this authority spec is documentation drift.

---

## 4. Halt and Recovery

### 4.1 Halt conditions

Stop and produce `audit/<date>/halt.md` when any of these occur:

- Two or more ADRs contradict each other on a structural question material to the audit.
- A directory or manifest claims a bounded context but contains only adapters, only generated artifacts, or only contracts with no domain behavior.
- The same business term has conflicting semantics in two regions both classified as domain or policy-bearing.
- A claimed bounded context has no identifiable authority basis (authoritative store, event source, external authoritative system, or explicit stateless justification).
- The repository exceeds the profile scope and no operator-approved bounds exist.
- Tool, action, or skill definitions exist but no schema, signature, manifest, or authority declaration can be located.
- Runtime prompts contain hard-coded business values that appear nowhere else in policy, configuration, or domain code.
- Agent or automation runtime can perform write actions but approval policy is absent or unclear.
- A protocol surface advertises capabilities, skills, resources, prompts, roots, tasks, callbacks, or remote actions but no matching authorization, scope, schema, or lifecycle declaration can be located.
- Background, paused, resumable, streaming, durable, or long-running execution can cause side effects but lacks an explicit lifecycle contract, resume-state handling, approval path, or callback/webhook authentication model.
- Operator-granted authority is insufficient to read a region the audit depends on.
- Profile evidence and repository evidence contradict in a way that changes scope, stack, governance precedence, or claimed bounded contexts.
- Phase 10.5 smoke-tests reveal that more than one third of findings cite stale evidence — the audit has drifted too far from current development to ship; produce `audit/<date>/halt-stale-evidence.md` and request a fresh profile snapshot.
- The directive package supplied to the audit contains conflicting authority texts (for example, kickoff prompt versus audit spec) and no precedence statement resolves the conflict.

### 4.2 Halt artifact contents

`halt.md` must include:

- halt condition;
- phase where it occurred;
- evidence citations;
- why the contradiction blocks the audit;
- the single operator decision needed to resume;
- downstream phases that are blocked;
- downstream phases that may safely continue, if any.

### 4.3 Halt-recovery state machine

A halted audit may resume only through this sequence:

1. **Halt.** Agent writes (and, if commit authority exists, commits) the halt artifact. Stops downstream phases.
2. **Investigation.** Operator and/or agent gathers missing context. Investigation artifacts are appended to the halt file or written under `audit/<date>/halt-investigation/`.
3. **Rescope.** Agent proposes one or more scoped recovery options (close, rescope, split). Do not rewrite the original finding as if the halt never happened.
4. **Adjudicate.** Operator chooses one option in directive text.
5. **Resume.** Agent continues from the earliest affected phase and records the recovery path in `SUMMARY.md`.

This pattern applies equally when remediation work later triggers a halt (e.g., a Wave 2 PR rescope). Naming the state machine here lets it run the same way at audit time and at remediation time.

---

## 5. Target Architecture Model

This model is a reference for classification and scoring. It is not a mandate to refactor.

### 5.1 Planes

1. **Domain.** Invariants, policies, value objects, domain services, domain events. Pure with respect to transport, persistence, UI, and provider SDKs.
2. **Application.** Use cases and workflows. Coordinates domain, adapters, transactions, authorization checks, idempotency, and side effects.
3. **Agent or automation runtime.** Model calls, tool selection, handoffs, loop control, guardrails, prompt assembly, planner/executor behavior, subagent dispatch, human approval checkpoints, and automation-policy routing.
4. **Contracts.** Machine-readable definitions for externally visible interfaces: HTTP, RPC, events, tools, resources, prompts, config, persisted records, retrieval metadata, plugin or extension manifests, OpenAPI/Arazzo/Overlay-style API and workflow descriptions, MCP tools/resources/resource templates/prompts/roots/sampling/elicitation metadata, A2A Agent Cards/skills/task-state contracts, callback or notification schemas, public SDK surfaces, and provenance manifests for agentic outputs.
5. **Adapters.** Driving and driven integrations: routers, CLIs, workers, UI/API gateways, databases, queues, filesystems, cloud APIs, model providers, external services, device interfaces, retrieval indices, browser-use harnesses, computer-use sandboxes, and durable-workflow workers.
6. **State, memory, and artifacts.** Request-local state, session state, durable conversation state, long-term memory, retrieval corpora, retrieval indexes, generated artifacts, logs, evaluation datasets, checkpoint state, operator-authored persistent rules/memory, and operator decisions.
7. **Authority and governance.** Approval policies, approval-mode precedence, bypass/auto-approval modes, capability scopes, secrets, secondary credential paths, callback/webhook authentication, workspace roots, ADRs, rules, risk controls, access boundaries, and audit trail.
8. **Observability and evaluation.** Traces, logs, metrics, semantic conventions with version/stability status, audit logs, eval suites, golden datasets, regression gates, quality attribution, cost/latency tracking, runtime/action provenance, content provenance, and build/source provenance records.

Authority is cross-cutting. Every tool, adapter, action, agent, subagent, service, and entrypoint declares readable scope, writable scope, callable capabilities, and approval policy.

### 5.2 Alignment principle

The architecture is aligned when the system can answer, with evidence:

- What business terms mean, and where their meanings are authoritative.
- Which context owns each policy, data store, event, and external contract.
- Which runtime entrypoints can cause which side effects.
- Which schemas define external interactions.
- Which prompts carry instructions only and which carry policy.
- Which agent or automation actions require approval.
- Which background, paused, resumable, streaming, durable, or callback-mediated paths can cause side effects and how they resume or complete.
- Which state class a memory-like surface belongs to, who can delete it, and what policy controls retention.
- Which telemetry attributes allow cost, latency, quality, provenance, and failure analysis.
- Which fitness functions prevent known drift from recurring.

---

## 6. Classification Model

### 6.1 Primary categories

Apply in order; first match wins unless the subject is explicitly mixed.

1. Defines business invariants, policies, domain vocabulary, or domain events without framework dependency → `domain`.
2. Orchestrates use cases, transactions, workflows, or policy application across domain and adapters → `application`.
3. Contains model calls, prompts, tool choice, handoffs, guardrails, agent loops, subagent dispatch, planners, or automation runtime policy → `agent-runtime`.
4. Defines schema, IDL, API description, workflow description, overlay, event payload, tool signature, resource manifest, prompt manifest, MCP resource template/root/sampling/elicitation metadata, A2A Agent Card/skill/task contract, config schema, persisted format, public SDK/API shape, callback schema, or provenance manifest → `contracts`.
5. Accepts external calls, messages, user input, CLI input, webhooks, or UI events → `interface`.
6. Calls an external system, provider, device, database, queue, filesystem, model, or cloud service → `adapter`.
7. Provides platform capability with no domain semantics → `infrastructure`.
8. Stores state, memory, cache, index, or generated artifact → `state`.
9. Produces telemetry, audit records, eval records, provenance records, or quality metrics → `observability`.
10. Records decisions, policies-as-code, governance rules, risk controls, fitness functions, or skill/SOP files (SKILL.md, AGENTS.md, CLAUDE.md) → `governance`.
11. Renders or manages user interface behavior → `interface-ui`.
12. Cannot be cleanly classified → `unclassified` with `reason`.

### 6.2 Mixed classification

A module, file, package, or directory is `mixed` when it contains two or more categories whose co-location creates architectural ambiguity or enforcement difficulty.

Examples:

- domain policy plus database calls;
- prompt assembly plus durable writes;
- API route plus business invariant;
- tool definition plus undeclared ambient authority;
- schema plus runtime migration side effects;
- subagent definition plus tool implementation in the same module.

A `mixed` classification requires citations for each mixed concern.

### 6.3 Tie-breakers

- A "service" that orchestrates and performs I/O is `application` — the I/O belongs in an adapter.
- A router that validates business rules is `interface` — the rules belong in `domain` or `application`.
- A subagent definition is `agent-runtime`; the subagent's tool implementations are `adapter` or `application` per their primary work.
- A SKILL.md / AGENTS.md / CLAUDE.md file is `governance`. A prompt template referenced from one is `agent-runtime`.
- Test code is classified by the subject under test, tagged `kind:test`.

### 6.4 Secondary tags

Use as many as apply:

- `bounded-context:<name>`
- `authority:read-only | read-write | admin | privileged | sandboxed | computer-use | browser-use | filesystem-use | hosted-tool | remote-agent | callback-capable | unknown`
- `durability:request-local | session | durable | long-term | derived | cache | index | artifact | checkpoint | unknown`
- `surface:http | rpc | event | queue | tool | resource | resource-template | prompt | root | sampling | elicitation | completion | cli | ui | webhook | callback | file | device | sdk | workflow | a2a | agent-card | task | subagent | other`
- `sync-model:sync | async | streaming | long-running | scheduled | batch | background | paused-for-approval | resumable | durable | event-triggered | unknown`
- `approval-mode:deny | ask | allow | auto-approved | human-in-loop | blocked | none-required | unknown`
- `provenance:runtime-action | content | build-source | unknown`
- `owner:<team-or-person-or-unknown>`
- `criticality:core | supporting | edge | experimental | unknown`
- `lifecycle:stable | experimental | deprecated | legacy | unknown`
- `versioning:semver | date | hash | schema-version | none | unknown`
- `kind:prod | test | fixture | tool | generated | docs | governance`
- `provenance:emits | consumes | passthrough | none`

---

## 7. Phased Workflow

Phases run in order. Each phase has inputs, procedure, boundaries, outputs, and an exit check. The agent must not advance past a failed exit check.

### Phase 0 — Scope, Snapshot, and Orientation

**Inputs**

- `profile/<date>/project_profile.yaml`
- `profile/<date>/profile-discovery.md`
- `profile/<date>/profile-diff.md`, if present
- `profile/cycle-history.md`, if present
- prior `audit/<earlier-date>/SUMMARY.md`, if present
- operator scope statement, if present

**Procedure**

1. Record profile date, audit date, current branch, current revision, and audit mode (`first-cycle`, `steady-state`, or `focused-diff`).
2. Enumerate in-scope units, deployables, workspaces, packages, services, libraries, automation surfaces, and governance artifacts from the profile.
3. Verify that all profile-cited paths still exist; record drift where they do not.
4. Record include and exclude paths.
5. Record strategic themes and affected scoring dimensions, if provided.
6. Pin reference-anchor versions and stability statuses needed for the run (§14), including protocol revisions when MCP, A2A, workflow-description, or semantic telemetry surfaces exist.
7. Check directive-set companion metadata if supplied (`companions/kickoff-prompt.md`, `companions/explainer.md`, manifest, examples). Record drift when companions target a different authority version.
8. Route profile audit-attention flags to Phases 1–10.
9. Identify previous-cycle conventions from cycle history that affect this audit.

**Boundary declarations**

- Do not re-run profile discovery.
- Do not expand scope merely because adjacent code is interesting.
- Do not treat profile claims as audit findings until tested.
- Do not silently discard profile drift; record it.
- Do not treat companion docs as authority over this specification unless the operator explicitly says the audit spec is superseded.

**Outputs**

- `audit/<date>/00-scope.md`
- `audit/<date>/00-scope.json`
- `audit/<date>/00-reference-anchors.json`

**Exit check**

- Scope is bounded and audit mode is recorded.
- Every routed audit-attention flag has a target phase.
- Every profile path missing from the current branch is listed as drift.
- Strategic themes are recorded or explicitly empty.
- Required protocol, semantic-convention, and companion-version anchors are pinned or explicitly marked not applicable.

---

### Phase 1 — Domain Vocabulary Extraction

**Inputs**

- confirmed scope;
- claimed bounded contexts;
- glossaries, ADRs, docs, type names, schema names, events, commands, tools, UI labels, and prompts.

**Procedure**

1. Extract candidate domain nouns, verbs, event names, command names, policy names, state names, and external contract terms.
2. Group terms by unit and claimed context.
3. Identify terms appearing in multiple contexts with distinct definitions.
4. Identify multiple terms used for the same concept.
5. Record cited definitions and usage evidence.

**Boundary declarations**

- Do not infer a definition from a filename alone.
- Do not resolve naming collisions by proposing renames in this phase.
- Do not collapse technical terms into domain terms unless code or docs use them as domain language.

**Outputs**

- `audit/<date>/01-vocabulary.md`
- `audit/<date>/01-vocabulary.json`

**Exit check**

- Every term has at least one citation.
- Every collision candidate has citations for each conflicting use.
- Unsupported terms are removed or marked `unclassified`.

---

### Phase 2 — Bounded Context Mapping

**Inputs**

- vocabulary report;
- claimed bounded contexts;
- state and contract hints from profile.

**Procedure**

For each candidate context, fill a `BoundedContext` record (§8.3) with:

- name;
- status;
- owner;
- ubiquitous language;
- authority basis (authoritative store, event source, external authority, stateless policy, or unknown);
- inbound commands;
- outbound events;
- external dependencies;
- consumed contracts;
- produced contracts;
- known policy responsibilities;
- citations.

Classify status:

- `confirmed` — at least three distinct evidence types support a coherent boundary.
- `candidate` — one or two evidence types support the boundary.
- `claimed-only` — docs or folder names claim it, but code evidence is insufficient.
- `rejected` — claim contradicts evidence.
- `merged` — evidence shows the claim is part of another context (note the merge target).
- `split` — evidence shows the claim contains multiple contexts (note the split set).

Produce a context map showing calls, events, data dependencies, policy dependencies, and shared stores.

**Boundary declarations**

- Do not upgrade `claimed-only` to `confirmed` without three independent evidence types.
- Do not treat shared infrastructure as proof of one bounded context.
- Do not recommend folder moves.
- Do not decide ownership when ownership is absent; record `unknown`.

**Outputs**

- `audit/<date>/02-context-map.md`
- `audit/<date>/02-contexts.json`
- `audit/<date>/02-context-map.mmd`

**Exit check**

- Every claimed bounded context is confirmed, retained as candidate, rejected, merged, or split.
- Every confirmed context has an authority basis.
- No context map edge lacks evidence.

---

### Phase 3 — Runtime Map

**Inputs**

- context map;
- profile deployable units;
- entrypoint hints.

**Procedure**

1. Enumerate entrypoints: HTTP routes, RPC, CLI, UI actions, queue consumers, schedulers, webhooks, callbacks, event handlers, MCP tools, MCP resources, MCP resource templates, MCP prompts, MCP roots exposure, MCP sampling/elicitation/completion paths, A2A receivers, A2A Agent Card discovery paths, agents, subagent invocations, automation loops, durable-workflow handlers, background-agent triggers, batch jobs, device interfaces, and public SDK calls.
2. For each entrypoint, trace the call chain to the first external side effect (DB write, external API, queue publish, filesystem write, LLM call, tool invocation crossing an authority boundary).
3. Mark execution model: `sync | async | streaming | long-running | scheduled | batch | background | paused-for-approval | resumable | durable | event-triggered`.
4. For background, paused, resumable, durable, streaming, or callback-mediated paths, record lifecycle contract, resume state, timeout/retry behavior, notification/callback channel, and completion authority.
5. Identify loops where model, planner, script, or automation output feeds back into further actions. Record termination conditions: max-iterations, explicit stop tool, budget exhaustion, evaluator approval, human approval gate, scheduler bound, or timeout.
6. Identify subagent and remote-agent invocations (one agent calls another). Each invocation crosses an authority boundary; record both sides for Phase 6 consumption and any typed task/state contract for Phase 4.
7. Note human-in-the-loop approval gates and policy gates.

**Boundary declarations**

- Do not assume an entrypoint is harmless because it is internal.
- Do not stop tracing at an abstraction boundary if side effects continue downstream.
- Do not infer termination from good intent; cite explicit stop, iteration cap, timeout, budget, or external scheduler bound.
- Do not collapse subagent calls into "tool calls"; they have separate authority and separate evals.
- Do not treat durable workflow handlers as cron — they have checkpoint state.
- Do not treat a callback or push notification as a passive detail when it can resume work, deliver results, or trigger side effects.

**Outputs**

- `audit/<date>/03-runtime.md`
- `audit/<date>/03-runtime.json`
- `audit/<date>/03-loops/*.mmd`, for the most important loops

**Exit check**

- Every entrypoint has a traced chain or an explicit `trace-blocked` reason.
- Every loop has a termination condition or is flagged.
- Every write-capable runtime path is routed to Phase 6.
- Every subagent invocation has caller and callee authority recorded.
- Every background, paused, resumable, durable, or callback-mediated path has lifecycle evidence or is flagged.

---

### Phase 4 — Contract Inventory

**Inputs**

- runtime map;
- profile contract hints;
- public interfaces and integration surfaces.

**Procedure**

Locate externally visible and internally relied-upon contracts:

- HTTP/RPC API descriptions;
- workflow descriptions and overlays;
- event payload schemas;
- tool/action/skill schemas;
- resource manifests;
- MCP tools, resources, resource templates, prompts, roots exposure, sampling support, elicitation support, completion support, and authorization metadata;
- prompt manifests and parameter schemas;
- configuration schemas;
- database migration contracts and persisted document formats;
- retrieval chunk metadata;
- SDK/API public surface;
- file formats;
- device or hardware protocol definitions;
- A2A Agent Cards, advertised skills, authentication schemes, task-state contracts, streaming capability, push-notification capability, and registry-discovery mechanisms;
- inter-agent message schemas;
- subagent boundary message contracts;
- callback/webhook request and response schemas;
- provenance manifests for runtime/action records, content credentials, and build/source attestations;
- eval dataset schemas;
- policy-as-code input/output schemas.

For each contract, record: name, format, surface, location, versioning strategy, schema dialect if applicable, protocol version if applicable, advertised capabilities, authentication/authorization scheme, producer, consumers, validation mechanism, compatibility policy, citations.

Flag:

- route/action/tool without schema;
- event without payload contract;
- config without validation;
- persisted format without versioning;
- schema drift between producer and consumer;
- duplicate contract names;
- public SDK shape not represented as a contract;
- prompt arguments without schema;
- MCP surface without separately recorded contract object;
- A2A Agent Card or skill without auth/capability/task-state contract;
- workflow description or overlay not tied to the API description it augments;
- callback or push notification without request/response schema and authentication declaration;
- subagent boundary without typed message contract;
- retrieval chunks without typed metadata;
- agentic output without runtime/action provenance manifest;
- generated content without content-provenance position where content authenticity matters;
- release/build output without build/source provenance position where supply-chain integrity matters.

**Boundary declarations**

- Do not equate having schemas with contract discipline unless producer, consumer, validation, and versioning are evident.
- Do not require a particular schema technology.
- Do not treat comments as machine-readable contracts unless the project intentionally uses comment-based IDL generation and cites it.
- Do not flatten MCP or A2A into "tool exists"; their advertised surfaces carry separate contract, authority, and lifecycle implications.

**Outputs**

- `audit/<date>/04-contracts.md`
- `audit/<date>/04-contracts.json`

**Exit check**

- No unflagged ad-hoc external contract remains.
- Every tool/action/skill has a schema reference or is flagged.
- Every MCP or A2A surface has its protocol object inventoried separately or a missing-contract flag.
- Every public interface has producer and consumer evidence or an explicit `consumer-unknown` flag.
- Every subagent boundary has a typed message contract or a flag.

---

### Phase 5 — State and Memory Inventory

**Inputs**

- context map;
- runtime map;
- contract inventory;
- profile infrastructure baseline.

**Procedure**

Classify every store and memory surface:

- `request-local-ephemeral`;
- `session-state`;
- `durable-conversation-state`;
- `long-term-memory`;
- `operator-rules-memory`;
- `authoritative-durable`;
- `derived-durable`;
- `ephemeral-execution`;
- `cache`;
- `index`;
- `artifact`;
- `artifact-store`;
- `prompt-policy-config`;
- `session-memory`;
- `user-memory`;
- `tenant-memory`;
- `agent-scratchpad`;
- `retrieval-corpus`;
- `retrieval-index`;
- `eval-dataset`;
- `audit-log`;
- `checkpoint-state`;
- `unknown`.

For each, record: owner context, retention, deletion or reset path, write authority, read authority, invalidation trigger, lifecycle, sensitivity classification if evident, citations.

**Boundary declarations**

- Do not multi-classify a store without explaining the split.
- Do not treat caches as authoritative without evidence.
- Do not merge human preferences, retrieval indexes, session messages, and agent scratchpads into one generic `memory` bucket.
- Do not merge persistent project rules, operator memory, session state, durable conversations, retrieval corpora, and retrieval indexes into one generic `memory` bucket.
- Do not infer retention from deployment defaults.
- Do not skip retrieval corpora — they are state with retention and authority implications.

**Outputs**

- `audit/<date>/05-state.md`
- `audit/<date>/05-state.json`

**Exit check**

- Every store has an owner or an `owner-unknown` flag.
- Every writable store has write-authority evidence or a missing-authority flag.
- Every memory surface is classified by purpose, durability, owner, and deletion/reset semantics.

---

### Phase 6 — Authority Boundaries

**Inputs**

- runtime map;
- state inventory;
- contract inventory;
- profile authority baseline.

**Procedure**

For each principal — agent, subagent, automation, tool, action, service, adapter, worker, and human approval gate — record:

- readable scopes;
- writable scopes;
- callable tools/actions;
- callable subagents;
- callable external APIs;
- workspace roots;
- browser scope (allowed domains for browser-using agents);
- filesystem scope (allowed paths for filesystem-using or computer-use agents);
- secrets access;
- approval policy;
- approval mode and deny/ask/allow precedence where applicable;
- bypass, auto-approval, or trusted-workspace modes;
- protected-path behavior;
- secondary credential acquisition path;
- outbound network or callback scope;
- callback/webhook authentication and replay protection;
- hosted-versus-local execution boundary;
- token delegation or exchange model;
- sandbox or isolation model;
- escalation paths;
- citations.

Identify:

- capability escalation;
- ambient authority;
- undeclared scope;
- write path without approval policy;
- write path with approval policy but bypass mode enabled or unaccounted for;
- deny/ask/allow precedence unclear;
- approval gate present in code or comments but not connected to enforcement;
- secret access broader than needed;
- secondary credential path broader than the declared principal;
- workspace root broader than declared task;
- tool schema narrower than actual implementation authority;
- computer-use or browser-use surface without sandbox declaration;
- callback or push notification path without authentication model;
- hosted MCP or remote-agent path without token-scope or consent boundary;
- subagent without authority manifest.

**Boundary declarations**

- Do not assume least privilege because a tool name is narrow.
- Do not infer approval policy from comments unless comments are enforced by a policy layer.
- Do not broaden scope to other tools when investigating one authority issue unless the phase requires a full sweep.
- Do not score "approval exists" as sufficient unless bypass modes, protected paths, secondary credentials, and enforcement evidence were checked.

**Outputs**

- `audit/<date>/06-authority.md`
- `audit/<date>/06-authority.json`

**Exit check**

- Every write-capable path has an approval policy value, even if `none-required`.
- Every authority escalation is either explained or flagged.
- Every principal has readable and writable scopes recorded.
- Every browser-use, computer-use, or filesystem-use agent has a declared scope.
- Every callback-capable, hosted-tool, or remote-agent principal has authentication and token-scope evidence or a missing-authority flag.

---

### Phase 7 — Observability Semantics

**Inputs**

- runtime map;
- contracts;
- eval baseline;
- observability baseline.

**Procedure**

Inventory telemetry: span names, event names, metric names, metric units, log fields, trace context propagation, error attributes, model/provider attributes, token/cost/latency/quality attribution, user/tenant/workflow/tool correlation identifiers, audit logs, security events, callback/resume events, and protocol-specific events.

For agentic and model-mediated paths, verify the **cost / latency / quality / provenance** quartet:

- **Cost** — token usage per span, attributable per-feature, per-tenant, per-tool, or per-workflow.
- **Latency** — per agent loop iteration, per tool call, per subagent invocation, per model call.
- **Quality** — eval-result correlation linkable to runtime traces; LLM-as-judge calibration scores recorded where applicable.
- **Provenance** — tools called, retrieval sources used, model + version, prompt version, and subagent path recorded on each agentic output.

Verify semantic-convention alignment (e.g., OTel GenAI, agent, and MCP conventions where applicable) at the version pinned in §14. Record semantic-convention stability status (`stable`, `development`, `experimental`, `deprecated`, or `unknown`) and provider-specific extensions. Lack of conformance to stable conventions is scored separately from partial adoption of conventions still marked development or experimental.

Separate provenance into:

- **Runtime/action provenance** — tools called, resources read, retrieval sources used, model and prompt versions, approval events, subagent path, and task/resume IDs.
- **Content provenance** — content credentials, content-authenticity manifests, or explicit "not applicable" position for generated media/documents.
- **Build/source provenance** — source revision, build inputs, dependency attestations, and release artifact provenance where supply-chain integrity matters.

Flag:

- same event under multiple names;
- same metric under incompatible units;
- units conflicting with the adopted semantic convention;
- missing cost/latency/quality/provenance coverage;
- missing token accounting;
- no trace relationship across model → tool → model loops;
- eval results not linkable to runtime traces;
- agentic outputs without runtime/action provenance;
- generated content without content-provenance position where content authenticity matters;
- build/release artifacts without build/source provenance position where supply-chain integrity matters;
- semantic-convention version recorded without stability status.

**Boundary declarations**

- Do not require a specific observability vendor.
- Do not treat logging as sufficient tracing unless correlation and causality are evident.
- Do not claim convention alignment without checking names, attributes, and units.
- Do not credit token logging as cost attribution — attribution requires per-feature/per-tool dimensions.
- Do not conflate runtime/action provenance with content credentials or build/source attestations.
- Do not penalize missing development-stage semantic conventions the same way as missing stable conventions; record the distinction.

**Outputs**

- `audit/<date>/07-observability.md`
- `audit/<date>/07-observability.json`

**Exit check**

- Naming inconsistencies are flagged.
- Convention alignment is scored with citations.
- Agentic paths have cost/latency/quality/provenance coverage or explicit gaps.
- Semantic-convention version and stability status are recorded when conventions are claimed.

---

### Phase 8 — Policy and Prompt / Context Separation

The unit of analysis is the **assembled context**: prompts plus retrieved chunks plus tool descriptions plus memory plus system instructions plus skills/SOPs. Embedded business policy can hide in any layer.

#### Phase 8.0 — Prompt-surface classification

Before policy analysis, classify each prompt-like surface:

1. `runtime-production-prompt` — executed by production runtime.
2. `runtime-nonproduction-prompt` — executed by dev tools, test harnesses, internal automation, or agent-runtime code that runs locally but not in shipped product.
3. `authoring-artifact-prompt` — template, example, or snippet used by humans while authoring or directing agents; not executed by product runtime.
4. `documentation-about-prompts` — explanatory material, not itself a prompt.
5. `skill-or-sop` — files like SKILL.md, AGENTS.md, CLAUDE.md acting as standing instructions for agents.
6. `server-exposed-prompt` — protocol-advertised prompt exposed by an MCP-like server or remote agent.
7. `not-a-prompt` — false positive.

Each class receives a different treatment in Phase 8.1.

For projects with no runtime LLM surface, Phase 8 still executes — against the runtime non-production, authoring artifact, and skill-or-sop classes — and produces non-vacuous findings. Phase 8 is never silently skipped.

#### Phase 8.1 — Policy separation treatment

- **Runtime production prompts** are checked for embedded product policy, authority policy, compliance rules, thresholds, roles, rates, and undeclared tool behavior.
- **Runtime non-production prompts** are checked for policy that can affect generated code, infrastructure, governance, or release artifacts.
- **Authoring-artifact prompts** are checked for drift from current code, docs, ADRs, operator conventions, and safety boundaries.
- **Documentation about prompts** is checked only for contradictory guidance that could mislead future agents or developers.
- **Skill/SOP files** are checked for embedded policy and for convention-vs-policy confusion (rules expressed here may belong in code).
- **Server-exposed prompts** are checked as both contracts and privileged prompt surfaces: verify parameters, caller eligibility, injection boundaries, and whether untrusted inputs can enter developer/system or other privileged context.

Additionally check:

- **Retrieval-augmented surfaces** — locate retrieval policy (what's retrieved, what's filtered, what's reranked). Check whether retrieval policy encodes business rules that belong in domain code.
- **Tool descriptions** — check whether descriptions encode policy ("only invoke this if amount > $10,000") that belongs in the tool's call site.
- **Untrusted input boundaries** — identify whether user, tool, retrieval, resource, or remote-agent content can enter developer/system messages, privileged prompt context, policy context, or tool descriptions without structured boundary controls.

Prompt and context values to grep and classify include:

- currency amounts;
- numeric thresholds;
- role names;
- time windows;
- quotas;
- rates;
- jurisdiction or compliance assertions;
- approval rules;
- authority grants;
- secrets-handling instructions;
- tool-use constraints;
- test or release pass/fail criteria;
- eval rubrics that gate behavior.

Locate policy artifacts: domain policy code, declarative policy files, configuration, ADRs, governance rules, access-control rules, feature flags, schema constraints, eval rubrics.

Classify each prompt or context surface:

- `pure-instruction`;
- `instruction-with-parameters`;
- `embedded-policy`;
- `policy-masquerade`;
- `retrieval-policy-leak`;
- `tool-description-policy-leak`;
- `server-prompt-policy-leak`;
- `privileged-context-injection-risk`;
- `stale-authoring-artifact`;
- `contradictory-guidance`;
- `unclassified`.

**Boundary declarations**

- Do not mark a non-runtime prompt as vacuously safe.
- Do not classify authoring artifacts using only runtime-prompt criteria.
- Do not recommend policy extraction unless a plausible policy home exists or the finding states that no policy home exists.
- Do not treat templated variables as safe unless the variable source is policy-controlled.
- Do not skip retrieval pipelines because they "aren't prompts."
- Do not treat server-exposed prompts as ordinary docs; they are callable prompt contracts plus runtime context surfaces.

**Outputs**

- `audit/<date>/08-policy.md`
- `audit/<date>/08-policy.json`
- `audit/<date>/08-prompt-surfaces.json`

**Exit check**

- Every prompt-like surface is classified by surface type.
- Every embedded-policy finding cites exact lines and the missing or conflicting policy home.
- Every stale authoring artifact cites the current source it contradicts or states that no source exists.
- Every server-exposed prompt and privileged-context input path is mapped to Phase 4 and Phase 6 or explicitly marked not applicable.

---

### Phase 9 — Evals and Quality Gates

**Inputs**

- agent runtime map;
- contracts;
- prompts;
- tools/actions;
- retrieval surfaces;
- subagent boundaries;
- protocol surfaces;
- async/background lifecycle surfaces;
- observability baseline.

**Procedure**

Locate eval suites, golden datasets, regression fixtures, human-review rubrics, automated scorers, model or prompt comparison records, CI quality gates, release gates, drift tracking, protocol-conformance tests, approval-path tests, async/resume lifecycle tests, safety/security test suites, hardware/sensor/external-system verification suites where relevant.

Classify eval mode for each suite:

- `offline` — golden-data regression. Run pre-merge and on schedule.
- `online` — production sampling with LLM-as-judge or classifier scoring. Run continuously.
- `live` — canary deployments, A/B comparison, shadow mode.
- `calibration` — scoring-method validation (does the LLM judge agree with humans?).

Map each suite to: agent/tool/action/prompt/retrieval-surface/subagent/protocol-surface/lifecycle path under test, pass criteria, scoring method, current pass rate, dataset version, CI integration, release gate status, drift tracking, ownership, citations.

Flag:

- model-mediated or agent-mediated path without eval coverage;
- tool/action with write authority but no safety test;
- prompt without regression fixture;
- eval without golden or reference data;
- eval not run in CI;
- eval in CI but not at release gate;
- evaluator not versioned;
- LLM-as-judge surface without calibration data;
- quality result not linked to observability;
- high-risk behavior requiring only manual review with no rubric;
- retrieval surface uncovered;
- subagent surface uncovered;
- protocol-advertised tool/resource/prompt/skill/task surface uncovered;
- approval or bypass path untested;
- background, paused, resumable, durable, or callback lifecycle untested;
- memory retention or deletion path untested where persistence is material.

**Boundary declarations**

- Do not require LLM judges; classify the scoring method actually used.
- Do not treat unit tests as evals unless they test behavior quality against expected outputs or rubrics.
- Do not assume no eval is required; require an operator or artifact justification.
- Do not credit a single passing eval as coverage.
- Do not treat protocol schema validation as behavior coverage unless the behavior, lifecycle, and authority paths are tested too.

**Outputs**

- `audit/<date>/09-evals.md`
- `audit/<date>/09-evals.json`

**Exit check**

- Every model-mediated or agent-mediated entrypoint maps to an eval suite or a cited `no-eval-required` justification.
- Every write-capable tool/action has some quality, safety, or policy gate identified or flagged.
- Every protocol-advertised remote capability and async/resume path has conformance or lifecycle coverage identified or flagged.
- CI and release-gate integration status are recorded separately.

---

### Phase 10 — Findings, Scoring, and Fitness Functions

**Inputs**

- phase artifacts 0–9;
- routed audit-attention flags;
- strategic themes;
- known debt;
- prior audit results, if any.

**Procedure**

1. Score each dimension using the rubric in §11.
2. Produce structural current-state findings only (`10-findings.*`).
3. Produce future-state fitness-function candidates separately (`10-fitness-functions.*`).
4. Cross-reference findings and fitness functions without sharing IDs (findings use `F-NNN`, fitness functions use `FF-NNN`).
5. Rank findings by priority.
6. Apply strategic-theme weighting where applicable.
7. Classify caveats per §9.6.

#### 10.1 Finding priority

```
priority = severity × confidence × strategic_weight × reversibility_factor
```

Where:

- `severity` — 1–5.
- `confidence` — 0.25–1.0 based on evidence strength.
- `strategic_weight` — 1.0 unless an operator-defined theme applies (default 1.5× for direct relevance, 1.2× for indirect; operator may override).
- `reversibility_factor` — higher when delaying remediation makes later correction harder.

Do not hide low-severity findings if they are strategically relevant.

#### 10.2 Finding vs. fitness function separation

A finding describes a present structural state: current drift, missing contract, ambiguous authority, mixed policy location, unsupported claim, absent eval, telemetry mismatch, missing provenance.

A fitness function describes a future safeguard: static rule, schema diff, contract registry check, dependency boundary check, prompt scan, authority manifest check, telemetry semantic linter, eval coverage check, ADR template validation, release gate.

A finding may reference one or more fitness functions. A fitness function may protect against one or more findings. IDs remain independent.

**Boundary declarations**

- Do not combine a structural finding and a future safeguard into one ID.
- Do not score by severity alone when a strategic theme exists.
- Do not propose a fitness function without naming the enforceable rule and enforcement category.
- Do not write `SUMMARY.md` before Phase 10.5 smoke-test.
- Do not propose a fitness function whose enforcement tech does not exist for the project's stack.

**Outputs**

- `audit/<date>/10-findings.md`
- `audit/<date>/10-findings.json`
- `audit/<date>/10-scores.json`
- `audit/<date>/10-fitness-functions.md`
- `audit/<date>/10-fitness-functions.json`

**Exit check**

- Every score cites evidence from phase artifacts.
- Every finding has source evidence and a confidence level.
- Every fitness function names enforcement category, scope, failure condition, and owner recommendation.
- Findings and fitness functions have separate IDs.

---

### Phase 10.5 — Finding Smoke-Test

This phase exists because audit cycles repeatedly shipped findings whose evidence had drifted between profile snapshot and audit execution, then drifted further between audit shipping and remediation. Smoke-test cost is low; rework cost in remediation is high.

**Inputs**

- draft findings;
- current working branch;
- profile snapshot evidence;
- phase artifacts.

**Procedure**

For each current-state finding:

1. Re-read or re-grep the cited evidence against the current working branch (HEAD).
2. Record the current result.
3. Compare with the snapshot-backed finding.
4. Classify smoke-test outcome:
   - `confirmed-current` — evidence still supports the finding at the cited location with cited semantics.
   - `re-evidenced` — substance still true; citations updated (e.g., line numbers shifted, file renamed).
   - `reclassified` — finding substance changes; severity or category changes.
   - `promoted` — current evidence shows a broader or more serious issue than originally captured.
   - `demoted` — current evidence weakens the issue but does not remove it.
   - `struck` — finding no longer supported; retained in the smoke-test log for audit-trail.
   - `drift-only` — discrepancy between snapshot and current is itself the finding.
   - `not-run` — smoke-test could not be performed (cite reason).
5. Update findings and the smoke-test log.

For each fitness-function candidate:

1. Verify the proposed enforcement tech is currently installed or installable in the project's CI.
2. If a fitness function would be unenforceable, demote to `manual-review-only`.

**Boundary declarations**

- Do not erase the original snapshot evidence.
- Do not silently update line numbers without recording that re-evidencing occurred.
- Do not convert a failed smoke-test into a remediation claim.
- Do not use smoke-test to expand scope beyond the finding unless the outcome is explicitly `promoted` (operator notice required).
- Do not re-derive a finding from scratch; smoke-test verifies, it does not investigate.

**Outputs**

- `audit/<date>/10.5-finding-smoke-test.md`
- `audit/<date>/10.5-finding-smoke-test.json`
- updated `10-findings.*`

**Exit check**

- Every finding has a smoke-test outcome.
- Every struck finding is absent from final priority ranking but retained in the smoke-test log.
- Every drift-only item is recorded as profile/code drift.

If more than one third of findings receive `struck` or `drift-only` outcomes, halt per §4.1 and request a fresh profile snapshot.

---

### Phase 11 — Summary and Cycle-History Notes

**Inputs**

- all phase artifacts;
- smoke-tested findings;
- fitness functions;
- halted/resumed state if any.

**Procedure**

1. Write `SUMMARY.md` last.
2. Produce a one-page operator entry point with: audit mode, profile snapshot date, score table, top findings by priority, active strategic themes and their effects, profile/current-branch drift summary, proposed fitness functions, caveats and halt/resume history, recommended next audit cadence, pointer to detailed phase artifacts.
3. Write `cycle-history-notes.md` containing conventions or process patterns discovered during the audit that the operator should consider adopting into `profile/cycle-history.md` on the next profile run.

**Role separation:** The audit *proposes* additions to cycle history. The profile directive *commits* them, after operator approval. The audit must not edit `profile/cycle-history.md` directly.

**Boundary declarations**

- Do not summarize findings that were struck in Phase 10.5 as active findings.
- Do not hide caveats or halt history.
- Do not add new findings in the summary.
- Do not edit `profile/cycle-history.md` directly.

**Outputs**

- `audit/<date>/SUMMARY.md`
- `audit/<date>/cycle-history-notes.md`

**Exit check**

- Summary references final smoke-tested findings only.
- Operator can trace every top finding to source evidence.
- Cycle-history notes are suggestions, not automatically adopted conventions.

---

## 8. Output Schemas

The audit produces fully valid JSON. Fragments below define the required shape. A project may add fields but must not remove required fields.

### 8.1 Citation

```json
{
  "type": "object",
  "required": ["path", "lines", "evidence", "method"],
  "properties": {
    "path": {"type": "string"},
    "lines": {"type": "string"},
    "evidence": {"type": "string"},
    "method": {"type": "string", "description": "command or read operation that produced this evidence (e.g., 'rg', 'ast-grep', 'view')"},
    "snapshot_ref": {"type": "string", "description": "git revision or profile date the evidence was captured against"},
    "current_ref": {"type": "string", "description": "git revision the evidence was re-validated against in Phase 10.5"}
  }
}
```

### 8.2 VocabularyTerm

```json
{
  "type": "object",
  "required": ["term", "definitions", "collision"],
  "properties": {
    "term": {"type": "string"},
    "definitions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["unit", "definition", "citations"],
        "properties": {
          "unit": {"type": "string"},
          "definition": {"type": "string"},
          "context_hint": {"type": "string"},
          "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
        }
      }
    },
    "collision": {"type": "boolean"},
    "collision_type": {"enum": ["same-term-different-meaning", "different-term-same-meaning", "none"]}
  }
}
```

### 8.3 BoundedContext

```json
{
  "type": "object",
  "required": [
    "name", "status", "owner", "ubiquitous_language", "authority_basis",
    "inbound_commands", "outbound_events", "external_dependencies", "citations"
  ],
  "properties": {
    "name": {"type": "string"},
    "status": {"enum": ["confirmed", "candidate", "claimed-only", "rejected", "merged", "split"]},
    "merge_target": {"type": "string"},
    "split_into": {"type": "array", "items": {"type": "string"}},
    "owner": {"type": "string"},
    "ubiquitous_language": {"type": "array", "items": {"type": "string"}},
    "authority_basis": {
      "type": "array",
      "items": {"enum": ["authoritative-store", "event-source", "external-authority", "stateless-policy", "unknown"]}
    },
    "authoritative_stores": {"type": "array", "items": {"type": "string"}},
    "inbound_commands": {"type": "array", "items": {"type": "string"}},
    "outbound_events": {"type": "array", "items": {"type": "string"}},
    "external_dependencies": {"type": "array", "items": {"type": "string"}},
    "produced_contracts": {"type": "array", "items": {"type": "string"}},
    "consumed_contracts": {"type": "array", "items": {"type": "string"}},
    "subagents_consumed": {"type": "array", "items": {"type": "string"}},
    "subagents_exposed": {"type": "array", "items": {"type": "string"}},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.4 Entrypoint

```json
{
  "type": "object",
  "required": ["id", "kind", "path", "sync_model", "side_effects", "touches_loop", "citations"],
  "properties": {
    "id": {"type": "string"},
    "kind": {"enum": ["http-route", "rpc", "queue-consumer", "cron", "cli", "ui-action", "agent-loop", "subagent-call", "remote-agent-call", "tool", "resource", "resource-template", "root", "sampling", "elicitation", "completion", "prompt", "webhook", "callback", "sdk-call", "batch", "device", "durable-workflow", "background-trigger", "a2a-receiver", "agent-card-discovery", "other"]},
    "path": {"type": "string"},
    "sync_model": {"enum": ["sync", "async", "streaming", "long-running", "scheduled", "batch", "background", "paused-for-approval", "resumable", "durable", "event-triggered", "unknown"]},
    "execution_mode": {"enum": ["sync", "streaming", "background", "paused", "resumable", "durable-workflow", "scheduled", "batch", "event-triggered", "unknown"]},
    "side_effects": {"type": "array"},
    "touches_loop": {"type": "boolean"},
    "termination_condition": {"type": "string"},
    "lifecycle_contract": {"type": "string"},
    "resume_state": {"type": "string"},
    "callback_channel": {"type": "string"},
    "approval_gates": {"type": "array"},
    "checkpoint_state": {"type": "string"},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.5 Contract

```json
{
  "type": "object",
  "required": ["name", "format", "surface", "location", "versioning", "producers", "consumers", "citations"],
  "properties": {
    "name": {"type": "string"},
    "format": {"enum": ["openapi", "arazzo", "overlay", "json-schema", "protobuf", "graphql", "idl", "zod", "pydantic", "typescript", "kotlin", "go-type", "python-type", "rust-type", "mcp-manifest", "a2a-agent-card", "workflow-description", "provenance-attestation", "ad-hoc", "other"]},
    "surface": {"enum": ["http", "rpc", "event", "workflow", "tool", "resource", "resource-template", "root", "sampling", "elicitation", "completion", "prompt", "config", "persisted-format", "retrieval-metadata", "sdk", "file", "device", "policy", "a2a", "agent-card", "skill", "task-state", "subagent", "callback", "provenance-runtime-action", "provenance-content", "provenance-build-source", "other"]},
    "location": {"type": "string"},
    "versioning": {"enum": ["semver", "hash", "date", "schema-version", "none", "unknown"]},
    "schema_dialect": {"type": "string"},
    "protocol_version": {"type": "string"},
    "advertised_capabilities": {"type": "array", "items": {"type": "string"}},
    "auth_scheme": {"type": "string"},
    "producers": {"type": "array", "items": {"type": "string"}},
    "consumers": {"type": "array", "items": {"type": "string"}},
    "validation": {"type": "string"},
    "compatibility_policy": {"type": "string"},
    "flags": {"type": "array", "items": {"enum": ["route-without-spec", "tool-without-schema", "event-without-payload", "config-without-validation", "version-drift", "duplicate-name", "producer-consumer-drift", "sdk-surface-uncontracted", "prompt-args-without-schema", "mcp-surface-uninventoried", "a2a-card-without-auth", "a2a-task-contract-missing", "workflow-overlay-unlinked", "callback-schema-missing", "subagent-boundary-untyped", "retrieval-chunk-untyped", "runtime-provenance-missing", "content-provenance-position-missing", "build-provenance-position-missing", "provenance-missing"]}},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.6 Store

```json
{
  "type": "object",
  "required": ["name", "classification", "owner_context", "retention", "write_authority", "citations"],
  "properties": {
    "name": {"type": "string"},
    "classification": {"enum": ["request-local-ephemeral", "session-state", "durable-conversation-state", "long-term-memory", "operator-rules-memory", "authoritative-durable", "derived-durable", "ephemeral-execution", "cache", "index", "artifact", "artifact-store", "prompt-policy-config", "session-memory", "user-memory", "tenant-memory", "agent-scratchpad", "retrieval-corpus", "retrieval-index", "eval-dataset", "audit-log", "checkpoint-state", "unknown"]},
    "owner_context": {"type": "string"},
    "retention": {"type": "string"},
    "read_authority": {"type": "array", "items": {"type": "string"}},
    "write_authority": {"type": "array", "items": {"type": "string"}},
    "invalidation_trigger": {"type": "string"},
    "deletion_or_reset_path": {"type": "string"},
    "lifecycle": {"type": "string"},
    "sensitivity": {"type": "string"},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.7 Authority

```json
{
  "type": "object",
  "required": ["principal", "readable_scopes", "writable_scopes", "callable_capabilities", "approval_policy", "citations"],
  "properties": {
    "principal": {"type": "string"},
    "readable_scopes": {"type": "array", "items": {"type": "string"}},
    "writable_scopes": {"type": "array", "items": {"type": "string"}},
    "callable_capabilities": {"type": "array", "items": {"type": "string"}},
    "callable_subagents": {"type": "array", "items": {"type": "string"}},
    "callable_externals": {"type": "array", "items": {"type": "string"}},
    "workspace_roots": {"type": "array", "items": {"type": "string"}},
    "browser_scope": {"type": "array", "items": {"type": "string"}},
    "filesystem_scope": {"type": "array", "items": {"type": "string"}},
    "secrets_access": {"type": "array", "items": {"type": "string"}},
    "approval_policy": {"type": "string"},
    "approval_mode": {"enum": ["deny", "ask", "allow", "auto-approved", "human-in-loop", "blocked", "none-required", "unknown"]},
    "approval_precedence": {"type": "string"},
    "bypass_modes": {"type": "array", "items": {"type": "string"}},
    "protected_paths": {"type": "array", "items": {"type": "string"}},
    "secondary_credentials": {"type": "array", "items": {"type": "string"}},
    "outbound_network_scope": {"type": "array", "items": {"type": "string"}},
    "callback_auth": {"type": "string"},
    "hosted_or_local": {"enum": ["hosted", "local", "hybrid", "n/a", "unknown"]},
    "token_delegation": {"type": "string"},
    "sandbox_model": {"type": "string"},
    "flags": {"type": "array", "items": {"enum": ["escalation", "ambient-authority", "undeclared-scope", "write-without-approval-policy", "approval-not-enforced", "bypass-mode-unaccounted", "approval-precedence-unclear", "secret-scope-too-broad", "secondary-credential-too-broad", "workspace-root-too-broad", "callback-auth-missing", "remote-agent-token-scope-unknown", "computer-use-unsandboxed", "subagent-without-policy"]}},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.8 TelemetrySignal

```json
{
  "type": "object",
  "required": ["name", "kind", "producers", "attributes", "citations"],
  "properties": {
    "name": {"type": "string"},
    "kind": {"enum": ["span", "event", "metric", "log", "audit-log", "eval-result"]},
    "producers": {"type": "array", "items": {"type": "string"}},
    "attributes": {"type": "array", "items": {"type": "string"}},
    "unit": {"type": "string"},
    "semantic_convention": {"type": "string"},
    "semantic_convention_version": {"type": "string"},
    "semantic_convention_stability": {"enum": ["stable", "development", "experimental", "deprecated", "unknown"]},
    "provider_extensions": {"type": "array", "items": {"type": "string"}},
    "genai_aligned": {"type": "boolean"},
    "carries_provenance": {"type": "boolean"},
    "provenance_kinds": {"type": "array", "items": {"enum": ["runtime-action", "content", "build-source", "unknown"]}},
    "cost_latency_quality_provenance": {
      "type": "object",
      "properties": {
        "cost": {"type": "boolean"},
        "latency": {"type": "boolean"},
        "quality": {"type": "boolean"},
        "provenance": {"type": "boolean"}
      }
    },
    "flags": {"type": "array", "items": {"enum": ["naming-inconsistent", "attribute-missing", "unit-mismatch", "semantic-stability-unpinned", "no-token-accounting", "no-cost-attribution", "no-quality-attribution", "no-runtime-action-provenance", "no-content-provenance-position", "no-build-source-provenance-position", "no-provenance", "trace-break", "no-eval-correlation"]}},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.9 PromptSurface

```json
{
  "type": "object",
  "required": ["id", "path", "surface_type", "classification", "citations"],
  "properties": {
    "id": {"type": "string"},
    "path": {"type": "string"},
    "surface_type": {"enum": ["runtime-production-prompt", "runtime-nonproduction-prompt", "authoring-artifact-prompt", "documentation-about-prompts", "skill-or-sop", "server-exposed-prompt", "not-a-prompt"]},
    "classification": {"enum": ["pure-instruction", "instruction-with-parameters", "embedded-policy", "policy-masquerade", "retrieval-policy-leak", "tool-description-policy-leak", "server-prompt-policy-leak", "privileged-context-injection-risk", "stale-authoring-artifact", "contradictory-guidance", "unclassified"]},
    "embedded_values": {"type": "array", "items": {"type": "object", "required": ["value", "kind", "line"], "properties": {"value": {"type": "string"}, "kind": {"enum": ["currency", "threshold", "role", "duration", "quota", "rate", "jurisdiction", "approval", "authority", "secret", "tool-constraint", "release-criterion", "eval-rubric"]}, "line": {"type": "integer"}}}},
    "policy_home": {"type": "string"},
    "drift_target": {"type": "string"},
    "privileged_context": {"type": "boolean"},
    "untrusted_input_boundary": {"type": "string"},
    "server_exposed": {"type": "boolean"},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.10 EvalSuite

```json
{
  "type": "object",
  "required": ["name", "covers", "scoring_method", "mode", "ci_integrated", "citations"],
  "properties": {
    "name": {"type": "string"},
    "mode": {"enum": ["offline", "online", "live", "calibration"]},
    "covers": {"type": "array", "items": {"type": "string"}},
    "golden_dataset_path": {"type": "string"},
    "dataset_version": {"type": "string"},
    "scoring_method": {"enum": ["exact-match", "rubric", "llm-judge", "classifier", "statistical", "human-review", "simulation", "hardware-verification", "reference-free", "custom", "unknown"]},
    "current_pass_rate": {"type": "number"},
    "ci_integrated": {"type": "boolean"},
    "release_gate": {"type": "boolean"},
    "drift_tracking": {"type": "boolean"},
    "judge_calibrated": {"type": "boolean"},
    "owner": {"type": "string"},
    "flags": {"type": "array", "items": {"enum": ["no-golden-data", "no-ci", "no-release-gate", "regression-silenced", "model-path-uncovered", "write-tool-untested", "prompt-untested", "unversioned-evaluator", "judge-uncalibrated", "retrieval-surface-uncovered", "subagent-surface-uncovered", "protocol-surface-uncovered", "approval-path-untested", "async-lifecycle-untested", "memory-lifecycle-untested"]}},
    "citations": {"type": "array", "items": {"$ref": "#/$defs/Citation"}}
  }
}
```

### 8.11 Finding

```json
{
  "type": "object",
  "required": ["id", "title", "dimension", "severity", "confidence", "status", "snapshot_evidence", "smoke_test", "recommendation_boundary"],
  "properties": {
    "id": {"type": "string", "pattern": "^F-[0-9]{3}$"},
    "title": {"type": "string"},
    "dimension": {"type": "string"},
    "severity": {"type": "integer", "minimum": 1, "maximum": 5},
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "status": {"enum": ["active", "struck", "drift-only", "superseded"]},
    "strategic_relevance": {"enum": ["direct", "indirect", "none"]},
    "finding_bucket": {"type": "string"},
    "snapshot_evidence": {"type": "array", "items": {"$ref": "#/$defs/Citation"}},
    "current_evidence": {"type": "array", "items": {"$ref": "#/$defs/Citation"}},
    "smoke_test": {"enum": ["confirmed-current", "re-evidenced", "reclassified", "promoted", "demoted", "struck", "drift-only", "not-run"]},
    "related_fitness_functions": {"type": "array", "items": {"type": "string"}},
    "recommendation_boundary": {"type": "string"}
  }
}
```

### 8.12 FitnessFunction

```json
{
  "type": "object",
  "required": ["id", "title", "rule", "enforcement_category", "scope", "failure_condition", "ff_bucket"],
  "properties": {
    "id": {"type": "string", "pattern": "^FF-[0-9]{3}$"},
    "title": {"type": "string"},
    "rule": {"type": "string"},
    "enforcement_category": {"enum": ["dependency-boundary", "schema-diff", "contract-registry", "protocol-contract-registry", "static-analysis", "policy-as-code", "prompt-scan", "authority-manifest", "approval-matrix", "memory-lifecycle-lint", "telemetry-lint", "provenance-attestation", "eval-coverage", "adr-template", "release-gate", "companion-doc-drift", "manual-review-only", "custom"]},
    "scope": {"type": "string"},
    "failure_condition": {"type": "string"},
    "ff_bucket": {"type": "string"},
    "related_findings": {"type": "array", "items": {"type": "string"}},
    "implementation_notes": {"type": "string"}
  }
}
```

`finding_bucket` and `ff_bucket` are independent classifications. A single audit observation may produce one entry in each list with different bucket assignments — the schema makes this orthogonality explicit.

---

## 9. Decision Matrices

### 9.1 Tool vs. Resource vs. Prompt vs. Workflow

| Trait | Classification |
| --- | --- |
| Performs computation or causes side effects | `tool` or `action` |
| Read-only, addressable, returns content without side effects | `resource` |
| Parameterized read-only addressable content in a protocol that supports templates | `resource-template` plus contract check |
| Reusable instruction template consumed by a model or agent | `prompt` |
| Parameterized read-only computation | `tool` unless the protocol explicitly supports parameterized resources |
| Static metadata with no parameters | `resource` |
| Declares allowed filesystem/workspace exposure to a protocol client | `root` plus authority check |
| Requests model assistance from a client or host | `sampling` plus authority and privacy check |
| Requests additional user input through a protocol flow | `elicitation` plus UX and authority check |
| Accepts user/business state and creates model-directed instructions | `prompt` plus policy check |
| Multi-step sequence with durable state, approvals, or retries | `workflow` or `application` path, not only a tool |
| Tool that delegates to model calls | `agent-runtime` plus `tool` surface |
| Advertises a remote agent's identity, skills, auth, and capabilities | `agent-card` contract plus authority check |
| Represents remote-agent task states, push notifications, or streaming lifecycle | `task-state` or `callback` contract plus runtime check |

Flag mismatches.

### 9.2 Agent or automation split justification

| Signal | Score |
| --- | ---: |
| Prompt/instruction set has more than five conditional branches | +1 |
| Capabilities span more than two authority zones | +1 |
| Eval suites differ in failure modes | +1 |
| Model/runtime requirements differ materially (vision vs. reasoning vs. fast vs. on-device) | +1 |
| Memory scopes differ: user, tenant, session, workspace, tool | +1 |
| Workflow has independently failing long-running stages | +1 |
| Tools/actions overlap semantically and confuse selection | +1 |
| Safety or approval policy differs by capability | +1 |
| Context window pressure causes frequent truncation | +1 |
| Subagent invocation would cross a regulatory or trust boundary | +1 |

- 0–1: likely single-agent or single-runtime path is sufficient.
- 2: inspect for clarity but do not recommend split solely on score.
- 3 or more: split or explicit orchestration boundary is justified if supported by evidence.

When split, every subagent boundary requires a typed message contract (Phase 4) and an authority declaration (Phase 6).

### 9.3 Sync vs. async vs. durable boundary

| Trait | Boundary |
| --- | --- |
| User waits and P95 is comfortably under interaction timeout | `sync` |
| User waits and output can be incremental | `streaming` |
| Work exceeds typical request timeout | `async` or `long-running` |
| User does not need immediate result | `async`, `scheduled`, or `batch` |
| Work continues after user-visible response or after the initiating session ends | `background`; lifecycle and provenance required |
| Work stops awaiting explicit human approval or additional user input | `paused-for-approval`; approval state and timeout required |
| Work can be resumed after interruption, host restart, or callback completion | `resumable`; resume token/state contract required |
| Tool calls an agent or automation that can call more tools | `long-running`; termination condition required |
| External device, human approval, or external queue controls completion | `long-running` or `async`; lifecycle contract required |
| State must survive process restart, retry, or migration | `durable`; checkpoint state required |
| External event or registry discovery starts the path | `event-triggered`; trigger contract required |

### 9.4 Embedded policy in prompts and contexts

A value or instruction inside prompt text, retrieval filter logic, tool description, system instruction, or skill/SOP file is embedded policy when any of the following are true:

- It represents a business, compliance, release, authority, pricing, safety, eligibility, or approval rule.
- Changing it would change externally visible behavior.
- It appears only in prompt or context surfaces and not in policy, domain code, configuration, ADRs, or eval rubrics.
- It controls tool choice, write authority, data visibility, or human approval.
- It defines pass/fail criteria for generated artifacts or release decisions.

Recommendation template: extract or reference the rule from a policy-controlled location; pass only the current value or decision result into the prompt; add a test or fitness function that prevents prompt-only policy drift.

### 9.5 Strategic relevance

| Value | Meaning | Default weight |
| --- | --- | ---: |
| `direct` | Finding materially affects an operator-stated strategic theme. | 1.5× |
| `indirect` | Finding affects a dependency or precondition of a strategic theme. | 1.2× |
| `none` | Finding is structurally relevant but not tied to any strategic theme. | 1.0× |

The agent must cite why `direct` or `indirect` applies. If no strategic theme exists, all findings are `none`.

### 9.6 Caveat classification

| Caveat type | Treatment |
| --- | --- |
| `substantive-deviation` | Requires operator awareness and may require rescope or remediation change. |
| `cosmetic-or-framing-deviation` | Record for awareness; does not block if substance matches. |
| `exact-match` | No caveat needed unless explicitly requested by operator. |

Agents are expected to flag deviations. Honest caveats are signal, not noise.

### 9.7 Authority matrix completeness

| Authority facet | Required evidence |
| --- | --- |
| Read scope | paths, resources, records, tenants, domains, or APIs the principal can read |
| Write scope | paths, records, tools, APIs, devices, or external systems the principal can mutate |
| Callable capabilities | tools, actions, subagents, workflows, resources, prompts, or remote agents callable by the principal |
| Approval mode | `deny`, `ask`, `allow`, `auto-approved`, `human-in-loop`, `blocked`, `none-required`, or `unknown` |
| Precedence | whether deny overrides ask/allow, project rules override user rules, or protected paths override broad permissions |
| Bypass modes | any trusted workspace, auto-approve, emergency, CI, test, admin, or hook-bypass behavior |
| Credentials | direct secrets, delegated tokens, secondary credential flows, OAuth scopes, or host-managed credentials |
| Network/callback scope | outbound domains, webhook receivers, push notifications, replay protection, and callback authentication |
| Isolation | sandbox roots, browser/computer-use restrictions, hosted-vs-local boundary, filesystem scope |
| Audit trail | where approval, denial, bypass, credential use, and side effects are recorded |

A principal is not "scoped" merely because some of these fields are documented. Scoring requires enforcement evidence or an explicit gap.

### 9.8 Provenance split

| Provenance class | Evidence target |
| --- | --- |
| `runtime-action` | model, prompt version, tools/resources called, retrieved sources, approvals, subagent path, task/resume IDs, output artifact ID |
| `content` | content credentials, media/document generation manifest, authenticity assertion, or explicit not-applicable position |
| `build-source` | source revision, build inputs, dependency attestations, generated artifact hash, release/signing record |

Do not use one class as evidence for another unless an artifact explicitly links them.

---

## 10. Worked Mini-Example

**Subject:** a TypeScript monorepo with `packages/api`, `packages/agent`, `packages/domain`, `packages/db`, plus a subagent at `packages/agent/subagents/categorizer` and an MCP-like server exposing agent tools.

### Phase 1 finding

```json
{
  "term": "Transaction",
  "definitions": [
    { "unit": "packages/domain", "definition": "A domain event representing a money movement",
      "citations": [{"path":"packages/domain/src/transaction.ts","lines":"12-45","evidence":"export class Transaction { ... }","method":"view"}] },
    { "unit": "packages/db", "definition": "A database transaction scope (BEGIN/COMMIT)",
      "citations": [{"path":"packages/db/src/tx.ts","lines":"3-20","evidence":"export class Transaction { begin() ...","method":"view"}] }
  ],
  "collision": true,
  "collision_type": "same-term-different-meaning"
}
```

### Phase 2 consequence

`db.Transaction` should be renamed (e.g., `DbTxScope`) or namespaced. Recorded as collision finding; no rename performed.

### Phase 3 consequence

The categorizer subagent is invoked at `packages/agent/src/orchestrator.ts:142`. Invocation crosses an authority boundary: main agent has read-write access to user data; subagent is intended to be read-only over a curated chunk. The MCP-like server also exposes `categorize_transaction` as a callable tool. Record both sides, the protocol surface, and the execution mode.

### Phase 4 consequence

The categorizer subagent invocation passes input as `unknown` (no typed message). The MCP-like tool has a name and description but no machine-readable input schema or authorization metadata. Flag `subagent-boundary-untyped`, `tool-without-schema`, and `mcp-surface-uninventoried`. Recommend a typed boundary schema and a protocol-surface registry.

### Phase 5 consequence

The `transactions` table in `packages/db/schema.ts` is the authoritative store for the domain `Transaction`. Classify `authoritative-durable`, `owner_context: billing`. The bounded context's `authority_basis` includes `authoritative-store`.

### Phase 6 consequence

The categorizer subagent has no explicit `readable_scopes`, `approval_mode`, bypass-mode statement, or protocol token-scope declaration. Flag `subagent-without-policy`, `approval-precedence-unclear`, and `remote-agent-token-scope-unknown`. Recommend an authority manifest at `packages/agent/subagents/categorizer/manifest.json`.

### Phase 8 consequence

`packages/agent/prompts/categorize.md:14` reads "Transactions over $10,000 require manager approval." Phase 8.0 classifies the surface as `runtime-production-prompt`. Phase 8.1 classifies as `embedded-policy` (currency + threshold + role in one breath). Recommend extraction to `packages/domain/src/approval-policy.ts` with a unit test.

### Phase 9 consequence

The categorizer subagent and exposed protocol tool have no eval suite. Flag `subagent-surface-uncovered`, `protocol-surface-uncovered`, and `approval-path-untested`. Recommend an offline eval suite + a calibration suite if scoring uses an LLM judge.

### Phase 10 finding (current-state list)

```json
{
  "id": "F-007", "title": "Categorizer subagent and protocol tool boundary is untyped, unauthored, and unevaluated",
  "dimension": "tool-surface-clarity", "severity": 4, "confidence": 0.9,
  "status": "active", "strategic_relevance": "direct",
  "snapshot_evidence": [
    {"path":"packages/agent/src/orchestrator.ts","lines":"142-160","evidence":"invokeCategorizer(...)","method":"view"}
  ],
  "smoke_test": "confirmed-current",
  "related_fitness_functions": ["FF-003"],
  "recommendation_boundary": "Boundary contract + protocol registry + authority manifest + eval suite. Does not require subagent rewrite."
}
```

### Phase 10 fitness function (future-protection list)

```json
{
  "id": "FF-003", "title": "Subagent and protocol-boundary discipline",
  "rule": "Every subagent or protocol-exposed agent boundary must declare a typed message contract, protocol registry entry, authority manifest, and eval suite.",
  "enforcement_category": "protocol-contract-registry",
  "scope": "packages/agent/subagents/*",
  "failure_condition": "missing manifest.json, missing protocol registry entry, missing schema.ts, or missing eval suite for any subagent/protocol-exposed agent capability",
  "ff_bucket": "agent-runtime-discipline",
  "related_findings": ["F-007"]
}
```

### Phase 10.5 smoke-test

Re-grep `packages/agent/prompts/categorize.md:14` against current development. Possible outcomes:

- Line still reads as cited → `confirmed-current`.
- Line moved to line 18 because a header was added → `re-evidenced` (citation updated).
- Prompt was rewritten and threshold removed → `struck` (kept in log; absent from final priority).
- New prompts also embed thresholds → `promoted` (operator notice).
- Prompt was reworded but threshold retained as `>$8000` → `demoted` if scope shrank, or `re-evidenced` if equivalent.

---

## 11. Scoring Rubric

Score each dimension 0–3 with evidence. Aggregate score is informational; the lowest dimensions matter most.

### 11.1 Bounded contexts

- 0: No meaningful context distinctions.
- 1: Names suggest contexts, but vocabulary, stores, or policy ownership collide.
- 2: Distinct vocabulary and mostly distinct authority, with leaks.
- 3: Context boundaries are machine-verifiable and pass fitness functions.

### 11.2 Domain/application separation

- 0: Business rules live primarily in controllers, adapters, prompts, scripts, or UI.
- 1: Domain concepts exist but I/O, framework, or provider dependencies leak in.
- 2: Domain is pure for most contexts; occasional leaks exist.
- 3: Domain purity and dependency direction are enforced.

### 11.3 Contract discipline

- 0: External interfaces are mostly ad hoc.
- 1: Partial schema coverage; producer/consumer or validation unclear.
- 2: Most external interfaces are schema-defined; versioning, compatibility, protocol object separation, or workflow-overlay linkage is inconsistent.
- 3: Interfaces (HTTP, RPC, workflow descriptions, overlays, MCP tools/resources/prompts/roots, A2A Agent Cards/skills/tasks, subagents, callbacks, provenance) are machine-defined, versioned, validated, and diff-gated.

### 11.4 Tool/action surface clarity

- 0: Tools/actions overlap, have vague names, or lack schemas.
- 1: Tools/actions are named with partial schemas but overlap or authority ambiguity exists.
- 2: Tools/actions/resources/prompts/skills are distinct, schema-defined, protocol objects are mostly separated, and overlap is limited.
- 3: Registry includes descriptions, schemas, protocol versions, authority scopes, approval policies, lifecycle modes, and version pins.

### 11.5 State and memory clarity

- 0: Memory/state is conflated or implicit.
- 1: Some stores are identified, but lifecycle, owner, or authority is unclear.
- 2: Stores and memory surfaces are classified with retention, owners, and delete/reset paths for request-local, session, durable conversation, long-term memory, retrieval corpus, retrieval index, artifact, and operator-rules classes.
- 3: Store registry is machine-readable and retention, deletion, invalidation, and authority are enforced by class.

### 11.6 Authority boundaries

- 0: Broad default access; write capabilities not scoped.
- 1: Authority documented informally.
- 2: Per-tool/action/principal authority declared with approval gates for write paths, but bypass/precedence/callback/secondary-credential handling may have gaps.
- 3: Capability-scoped authority is enforced per invocation and audited; approval precedence, bypass modes, secondary credentials, callbacks, hosted/local boundaries, and computer-use/browser-use/filesystem-use sandboxes are verifiable.

### 11.7 Observability semantics

- 0: Logs only or no meaningful telemetry.
- 1: Structured telemetry exists but naming and units are inconsistent.
- 2: Traces/metrics/logs align with chosen conventions for most critical paths; semantic-convention version/stability, provenance class, or eval linkage gaps remain.
- 3: Stable semantic telemetry, cost/latency/quality attribution, runtime/action provenance, relevant content/build provenance positions, and eval-result correlation are enforced.

### 11.8 Policy/prompt separation

- 0: Prompts or instructions carry product, authority, or release policy.
- 1: Some policy extracted, but prompt-only rules remain.
- 2: Runtime and server-exposed prompts are mostly parameterized from policy-controlled sources; authoring artifacts or privileged-context boundaries may drift.
- 3: Prompt surfaces are classified, server-exposed prompts are contracted, untrusted input boundaries are controlled, policy homes are explicit, and drift is fitness-function checked.

### 11.9 Evals and quality gates

- 0: No eval coverage for model/agent/automation paths.
- 1: Ad hoc examples or manual review only.
- 2: Critical paths have evals, golden data or rubrics, and partial CI/release integration.
- 3: Coverage registry, versioned datasets/evaluators, CI and release gates, trace-linked quality results, and LLM-judge calibration.

### 11.10 Governance and audit trail

- 0: Decisions and rules are tribal knowledge.
- 1: Some docs/ADRs exist but precedence and supersession are unclear.
- 2: Governance artifacts are current enough to guide the audit; some drift remains.
- 3: ADRs, conventions, cycle history, and fitness functions are current, explicit, and validated. ADR template includes "Decides / Scopes to / Does not decide / Carve-outs" sections.

### 11.11 Architectural fitness functions

- 0: None.
- 1: Rules documented but not enforced.
- 2: Some automated checks exist.
- 3: Comprehensive CI/release gates cover dependency direction, schemas, protocol-contract registries, authority matrices, memory lifecycle, telemetry, prompts, evals, provenance, companion-doc drift, and governance templates.

### 11.12 Strategic-theme default-mapping

When an operator supplies a theme without an explicit dimension list, apply this default:

| Theme | Weighted dimensions (1.5× direct) |
| --- | --- |
| `sdk-extraction` | 11.3 Contract discipline, 11.4 Tool surface, 11.6 Authority, 11.1 Bounded contexts |
| `multi-tenant-isolation` | 11.6 Authority, 11.5 State, 11.1 Bounded contexts |
| `regulatory-readiness` | 11.6 Authority, 11.7 Observability, 11.9 Evals, 11.3 Contract discipline |
| `agent-safety-hardening` | 11.6 Authority, 11.7 Observability, 11.8 Policy/prompt separation |
| `eval-coverage` | 11.9 Evals, 11.7 Observability, 11.4 Tool surface |
| `cost-attribution` | 11.7 Observability, 11.5 State, 11.3 Contract discipline |
| `agent-runtime-consolidation` | 11.4 Tool surface, 11.1 Bounded contexts, 11.6 Authority |
| `legacy-migration` | 11.1 Bounded contexts, 11.2 Domain/application, 11.3 Contract discipline |

Operators may override; custom themes name their own dimensions.

---

## 12. Priority and Remediation Handoff

The audit may recommend fix order, but remediation planning is a separate directive.

Default fix order:

1. vocabulary and bounded contexts;
2. contracts and schemas;
3. authority boundaries;
4. state and memory boundaries;
5. runtime and orchestration boundaries;
6. policy/prompt separation;
7. observability semantics;
8. evals and quality gates;
9. governance and ADR cleanup;
10. fitness functions to lock in the intended architecture.

The audit must preserve this distinction:

- **Audit:** identifies and scores structural evidence.
- **Planning:** decides PR units, ordering, ADR decisions, split rules, and implementation sequence.
- **Remediation:** changes code or governance artifacts.

---

## 13. Deliverables Manifest

```text
audit/<date>/
  00-scope.md
  00-scope.json
  00-reference-anchors.json
  profile-diff.md                 # only on re-runs (consumed from profile)
  01-vocabulary.md
  01-vocabulary.json
  02-context-map.md
  02-contexts.json
  02-context-map.mmd
  03-runtime.md
  03-runtime.json
  03-loops/*.mmd
  04-contracts.md
  04-contracts.json
  05-state.md
  05-state.json
  06-authority.md
  06-authority.json
  07-observability.md
  07-observability.json
  08-policy.md
  08-policy.json
  08-prompt-surfaces.json
  09-evals.md
  09-evals.json
  10-findings.md
  10-findings.json
  10-scores.json
  10-fitness-functions.md
  10-fitness-functions.json
  10.5-finding-smoke-test.md
  10.5-finding-smoke-test.json
  cycle-history-notes.md
  halt.md                         # only if halted
  halt-stale-evidence.md          # only on Phase 10.5 stale-rate halt
  halt-investigation/             # only if recovery required
  SUMMARY.md
```

`SUMMARY.md` is the operator entry point and contains:

- audit mode and profile snapshot date;
- score table;
- top findings by priority (smoke-tested form);
- active strategic themes and their effects on prioritization;
- profile/current-branch drift summary;
- proposed fitness functions;
- caveats and halt/resume history;
- recommended next audit cadence;
- pointer to detailed phase artifacts.

The agent's final chat message is a one-line pointer to `audit/<date>/SUMMARY.md`. No substitute summary.

---

## 14. Reference Anchors to Version-Pin at Audit Time

The agent must check current official sources when an audit run depends on current versions or semantic conventions. At minimum, version-pin:

- **OpenAPI Specification** for HTTP API descriptions.
- **Arazzo or equivalent workflow-description specification** when workflow contracts exist.
- **Overlay or equivalent API augmentation specification** when overlays exist.
- **JSON Schema** for structured payload validation.
- **Model Context Protocol**, including security, authorization, roots, tools, resources, resource templates, prompts, sampling, elicitation, and completion behavior, if MCP or MCP-like surfaces exist.
- **OpenTelemetry semantic conventions**, including GenAI, agent, and MCP conventions when model-mediated or protocol-mediated paths exist. Record both version and stability status.
- **A2A / inter-agent protocols**, including Agent Cards, skills, task states, streaming, push notifications, registries, and authentication if such surfaces exist.
- **Provenance standards** separately for runtime/action records, content credentials, and build/source attestations where applicable.
- Relevant model-provider or agent-framework documentation for tool use, handoffs, guardrails, tracing, and evals.
- **NIST AI RMF** when AI risk-management findings are in scope.
- **OWASP GenAI / LLM / agentic / MCP risk materials** when security or safety findings are in scope.
- Computer-use and browser-use sandboxing patterns from current vendor guidance.

Do not assume the agent's training data reflects current versions. Record the pinned version of each anchor in `00-scope.md`.

---

## 15. Global Boundary Declarations

Per-step boundaries are declared inline at each phase. The following apply globally. The agent must not:

- modify source code;
- recommend folder moves during audit phases;
- infer bounded contexts from folder names alone;
- cite sources it cannot read in-session;
- equate schema presence with contract discipline absent registry, validation, producer/consumer mapping, or versioning;
- collapse MCP, A2A, workflow, callback, or remote-agent protocol surfaces into a generic "tool" finding when the concrete objects can be inventoried;
- skip halt conditions;
- produce `SUMMARY.md` before phases 0–10.5 artifacts exist;
- use hook-bypass or verification-bypass mechanisms (`--no-verify` and equivalents);
- produce prose findings without citations;
- paper over contradictions with speculation;
- expand scope without operator direction;
- silently correct stale evidence;
- collapse current-state findings and future-state fitness functions into one ID;
- treat non-runtime prompt artifacts as irrelevant without classification;
- treat server-exposed prompts as documentation-only;
- treat approval presence as sufficient without checking precedence, bypass modes, protected paths, secondary credentials, callbacks, and enforcement;
- conflate request-local state, session state, durable conversation state, long-term memory, retrieval corpora, retrieval indexes, artifacts, and operator-authored persistent rules;
- conflate runtime/action provenance, content provenance, and build/source provenance;
- score missing development-stage semantic conventions as strictly as missing stable conventions without recording stability status;
- weight findings by severity alone if a strategic theme is supplied;
- edit `profile/cycle-history.md` directly (audit proposes via `cycle-history-notes.md`; profile commits).

---

## 16. Versioning

This specification is **v3.1** dated 2026-05-08.

Breaking changes bump the major version. Additive schema fields, additional examples, or clarification of existing behavior bump the minor version. Patch versions correct wording without changing behavior.

Each audit records:

- audit spec version;
- profile directive version;
- profile snapshot date;
- current branch and revision;
- audit mode;
- strategic themes, if any;
- pinned versions of reference anchors used during the audit (§14).

Changes from v2.0:

- Added Phase 10.5 finding smoke-test with eight outcome states.
- Added Phase 8.0 prompt-surface classification and Phase 8.1 policy treatment.
- Added §1 directive-as-handoff operating model with audit-mode enum.
- Added §4.3 halt-recovery state machine.
- Generalized SDK-relevance to multi-theme strategic weighting (§11.12 default-mapping table).
- Promoted prohibitions to per-step boundary declarations inline at each phase.
- Separated Phase 10 findings into structural-current-state (`F-NNN`) and missing-safeguard (`FF-NNN`) lists with independent IDs.
- Added subagent, computer-use, browser-use, durable-workflow, A2A surfaces to Phases 3, 4, 6, 7, 9.
- Added provenance to the cost/latency/quality observability quartet.
- Added LLM-as-judge calibration as a distinct eval mode.
- Added context-assembly logic (retrieval filters, tool descriptions, skills/SOPs) to Phase 8 scope.
- Citation schema gained `evidence`, `method`, `snapshot_ref`, `current_ref` fields.
- BoundedContext status enum gained `rejected | merged | split` outcomes; added `authority_basis` field.
- Finding schema gained `confidence`, `strategic_relevance`, `snapshot_evidence`, `current_evidence`, `smoke_test`.
- Scoring rubric expanded from 8 to 11 dimensions (separate Policy/prompt, Evals, Governance, Fitness functions).
- Audit emits `cycle-history-notes.md` as proposals only; profile directive owns commits to `profile/cycle-history.md`.
- Caveat classification (substantive / cosmetic / exact-match) made first-class in §9.6.
- Reference anchors expanded to include NIST AI RMF and OWASP GenAI materials.

Changes from v3.0:

- Added protocol-aware inventory for MCP tools, resources, resource templates, prompts, roots, sampling, elicitation, completion, and authorization metadata.
- Added A2A Agent Card, advertised skill, task-state, streaming, push-notification, registry, and authentication handling.
- Added workflow-description and overlay contract handling alongside API descriptions and schema dialect pinning.
- Expanded execution-mode taxonomy to cover background, paused-for-approval, resumable, durable, callback-mediated, and event-triggered paths.
- Replaced simple authority fields with authority-matrix requirements covering approval mode, precedence, bypass modes, protected paths, secondary credentials, callback authentication, hosted/local boundaries, and token delegation.
- Split state and memory into request-local state, session state, durable conversation state, long-term memory, retrieval corpus, retrieval index, artifact store, evaluation dataset, checkpoint state, and operator-authored persistent rules/memory.
- Split provenance into runtime/action, content, and build/source classes.
- Added semantic-convention version and stability-status pinning.
- Added server-exposed prompt classification and privileged-context injection checks.
- Added protocol, approval, async lifecycle, and memory lifecycle eval coverage flags.
- Added companion-artifact drift controls for kickoff prompts, friendly explainers, manifests, examples, and other derived guidance.

## Appendix A — Migration from v2 to v3.x

For projects with a v2 audit cycle on file:

1. Run the profile discovery directive (current version per `MANIFEST.md`) to refresh the profile (it emits diff artifacts, strategic-themes blocks, and protocol/authority/state/provenance baselines).
2. Initialize `profile/cycle-history.md` from the v2 cycle's directive series — the prior cycle becomes "cycle 1, retrospective entry."
3. First v3.x cycle inherits v2 conventions; record them in `cycle-history.md` rather than restating them in directives.
4. Run Phase 10.5 against the v2 findings list as a one-time validation (catches drift accumulated since v2 ship).
5. Apply strategic-theme weighting; if no theme was specified at v2 time, treat as `none` and re-run Phase 10 prioritization.

The diff between v2 and v3 outputs is itself useful audit signal — it shows what the older spec missed.

---

## Appendix B — Migration from v3.0 to v3.1

For projects with a v3.0 audit cycle on file:

1. Preserve the v3.0 audit artifacts as the historical record.
2. Run the profile discovery directive (current version per `MANIFEST.md`) to refresh protocol, authority, state, provenance, and companion-artifact fields.
3. In Phase 0, record v3.0-to-v3.1 drift separately from code drift.
4. Re-run Phases 3–8 and 9 for any project exposing MCP, A2A, background/resumable execution, server-exposed prompts, or durable memory.
5. Re-score Phases 10 and 10.5 only after protocol surfaces, authority matrix, memory classes, semconv stability, and provenance classes have been pinned or marked not applicable.
