---
description: Build one feature end to end — questions + media first, then app/api/web, then the Android QA loop; stop when done
argument-hint: <slug> [— extra notes, constraints, out of scope]
---
Build feature: $ARGUMENTS

The owner names a feature; you deliver every part it needs — **app** (bare RN), **api**, **web** (only if the
feature needs admin/back-office). One feature per session. When it is done you **stop**; the next feature starts only
when the owner says so.

## 0. Read (no questions yet)
- `STATUS.md`, `PROJECT.md`, the feature's row in `ROADMAP.md`, the relevant `decisions/` ADRs.
- The requirements for this feature in the Product Overview (`PROJECT.md` → Sources of truth; read the doc's
  matching section with the docs connector) and `design/canvas-rules.md`.
- The feature's screens in `design/canvas/` (the `.dc.html` boards the roadmap row names) — their text, states,
  numbers and notes. Light + dark variants if present.
- Each touched repo's `docs/architecture.md` (domain model, structure) so the plan fits what exists.
- Existing code for anything this feature builds on (models, endpoints, components) — reuse, don't duplicate.

## 1. Ask before building — rules and media (STOP for answers)
**Rules.** List every point where the doc, the canvas and the existing code leave a choice open or disagree and the
choice changes behaviour or a test's expected result — XP amounts and caps, thresholds, limits, timers, day/week
boundaries, who can do what, what happens at empty / offline / permission denied / failure, conflicts between doc
and canvas. Ask with AskUserQuestion: up to 4 per round, max 3 rounds; options are concrete behaviours (the one the
doc/canvas best supports first, citing where), "Leave open" last. Never ask what the doc, canvas or ADRs already
answer — cite them instead.

**Media.** List every image, animation or video the screens need and say which already exist
(`design/assets.md`: canvas SVGs) and which do not — e.g. badge art, league tier emblems, mascot animations or
videos, companion poses, illustrations, sounds. Write the list to `design/media/<slug>/MEDIA.md`:
`| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |`.
Ask the owner to drop the needed files into `design/media/<slug>/` (or attach them), and ask which canvas SVGs are
final. For each missing item ask: wait for it, or ship a labelled placeholder now and swap later (a placeholder is
tracked as a STATUS.md known issue, never left silently).

Then STOP until the owner answers. Record every answer in the spec's Assumptions as `Q{n} (owner, date): …`.

## 2. Spec (short approval)
Write `features/<slug>.md` from `features/_TEMPLATE.md`: goal, surfaces, endpoints, data model changes, numbered
`AC1…` (answers folded in, concrete values), required UI states, QA events, testIDs, media, waivers, out of scope.
Show the AC list and ask "approved?" — one short gate; on "approved" continue without stopping again unless
something new and blocking comes up.

## 3. API (subagent: api-dev) — if the feature touches the api
Spec path + slug. Failing tests from the AC first, implement, `npm run check` green, `npm run openapi:export`, commit.
Values the doc calls "decided after testing" (XP, thresholds) go in server config, not constants in code.

## 4. Clients (subagents: app-dev, and web-dev if needed — in parallel)
`npm run gen:api`, implement from the canvas boards (exact copy via i18n keys in uz/ru/en, tokens, light/dark),
media from `design/media/<slug>/` copied into the app's assets, `npm run check` green, commit.

## 5. Review (subagent: reviewer)
All diffs against the spec, the slop checklist and each repo's Quick gate. Fix rounds via the dev agents (max 2).

## 6. Test on the Android phone — the QA loop
1. `/qa-plan <slug>` → case scripts from the AC (the qa-tester subagent; summary only in this conversation).
2. `/qa-run <slug> build` → feature cases + standards suite on the emulator, defects logged to `qa/<slug>/bugs/`.
3. For each defect: `/bugfix <slug>/D{n}` (failing test first), then rebuild and `/qa-retest <slug>/D{n} …`.
4. Repeat 3 until `python3 scripts/qa/case/bugs.py open` shows nothing for this feature — or the owner accepts a
   remaining defect (it stays Open in `qa/BUGS.md` and STATUS.md Known issues).
iOS is checked by hand by the owner; ask them to, and note the result.

## 7. Wrap up and STOP
Spec → Done. STATUS.md: Done line with commits per repo, QA run + retest results, open defects and placeholders.
Commit irbis-docs. Do not push.
Reply: what was built per surface, AC → test coverage, QA totals (pass / fail / fixed), anything open or
placeholder, and "Ready for the next feature when you say so." Do **not** start another feature.
