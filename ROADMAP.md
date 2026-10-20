# Roadmap

From the Product Overview's proposed order: **prove the safe weekly-trip loop in the Tashkent region first**, then
community, then engagement games, then revenue, then expansion. No dates are set.

Each line is one feature = one `/feature <slug>` session (≈8 ACs at most — bigger ones get split), delivered app + api + web (as needed) and finished with the
Android QA loop. The next feature starts only when the owner says so. The split and order inside a phase are a
proposal — reorder freely. Screens refer to `design/canvas/`.

## M0 — Foundation (before feature 1)

- [x] Scaffold irbis-api, irbis-web, irbis-app (`SETUP.md`), `npm run check` + `gen:api`, `qaLog`, real Android package id `uz.irbis.app`
- [x] ADR-001..003 accepted (ADR-001 sign-in method — see open question below)
- [x] `design/design.md` tokens mirrored in app (`shared/constants`) and web (`tokens.css`); Nunito bundled
- [x] Reference feature `health` end to end (QA 9/9 on run 2026-10-17_1119; health/D1, D2 fixed)



## Phase 1 — Launch (Tashkent region): weekly path, places & safety, lessons, levels


| #   | Slug            | What                                                                                                                            | Screens                                                            | Surfaces      |
| --- | --------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ | ------------- |
| 1   | `auth`          | Guest mode + log-in prompt, username/password sign-up & log-in, optional recovery phone + SMS reset, guest-data merge, sign-out | AccLogin, AccSignup, AccGate, AccForgot, AccReset, AccGuestProfile | api, app, web |
| 2   | `onboarding`    | Splash → meet Irbis → language → experience → interests → companion reveal                                                      | Splash, Onb1–5                                                     | app, api      |
| 3   | `places`        | Place catalogue: types, difficulty boots, required level, trails, season bar, hazards; admin CRUD                               | Place, Explore, TrailMap                                           | api, web, app |
| 4   | `conditions`    | Go / Caution / Not now / Seasonal lock from forecast, hazard rules, closures, community reports                                 | Place (condition), Home rings                                      | api, web, app |
| 5   | `levels`        | XP ledger, L1–L7 companions, requirement bars, level-up evolution, difficulty locks                                             | Level, LevelUp, Companions                                         | api, app      |
| 6a  | `lessons-admin` | Web editor for tiers / lessons / questions (uz/ru/en, images), publish; tier gates count published lessons | — (admin, tokens) | api, web |
| 6   | `lessons`       | Safety lessons by tier, micro-lesson cards with hearts, correct / incorrect                                                     | LessonsHub, Quiz*                                                  | api, web, app |
| 7   | `weekly-path`   | This Month's Path (3 places + chest, owner 2026-10-20), status rings, smart swaps, chest                                                  | Home, HomeDark                                                     | api, app      |
| 8   | `trip-plan`     | Trip plan, emergency contact, gear checklist, shared at start; auto-alert SMS 1 h after return                                  | TripPlan                                                           | api, app      |
| 9   | `active-trip`   | Live distance / elevation / time, waypoint check-ins (+10 XP), SOS hold 3 s, check out safely                                   | ActiveTrip                                                         | api, app      |
| 10  | `check-in`      | Verified check-in at a place, XP by difficulty, summit celebration                                                              | Summit                                                             | api, app      |
| 11  | `streaks`       | Daily flame, weekly explorer boot, weather shield                                                                               | Home, Profile                                                      | api, app      |
| 12  | `badges`        | Badge catalogue, progress, profile showcase of 4                                                                                | Badges, Profile                                                    | api, app      |
| 13  | `profile`       | Profile (light/dark), edit profile, settings, notification preferences                                                          | Profile*, EditProfile, Settings, Notifs                            | api, app      |
| 14  | `safety-center` | Offline maps per region (free: 2), emergency contacts, safety tips                                                              | Safety                                                             | api, app      |
| 15  | `search`        | Search places / people                                                                                                          | Search                                                             | api, app      |




## Phase 2 — Community


