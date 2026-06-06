# What This Audit Does (Friendly Version)

This explainer targets Agentic Architecture Audit Specification v3.1 (2026-05-08) and Project Profile Discovery Directive v1.3 (2026-05-23). If it conflicts with the spec, the spec wins.

You built something with AI. Maybe it works. Maybe it mostly works. Maybe you can feel it getting harder to change without breaking, and you're starting to wonder if you've painted yourself into a corner.

This audit is a structured way to find out. You hand the spec to a coding agent (Claude Code, Cursor, whatever you're using), it spends a few hours reading your codebase carefully, and it produces a written report of what's actually in there versus what you think is in there. It doesn't change any code. It just tells you the truth, with receipts.

## Why this exists

AI-generated code has its own failure modes. Most of them aren't bugs — they're structural choices that work in a prototype and quietly betray you at scale. The most common ones:

**Business rules end up inside prompts.** "If the amount is over $10,000, ask for manager approval" gets typed into a prompt template because that's where the agent was looking when you gave the instruction. Now your approval threshold lives in a string, isn't tested anywhere, and changes silently when someone edits the prompt.

**Tools have more authority than they should.** A tool called `read_user_data` actually has database write access because the underlying function does both, and nobody noticed. The model name says "read" but the implementation says "do anything."

**Protocol surfaces hide real contracts.** MCP tools, resources, prompts, roots, A2A Agent Cards, remote-agent skills, workflow descriptions, callbacks, and background tasks can all carry different risks. If they're flattened into "the tool server," the audit will miss where authority and state actually cross boundaries.

**Memory and state get tangled.** Request-local state, session history, durable conversations, long-term memory, user preferences, RAG corpus, retrieval indexes, scratch notes, operator rules, audit logs — all dumped into a generic "memory" that nobody owns and nobody can clear.

**Approvals are too vague.** "Human approval required" sounds safe until you find a trusted-workspace bypass, a broad secondary credential, a callback that resumes work out of band, or a path that writes before the approval gate runs.

**You can't tell what the AI is doing.** Which prompt produced that output? How much did it cost? Was it the cheap model or the expensive one? Did it call three tools or thirty? Without instrumentation, you're flying blind.

**There are no evals.** Your code has tests. Your agent has nothing. When you change a prompt, you find out it broke from a customer, not from CI.

The audit catches these things. It doesn't moralize at you. It just shows you, with file paths and line numbers, where each one is happening in your specific codebase.

## What it actually checks

The audit walks through your code in eleven phases, each producing a written artifact. In plain English, the phases ask:

- **Phase 0 — Scope.** What are we actually auditing? What's in, what's out?
- **Phase 1 — Vocabulary.** Does "user" mean the same thing everywhere in your code? "Order"? "Transaction"? When the same word means two different things in two parts of the code, that's where bugs come from.
- **Phase 2 — Boundaries.** Are the parts of your app actually separate, or are they pretending to be separate while sharing everything?
- **Phase 3 — Runtime.** What happens when somebody calls your API? Trace the path. Where does it touch the database? Where does it call a model? Are there loops? Do they terminate?
- **Phase 4 — Contracts.** Do your APIs, tools, resources, prompts, workflows, remote-agent cards, callbacks, and schemas have machine-readable contracts? Do producers and consumers agree? Is anything still ad-hoc?
- **Phase 5 — State.** Where does data live? Is it request-local, session state, durable conversation history, long-term memory, retrieval corpus, retrieval index, artifact, or operator rule? Who owns it? How does it get cleared?
- **Phase 6 — Authority.** What can each agent, tool, script, remote service, or callback actually do? Can the read-only tool secretly write? Can approval be bypassed? Which credentials and scopes are really in play?
- **Phase 7 — Observability.** Can you tell what your system is doing? Cost, latency, quality, runtime/action provenance, content provenance, build/source provenance, and semantic-convention versions — are the important pieces present?
- **Phase 8 — Prompts and policy.** Are your prompts giving instructions or smuggling business rules? Can untrusted content enter privileged prompt context?
- **Phase 9 — Evals.** Is there any automated check that your AI behavior, approval paths, protocol surfaces, async lifecycle, and memory lifecycle didn't regress?
- **Phase 10 — Findings.** Score each dimension 0–3. List the worst stuff first. Suggest "fitness functions" — automated rules to add to CI so the same problem can't come back.
- **Phase 10.5 — Smoke test.** Re-check every finding against the current code, because the audit might have taken hours and the codebase moves.

You don't have to read all of them. The summary is one page. You read the summary; the detail is there if you want to dig in.

## What you have to do first

You don't run the audit cold. There's a precursor called the **profile discovery directive** that runs first. It produces a snapshot of what your repo *claims* to be — the frameworks, the bounded contexts, the conventions, the tools, the prompts. Then the audit tests those claims.

The split exists because LLMs are bad at doing both jobs at once. If you ask an agent to discover *and* judge, it'll cheat — it'll find things that confirm what it expected. If you split the work, the discovery agent has to lay out claims neutrally, and the audit agent has to test them with citations.

You'll see two authority docs in this folder: the profile directive (`profile-directive.md`) and the audit spec (`audit-spec.md`). The kickoff prompt and this explainer are companion docs derived from those authority texts. Run the profile first. Review what it found. Then run the audit.

## How to coordinate with your coding agent

A few rules that make this go well:

**Demand citations for everything.** The single biggest way audits go wrong is the agent making up findings that sound plausible. The spec requires every finding to cite a file path, line range, an evidence excerpt, and the command that produced it. If your agent's report has prose claims with no file references, that's a red flag. Send it back. The spec calls these "evidence-first" rules — they're non-negotiable.

**Let it halt.** The spec lists conditions where the agent must stop and ask you a question instead of guessing. If your agent halts, that's good — it means it caught something genuinely ambiguous. Read the halt artifact, answer the question, let it resume. Don't override halts to "save time."

**Treat artifacts as the record, not the chat.** The audit produces files under `audit/<date>/`. Those files are the audit. The chat is just the agent telling you it wrote files. Don't ask it to "summarize the audit in chat" — read the `SUMMARY.md` it produced.

**Don't skip the smoke test.** Phase 10.5 re-checks every finding against the current code. It catches drift between when the audit started and when it shipped. If your agent wants to skip it because "the findings are still good," don't let it. The whole point is verification.

**Do not accept vague approval language.** The current spec expects the agent to check approval mode, bypass modes, precedence, protected paths, secondary credentials, callback authentication, and enforcement evidence. A screenshot or doc sentence saying "approval required" is not enough by itself.

**Read the caveats section.** The spec asks the agent to flag where its findings are less certain. Honest caveats are signal, not noise. An audit with no caveats is suspicious.

**Don't ask it to fix things.** This audit is read-only by design. Once you have findings, you'll want a *separate* directive to plan the fixes — the audit shouldn't both diagnose and treat. If your agent offers to "just fix this real quick," say no. You want one job done well, not two jobs done sloppily.

## What you get at the end

A folder called `audit/<date>/` containing:

- `SUMMARY.md` — your one-page entry point. Read this first.
- `00-scope.md` through `10.5-finding-smoke-test.md` — the detailed phase reports. Skim or skip as you like.
- `10-findings.md` — the actual list of problems, ranked by priority.
- `10-fitness-functions.md` — proposed automated rules for CI to prevent regressions.
- `00-reference-anchors.json` — pinned protocol, semantic-convention, and companion-doc versions used during the run.
- `cycle-history-notes.md` — suggestions for conventions to adopt going forward.

The findings are ranked by `severity × confidence × strategic_weight × reversibility_factor` — meaning a low-severity issue that's getting worse over time can outrank a medium-severity issue that's stable. The math isn't important; the ranking just stops the agent from burying important things.

## When to run this

Once is good. Quarterly is better. After any major refactor or before any major shipping milestone is best. The first audit is heavier than later ones because the agent has to learn your project from scratch; subsequent audits inherit conventions from a `cycle-history.md` file that grows over time.

You don't have to act on every finding. The audit's job is to make the problems visible with evidence. Triage is your job. Some findings will be "yes that's a real issue, fix this quarter." Others will be "noted, won't matter until we hit 10x scale." Both are valid responses. The point is that you're choosing, not flying blind.

## What if you don't fix anything?

The audit still pays for itself. Even an unactioned audit gives you:

- A current map of how your system is actually structured.
- A list of where the time bombs are, in case one goes off later and you need to triage fast.
- A baseline to compare against next quarter's audit, so you can see what got worse and what got better.

The worst version of running this audit is doing it once, ignoring it, and forgetting. The next-worst version is reading it, panicking, and trying to fix everything in one PR. The good version is reading it, triaging, picking the two or three highest-priority items, and moving on with your life.

---

Spec reference: `audit-spec.md` (full v3.1 specification, 2026-05-08).
Precursor: `profile-directive.md` (v1.3) — run this first to produce the profile snapshot the audit consumes.
