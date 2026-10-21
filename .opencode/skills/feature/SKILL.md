---
name: Feature
description: Build one Irbis feature end-to-end — clarify rules and media first, write the spec and briefs, implement the app/api/web slices, keep checks green, and hand over for manual testing. Use this whenever the user names a feature to build, asks to run /feature, or wants a complete product slice across irbis-app, irbis-api, or irbis-web.
---

# Build one Irbis feature

Build the feature named in the request. Treat any additional text as notes, constraints, and out-of-scope items.

The owner names a feature; deliver every part it needs — **app** (bare RN), **api**, **web** (only if the feature needs admin/back-office). One feature per session. When it is done, **stop**; the next feature starts only when the owner says so.

**Token rules.** Start in a fresh session launched from `irbis-docs` (`./scripts/start.sh`), so the agents and hooks load and no old history rides along. If this conversation already holds another feature, ask the owner to start a new session first. Keep this main session light: ask questions, write the spec and briefs, delegate, and relay ≤10-line summaries — never read generated code, full test output, or screenshots yourself.

## 0. Read (no questions yet)

- `STATUS.md`, `PROJECT.md`, the feature's row in `ROADMAP.md`, and the relevant `decisions/` ADRs.
- The requirements for this feature in the Product Overview (`PROJECT.md` → Sources of truth), plus `design/canvas-rules.md`.
- The feature's screens in `design/canvas/` (the `.dc.html` boards the roadmap row names) — their text, states, numbers, and notes. Light + dark variants if present.
- Each touched repo's `docs/architecture.md` (domain model, structure) so the plan fits what exists.
- Existing code for anything this feature builds on (models, endpoints, components) — reuse, don't duplicate. Find it with `graphify explain/query` in each repo (see `CLAUDE.md` → Code map), not by browsing files.

## 1. Ask before building — rules and media (STOP for answers)

**Rules.** List every point where the doc, the canvas, and the existing code leave a choice open or disagree, and the choice changes behaviour or a test's expected result — XP amounts and caps, thresholds, limits, timers, day/week boundaries, who can do what, what happens at empty / offline / permission denied / failure, conflicts between doc and canvas. Ask with the `question` tool: up to 4 per round, max 3 rounds; options are concrete behaviours (the one the doc/canvas best supports first, citing where), "Leave open" last. Never ask what the doc, canvas, or ADRs already answer — cite them instead.

**Media.** List every image, animation, or video the screens need and say which already exist (`design/assets.md`: canvas SVGs) and which do not — e.g. badge art, league tier emblems, mascot animations or videos, companion poses, illustrations, sounds. Write the list to `design/media/<slug>/MEDIA.md`:

`| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |`

Ask the owner to drop the needed files into `design/media/<slug>/` (or attach them), and ask which canvas SVGs are final. For each missing item ask: wait for it, or ship a labelled placeholder now and swap later (a placeholder is tracked as a `STATUS.md` known issue, never left silently).

Then STOP until the owner answers. Record every answer in the spec's Assumptions as `Q{n} (owner, date): …`.

## 2. Spec (short approval)

Write `features/<slug>.md` from `features/_TEMPLATE.md`: goal, surfaces, endpoints, data model changes, numbered `AC1…` (answers folded in, concrete values), required UI states, QA events, testIDs, media, waivers, out of scope. **Size cap: about 8 ACs.** If the feature needs more, propose splitting it into two features (e.g. app vs. admin web) before approval. Show the AC list and ask "approved?" — one short gate; on "approved" continue without stopping again unless something new and blocking comes up.

## 2b. Briefs — slice the work

Split each repo's work into slices of 2–5 ACs that each end in a green, committed state (API first, then each client slice that uses it). For each slice write `features/briefs/<slug>-<n>-<repo>.md` from `features/_BRIEF_TEMPLATE.md` (60–80 lines): the ACs, files to touch and to read for patterns, endpoints + error codes, exact copy in en/ru/uz taken from the canvas boards (so the dev agent never opens the canvas HTML), testIDs, QA events, approved packages. Commit the briefs. A slice that hits a limit loses only itself.

## 3. API slices — if the feature touches the api

One fresh subagent per brief, in order: "implement `features/briefs/<slug>-<n>-irbis-api.md`". It reads only `RULES.md`, the brief, and the listed files; replies in ≤10 lines. Values the doc calls "decided after testing" go in server config. Use the configured `api-dev` agent when available; otherwise use a general subagent with the same brief.

## 4. Client slices — app and web slices may run in parallel

One fresh subagent per brief. The brief already contains the copy, testIDs, and the generated hooks to use; media is copied from `design/media/<slug>/`. Use the configured `app-dev` and `web-dev` agents when available; otherwise use general subagents with the same briefs.

## 5. No reviewer

Do not launch the reviewer subagent (owner decision 2026-10-18). Each dev agent's `npm run check` (green, output in its summary) is the gate; the slop checklist in `CLAUDE.md` stays binding for the dev agents.

## 6. Hand over for manual testing (owner)

No QA agents or `/qa-*` commands (owner decision 2026-10-18). Testing is manual by the owner on Android and iOS. Give the owner a short checklist: one line per AC with where to look and what to expect. Bugs they report go through `/bugfix <error/log + failing behaviour>` (failing test first).

## 7. Wrap up and STOP

The next feature means a new session — never carry this feature's history into the next one.

- Spec → Done.
- `STATUS.md`: Done line with commits per repo, "manual test by owner pending", open issues and placeholders.
- Run `graphify update .` in each touched code repo.
- Commit `irbis-docs`. Do not push.
- Reply: what was built per surface, AC → test coverage, the manual test checklist, anything open or placeholder, and "Ready for the next feature when you say so."

Do **not** start another feature.
