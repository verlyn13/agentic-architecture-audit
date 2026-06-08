## What & why

<!-- One or two sentences. Link the finding, flag, or issue if there is one. -->

## Change class (per AGENTS.md / MANIFEST.md)

- [ ] **Authority-text** change — bumps package **minor/major**; updated the header version **and** `MANIFEST.md` **and** `CHANGELOG.md`
- [ ] **Companion-only** change — bumps **patch**
- [ ] **Tooling / config / governance** — no authority or companion content change

## Done checklist

- [ ] `pre-commit run --all-files` passes (hygiene green; no `--no-verify`)
- [ ] Companions still declare the authority versions recorded in `MANIFEST.md`
- [ ] Repo-relative cross-references resolve
- [ ] Authority texts unchanged, or changed only as a deliberate version cut
- [ ] Commits are Conventional and signed

## Risks / follow-ups

<!-- Anything the reviewer should watch, or "none". -->
