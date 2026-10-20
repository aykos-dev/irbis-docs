# lessons

- Status: Draft — not started; build after `lessons-admin` (owner, 2026-10-20). Answers below are already decided;
  `/feature lessons` asks only what is still open.
- Surfaces: api (public lesson endpoints, completions, hearts, guest merge) | app (LessonsHub, Quiz, correct/wrong,
  lesson complete)
- Builds on: `lessons-admin` (content model, published lessons, images), `levels` (`award`, `recordFact`, tier gates),
  `auth` guest-merge registry.

## Decided (owner answers from the `lessons-admin` session)
- Q1 (owner, 2026-10-20): hearts = daily pool of 5 per Asia/Tashkent day, refilled to 5 at 00:00; a wrong answer
  costs one (Quiz).
- Q2 (owner, 2026-10-20): at 0 hearts new lessons lock until midnight ("Out of hearts — back at midnight");
  finished lessons can be replayed as practice with no heart cost and no XP; starting a new lesson needs ≥ 1 heart.
- Q3 (owner, 2026-10-20): XP per lesson = 10 on first completion, 15 if no heart lost (doc 10–15), server config;
  the correct sheet says "Nicely done!" without a per-answer XP number; XP shown on a lesson-complete screen.
- Q4 (owner, 2026-10-20): guests take lessons; completions stay on the phone and are sent on sign-up / log-in
  through guest-merge (XP then). Opened lessons are cached; a completion made offline is queued and synced.
- Q5 (owner, 2026-10-20): all tiers open to everyone, any order (no lesson locks; only level gates need them).
- Q6 (owner, 2026-10-20): daily goal ring = lessons finished today (Tashkent) out of 3 (server config), text
  "Daily goal · 3-minute lessons"; streak line and flame come with `streaks`.

## Still open (ask in `/feature lessons`)
- Lesson-complete screen (no canvas board) · re-asking wrong answers at the end · offline hearts reconciliation ·
  the "Tier X lessons are open" line on LevelUp · sounds (correct chime).
