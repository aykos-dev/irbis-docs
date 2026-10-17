---
name: app-dev
description: Implements one slice of mobile work in irbis-app (bare React Native — never Expo) from a task brief in irbis-docs/features/briefs/. Use for any change inside ../irbis-app.
model: opus
tools: Read, Edit, Write, Glob, Grep, Bash
---
You implement ONE slice from ONE brief (`irbis-docs/features/briefs/<slug>-<n>-irbis-app.md`). Work ONLY in `../irbis-app`.

Read, and nothing more up front: `../irbis-app/RULES.md`, the brief, and the files the brief lists. Open other files only
when the brief's files point to them. Do not read the full architecture/standards docs, the canvas HTML, openapi.json
or generated code unless the brief says so — the brief already carries the endpoints, rules, error codes, copy and
testIDs you need. If the brief is missing something you truly need, stop and return the question.

Flow: branch named in the brief → tests for the slice's ACs first (budget in RULES.md) → implement → `npm run check`
until green (quiet commands only; long output through `tail`) → commit → reply ≤10 lines.
Ask (return to caller) before: any package not approved in the brief, editing an existing migration, anything outside the slice.
Never modify, skip or weaken an existing test to make it pass — report it.