| #   | Slug                | What                                                                  | Screens                                   |
| --- | ------------------- | --------------------------------------------------------------------- | ----------------------------------------- |
| 16  | `groups`            | Your / public groups, membership, admins                              | Groups                                    |
| 17  | `group-chat`        | Messages + live trip cards, verified leader shield                    | GroupChat                                 |
| 18  | `trip-events`       | Create a group trip (min level, gear, meeting point), join / approval | CreateTrip                                |
| 19  | `buddies`           | Find buddies filters, invites, post-trip ratings                      | Buddies                                   |
| 20  | `feed`              | Posts (≤10 photos), place tag, trip type, tagging, filters, +5 XP/day | Feed, PostDetail, PostPhotos, PostDetails |
| 21  | `moderation`        | Reports, auto-hide, strikes, appeals; admin moderation queue (web)    | ReportSheet, ReportDone                   |
| 22  | `top-shots`         | 2-week rounds, fair likes, winners' wall, rewards                     | TopShots, TopShotWin                      |
| 23  | `add-a-spot`        | 4-step on-site flow, duplicate check, Fragile visibility              | Spot1–5                                   |
| 24  | `spot-verification` | Community 3/3 + official review (web), Discoverer XP, My spots        | MySpots                                   |




## Phase 3 — Engagement


| #   | Slug             | What                                                                            | Screens                                                |
| --- | ---------------- | ------------------------------------------------------------------------------- | ------------------------------------------------------ |
| 25  | `bu-qayer`       | Daily geo-guess: 360° view, pin, score, daily complete, reveal → save to path   | GameHub, GameRound, GameGuess, GameResult, GameSummary |
| 26  | `bu-qayer-modes` | Friend duel, region / seasonal packs, practice, game badges, entry points       | GameDuel, GameBadges, GameEntry                        |
| 27  | `campfire-core`  | Offline hosting: hotspot + QR, local server, lobby, join, reconnect             | CampHub, CampLobby, CampJoin                           |
| 28  | `campfire-party` | Imposter, Who am I?, Would you rather (pass-and-play → campfire-party-2)                      | Imp*, WhoAmI, WYR                                      |
| 29  | `campfire-mafia` | Mafia: roles + balance meter, narration, night actions, day vote                | Maf*                                                   |
| 30  | `leagues`        | Weekly elevation leagues (~15 people), promotion / demotion                     | Leagues                                                |
| 31  | `seasons`        | Seasonal collections + limited badges                                           | Badges                                                 |
| 32  | `gems`           | Gems wallet, chest / streak / badge rewards, spends (hints, freezes, cosmetics) | —                                                      |




## Phase 4 — Revenue


| #   | Slug                 | What                                                                                 | Screens            |
| --- | -------------------- | ------------------------------------------------------------------------------------ | ------------------ |
| 33  | `irbis-plus`         | Subscription (29,000 so'm / month, 249,000 / year, 7-day trial) and its entitlements | PlusPaywall        |
| 34  | `tours`              | Tour marketplace, booking, badge discounts, commission per operator                  | Tours              |
| 35  | `gear-rental`        | Partner gear rental, pickup points, level-gated gear                                 | Gear               |
| 36  | `operator-dashboard` | Operator web dashboard                                                               | OperatorDash (web) |




## Phase 5 — Expansion

All Uzbekistan → Kazakhstan → Kyrgyzstan → park partners (B2B trends with consent).

## Open questions that block the order

- **Sign-in:** decided 2026-10-17 (ADR-001) — guest-first, username + password, optional recovery phone. Still to
pick at `auth`: SMS provider for reset codes.
- **Admin web panel:** not designed. Build from tokens, or design first? → asked when `places` starts.



## Doc ↔ canvas conflicts — asked when their feature starts (details: `design/canvas-rules.md`)


| Conflict                                                                                                                                    | Asked in                       |
| ------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------ |
| Experienced users "pass a short safety quiz to unlock harder places sooner" (canvas) vs levels need XP + lessons + check-ins (doc)          | `onboarding`, `levels`         |
| Overnight trips unlock at L3 (Companions) or L4 (Level screen)                                                                              | `levels`                       |
| Which lesson tier gates L4 / L5 (Tier 3 vs First-aid tier vs Tier 4 Snow & Scrambles)                                                       | `levels`, `lessons`            |
| Daily goal "2/3" lessons vs "one more lesson keeps your streak"                                                                             | `lessons`, `streaks`           |
| Is the 3-second SOS hold switchable off (Safety screen toggle)                                                                              | `active-trip`, `safety-center` |
| Offline storage numbers don't add up (540 MB shown vs 492 MB listed)                                                                        | `safety-center`                |
| Spot verification: is the official review mandatory, and is +150 paid at community 3/3 or at official review; +5/visit before verification? | `spot-verification`            |
| Campfire badge count 2/8 vs 5 named                                                                                                         | `campfire-party-2`             |
| Free tier: "Daily + 3 duels" (paywall) vs no limit shown on Game hub                                                                        | `bu-qayer-modes`, `irbis-plus` |


