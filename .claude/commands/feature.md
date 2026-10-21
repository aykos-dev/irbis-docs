---
description: Build one feature end to end — questions + media first, then app/api/web, then hand over for the owner's manual test; stop when done
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

## 0. Read (no questions yet) — slices, not whole files
- `STATUS.md` from `## In progress` down only (`sed -n '/^## In progress/,$p' STATUS.md`); the Done history is
  not needed. `PROJECT.md`. Only the `decisions/` ADRs this feature touches.
- The feature's row in `ROADMAP.md` (`grep -n -A3 '<slug or feature name>' ROADMAP.md`), plus the matching line in
  its "Doc ↔ canvas conflicts" list — never the whole file.
- The requirements for this feature in the Product Overview (`PROJECT.md` → Sources of truth; read only the doc's
  matching section with the docs connector). From `design/canvas-rules.md` only the bullets that name this
  feature's boards or rules (`grep -n -i '<board>\|<keyword>' design/canvas-rules.md`).
- The feature's screens in `design/canvas/` (the `.dc.html` boards the roadmap row names) — their text, states,
  numbers and notes. Light + dark variants if present.
- Each touched repo's `RULES.md`. Open `docs/architecture.md` only when the feature adds a new domain module or
  changes the structure — and then only that section.
- Existing code for anything this feature builds on (models, endpoints, components) — reuse, don't duplicate.
  Find it with `graphify explain "<Symbol>"` / `graphify affected "<Symbol>"` in each repo (see CLAUDE.md →
  Code map); `graphify query … --budget 500` only when you have no symbol name. Do not browse files or read
  `GRAPH_REPORT.md`.

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

## 2b. Briefs — one per repo, slice only when big
Each new agent run costs a fresh context and its own `npm run check` loops, so use as few as possible:
- **One brief per repo** when that repo's share of the feature is ≤5 ACs (the usual case).
- Split a repo into slices only when it has >5 ACs; each slice is 3–5 ACs and ends green and committed.
- Order: api first; then app and web together.
For each brief write `features/briefs/<slug>-<n>-<repo>.md` from `features/_BRIEF_TEMPLATE.md` (60–80 lines): the ACs,
files to touch and to read for patterns, endpoints + error codes, testIDs, QA events, approved packages.
**Copy goes in one shared file**, `features/briefs/<slug>-copy.md` (i18n key | en | ru | uz, taken from the canvas
boards so no dev agent opens the canvas HTML). Briefs reference its keys instead of repeating the table.
Commit the briefs.

## 3. API slices (subagent: api-dev, Opus) — if the feature touches the api
One fresh agent per brief, in order: "implement features/briefs/<slug>-<n>-irbis-api.md". It reads only RULES.md, the
brief, the copy file if the brief names one, and the listed files; replies ≤10 lines. Values the doc calls "decided after testing" go in server config.

## 4. Client briefs (subagents: app-dev, web-dev — Opus; launch app and web in parallel, in one message)
One fresh agent per brief. The brief names the generated hooks and testIDs, and points to `<slug>-copy.md` for copy;
media is copied from `design/media/<slug>/`.

## 5. No reviewer
Do not launch the reviewer subagent (owner decision 2026-10-18). Each dev agent's `npm run check` (green, output in
its summary) is the gate; the slop checklist in CLAUDE.md stays binding for the dev agents.

## 6. Hand over for manual testing (owner)
No QA agents or `/qa-*` commands (owner decision 2026-10-18). Testing is manual by the owner on Android and iOS.
Give the owner a short checklist: one line per AC with where to look and what to expect. Bugs they report go
through `/bugfix <error/log + failing behaviour>` (failing test first).

## 7. Wrap up and STOP
(Next feature = new session or `/clear` — never carry this feature's history into the next.)
Spec → Done. STATUS.md: Done line with commits per repo, "manual test by owner pending", open issues and placeholders.
Run `graphify update .` in each touched code repo. Commit irbis-docs. Do not push.
Reply: what was built per surface, AC → test coverage, the manual test checklist, anything open or
placeholder, and "Ready for the next feature when you say so." Do **not** start another feature.
