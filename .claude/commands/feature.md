---
description: Build one feature end to end — questions + media first, then app/api/web, then the Android QA loop; stop when done
argument-hint: <slug> [— extra notes, constraints, out of scope]
---
Build feature: $ARGUMENTS

The owner names a feature; you deliver every part it needs — **app** (bare RN), **api**, **web** (only if the
feature needs admin/back-office). One feature per session. When it is done you **stop**; the next feature starts only
when the owner says so.

**Token rules for this command.** Start in a fresh session launched from `irbis-docs` (`./scripts/start.sh`), so the
agents and hooks load and no old history rides along; if this conversation already holds another feature, tell the
owner to `/clear` (or open a new session) first. Keep this main session light: it asks, writes the spec and the briefs,
delegates, and relays ≤10-line summaries — it never reads generated code, full test output or screenshots itself.

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
**Size cap: about 8 ACs.** If the feature needs more, propose splitting it into two features (e.g. app vs. admin web)
before approval. Show the AC list and ask "approved?" — one short gate; on "approved" continue without stopping again
unless something new and blocking comes up.

## 2b. Briefs — slice the work
Split each repo's work into slices of 2–5 ACs that each end in a green, committed state (API first, then each client
slice that uses it). For each slice write `features/briefs/<slug>-<n>-<repo>.md` from `features/_BRIEF_TEMPLATE.md`
(60–80 lines): the ACs, files to touch and to read for patterns, endpoints + error codes, exact copy in en/ru/uz taken
from the canvas boards (so the dev agent never opens the canvas HTML), testIDs, QA events, approved packages.
Commit the briefs. A slice that hits a limit loses only itself.

## 3. API slices (subagent: api-dev, Opus) — if the feature touches the api
One fresh agent per brief, in order: "implement features/briefs/<slug>-<n>-irbis-api.md". It reads only RULES.md, the
brief and the listed files; replies ≤10 lines. Values the doc calls "decided after testing" go in server config.

## 4. Client slices (subagents: app-dev, web-dev — Opus; app and web slices may run in parallel)
One fresh agent per brief. The brief already contains the copy, testIDs and the generated hooks to use; media is
copied from `design/media/<slug>/`.

## 5. Review (subagent: reviewer — risky parts only)
Diff stats + risky files (auth, data access, value/XP, new endpoints, edited tests) against the spec and the slop
checklist. Blocking fixes go back as a short fix brief to a fresh dev agent (max 2 rounds).

## 6. Test on the Android phone — the QA loop
1. `/qa-plan <slug>` → case scripts from the AC (the qa-tester subagent; summary only in this conversation).
2. `/qa-run <slug> build` → feature cases + standards suite on the emulator, defects logged to `qa/<slug>/bugs/`.
3. For each defect: `/bugfix <slug>/D{n}` (failing test first), then rebuild and `/qa-retest <slug>/D{n} …`.
4. Repeat 3 until `python3 scripts/qa/case/bugs.py open` shows nothing for this feature — or the owner accepts a
   remaining defect (it stays Open in `qa/BUGS.md` and STATUS.md Known issues).
iOS is checked by hand by the owner; ask them to, and note the result.

## 7. Wrap up and STOP
(Next feature = new session or `/clear` — never carry this feature's history into the next.)
Spec → Done. STATUS.md: Done line with commits per repo, QA run + retest results, open defects and placeholders.
Commit irbis-docs. Do not push.
Reply: what was built per surface, AC → test coverage, QA totals (pass / fail / fixed), anything open or
placeholder, and "Ready for the next feature when you say so." Do **not** start another feature.
