# Roadmap

Ordered. Each line becomes one `/feature` run (one session each). Edit freely.

## M0 — Foundation (by hand, not via /feature)
- [ ] Scaffold irbis-api, irbis-web, irbis-app with generators (see `SETUP.md`)
- [ ] `npm run check` quiet in all three; `gen:api` in web/app
- [ ] ADRs 001–003 accepted
- [ ] Reference feature built end to end by hand: `health` → app/web show API status

## M1 — Accounts
- [ ] auth — sign up / sign in, JWT + refresh rotation (ADR-001)
- [ ] profile — view/edit own profile

## M2 — Spots
- [ ] spots — admin CRUD for spots (web), list/detail (app)
- [ ] spot-checkin — check in within 200m, once/day/spot, +50 XP

## M3 — Later
<!-- badges, leaderboard, … -->
