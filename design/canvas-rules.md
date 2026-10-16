# Canvas rules vs the written requirements

Compared: canvas version `1792126344-9e9d` (snapshot 2026-10-16, see `canvas/README.md`), i.e. the rule boards GameSpec, CampSpec, FeedSpec, the canvas `notes` in `canvas/canvas.json`, and every number stated on a screen, against the requirements summary (levels, XP table, streaks, leagues, chest, Top Shots, auto-alert, SOS, Add a Spot, Plus, Bu qayer?, moderation).

Result: every number in the summary is confirmed by the canvas (level XP 300/1,000/2,500/5,000/9,000/15,000; 40-120 / 10 / 10-15 / 150 +5 / 150-100-50 / 5 per day; Bu qayer? k = 30/120/8, 5 daily places, reset 00:00 Tashkent, 60 s duels; Campfire 5-15 per game, 30/day; Top Shots Mon 00:00 to second Sun 23:59; auto-alert at return + 1 h; SOS 3 s; 3 photos; 3 community check-ins; Plus 29,000 / 249,000 / 7-day trial / 2 offline regions; 3 trusted reports; 3 posts/day for new accounts; league ~15 people, top 5 up, bottom 3 down). Differences are below. Board names are file names without `.dc.html`.

## (a) Rules and numbers on the canvas that the summary does not have

Progression
- **Per-level gates** (Companions): L2 "300 XP · 2 safety lessons · 2 verified check-ins"; L3 "1,000 XP · Tier 2 lessons · 5 check-ins at difficulty 2+"; L4 "2,500 XP · Tier 3 lessons · 8 check-ins at difficulty 3+"; L5 "5,000 XP · First-aid tier · 12 check-ins at difficulty 3+"; L6 "9,000 XP · Tier 5 lessons · 15 check-ins at difficulty 4+"; L7 "15,000 XP · all tiers · 25 check-ins at difficulty 5 · 3 verified spots".
- **Level unlocks** (Companions): L1 difficulty 1; L2 difficulty 2; L3 "difficulty 3, overnight trips"; L4 "scrambles, high passes"; L5 "difficulty 4, lead group trips"; L6 "verify other explorers’ spots"; L7 "difficulty 5, Legend frame". Names: Wanderer, Burrower, Pathfinder, Ridge Walker, Mountain Guardian, Sky Watcher, Snow Legend.
- Check-in counts only with GPS (Level): "GPS check-in on site counts; photos alone don't."
- Places have a minimum level (Place: "Requires Level 2 · Burrower or higher"; Search: "needs Level 5"; Place trail "Ridge Walker+"; Gear: crampons "Requires Ridge Walker", "Level 4").
- Lesson tiers (LessonsHub): Tier 1 Trail Basics, 2 Mountain Ready, 3 Ridge Skills, 4 Snow & Scrambles ("Unlocks when you reach Level 4"). Quiz correct answer "+10 XP" (Quiz).
- **Hearts**: 5 shown; a wrong answer costs one ("Not quite — you lost a heart") (Quiz, LessonsHub).
- **Daily goal** ring "2/3" with "3-minute lesson" (LessonsHub).
- **Gems** currency (380 on Home): Bu qayer? hint "Hint · region" costs 20 (GameRound); streak freezes cost gems on Free, "2 / month" on Plus (PlusPaywall).
- Summit gives "+620 m League elevation" = the trail's ascent (Summit, TrailMap "+620 m Ascent"); "5 Week streak" is the weekly explorer streak (Summit, Home "4-week explorer streak").
- Seasonal collection "Autumn Colors 2 / 5 places", "26 days" left; LIMITED badges/packs (Home, Badges, GameHub, GameBadges).
- Badge catalog "23 of 64 collected"; thresholds e.g. Peak Bagger II 6 peaks, III 15 peaks, Lake Hopper 3 lakes, Camp Master 4 nights, Trail Buddy 5 group trips, Safety Star "All check-outs on time", Group Leader Level 5, Verified Scout Level 6, Legend Path Level 7 (Badges).

Trips and safety
- SOS settings (Safety): "Send location by SMS", "Also call emergency services — Dials 112 after alerting contacts" (default off), "Test SOS (no alert sent)", multiple contacts with one "Primary". Share trip plan by Telegram / SMS / Link; guardian sees "last location sent 2 min ago" (TripPlan, ActiveTrip).
- Offline maps storage "540 MB of 2 GB", per-region sizes, "update available" (Safety). Trail "Offline · 24 MB" (TrailMap).
- Trip plan: "Back by" time, "Sunset 18:21 · that leaves 50 min of daylight buffer", gear checklist "5 / 7 packed" (TripPlan).
- Create trip: "Max people 10", minimum level suggested from difficulty, "Lower levels can request to join with a leader's approval", carpool "3 seats offered" (CreateTrip).
- Verified leader needs Level 5 (Profile "Verified leader · at Level 5"); Find buddies filter "Mentors (L5+)" (Buddies).
- Public groups: "Public groups over 500 members need 2+ admins" (canvas notes `n_report`).

Add a Spot
- Duplicate check radius: "2 spots already exist within 1.5 km." (Spot4Duplicate). GPS shown as "Accuracy ± 6 m · 9 satellites" (Spot1Gps; no threshold stated). "spots must be added in person".
- Visibility: Public ("after review") or "Fragile — my groups only" (Spot4Duplicate); Fragile spots show only the region name in posts (FeedSpec) and are never used as game rounds (GameSpec).
- Second gate: "Official verification — Reviewed for safety & access" after 3 community check-ins (Spot5Submitted, MySpots). Place page shows "Officially verified · Confirmed by Ugam-Chatkal park rangers".
- Optional 360 step "+20 XP" (GameSpec).
- Discoverer total on MySpots: 1,220 = 150 + 45 + 1,025 (per-visit XP 5 x 9 and 5 x 205).

Bu qayer? (GameSpec and screens)
- Per-round XP: "≥4,500 / ≥3,000 / ≥1,500 / less" = "5 / 4 / 3 / 1"; "Finish daily challenge +5"; "Daily cap from the game 30".
- Points table for k = 30 (1 km 4,836 ... 60 km 677); max daily 25,000 (GameSummary).
- Friend duel win "+3 XP", "Duelist badge 5 / 10" (GameDuel); challenge "23 h left" (Notifs).
- "first real check-in at a guessed place earns 2× XP" (GameSpec, GameResult).
- Packs: "Fergana Valley pack · 10 places · this week"; "Practice · Endless · no XP after the daily cap" (GameHub).
- Pushes: one 19:00 push, "Max 1 game push per day" (notes `n_g_entry`).
- Badge thresholds: Eagle Eye within 1 km (x3), Perfect Day 20,000+, Daily Explorer I–III 7 / 30 / 100 days, Region Expert avg 4,000+, Duelist 10 wins, Seen It For Real 5 places, Bullseye within 100 m (GameSpec, GameBadges).
- Imagery: Mapillary primary (attribution on every view), Google Street View paid fallback "$14 per 1,000 loads after 5,000 free a month ≈ $0.07 per 5-round daily"; anti-cheat server-side scoring (GameSpec).
- Companion reaction by score: "cheering ≥4,500, happy ≥3,000, thinking ≥1,500, worried below" (notes `n_g_result`).

Campfire (CampSpec, CampHub, Camp*)
- Players: Imposter 3–15, Mafia 6–15, Who am I? 3–12, Would you rather 2–15; "warn at 20%" host battery; reconnect keeps seat; pass-and-play for Imposter / Who am I / Would you rather; "spicy pack off by default".
- Imposter: discussion timer 3 min, imposter count, "Imposter sees the category" toggle, word pack "240 words" (CampLobby).
- Mafia: roles Boss, Mafia, Detective, Doctor (self-save "1 self-save left"), Maniac (solo), Lover, Bodyguard, Civilian; "Reveal role when out" toggle; narrator "App voice / Host reads"; day vote: majority exiles, tie means revote, second tie nobody exiled, host can pause timer, "you can also skip the vote" (MafSetup, MafDay, notes `n_m_day`).
- Secrets: hold-to-reveal, Android screenshots blocked, iOS blur on screen recording (notes `n_c_reveal`).
- Badges: spec names Poker Face, Sharp Detective, Life Saver, Mind Reader, Campfire Host.

Community
- Top Shot badge tiers: Bronze first Top 10; Silver 5; Gold 10; "Shot of the Fortnight" for #1; #1 gets "Gold frame on profile for 2 weeks" (FeedSpec, TopShotWin "1 / 5 to Silver").
- Winner eligibility: posted during the round, tagged with a place where the author has a verified check-in, own photos only (no reposts or operator marketing), ties go to the post that reached the count first (FeedSpec).
- Like rules: only likes from accounts older than 7 days with verified phone count; no self-likes; ranks (not counts) shown in the last 24 hours; "max one push per round"; Top 10 get one push, nobody else (FeedSpec, notes `n_f_win`).
- Posts: up to 10 photos, 11th tap shakes the counter, upload queues offline (notes `n_f_photos`); tagged people must approve; operators have a "Tour stories" tab.
- Moderation: reports reviewed "within 24 h"; strikes "warning → 7-day posting mute → ban, with appeal"; new accounts "can't share links or phone numbers" (notes `n_report`). Report reasons (7): Unsafe behaviour, Wrong or fake place, Not their photo, Reveals a fragile place, Spam or advertising, Harassment or hate, Inappropriate content (ReportSheet). Reporter can "Hide all posts from" or "Block" the author (ReportDone).
- Weekly chest reward is not specified; only "Check in at 3 places" (Home).

Money
- Plus: "SAVE 28%" yearly (20,750 so'm / month equivalent); Free vs Plus table: forecast "Weekend" vs "7-day hourly", streak freezes "Gems" vs "2 / month", Bu qayer? "Daily + 3 duels" vs "All, unlimited", partner tours "Badge discounts" vs "+5% & early access"; "Never paywall safety, conditions, lessons or levels" (PlusPaywall, notes `n_plus`). Price footnote: "Starting price — to be tested."
- Marketplace is "COMING SOON"; prices/commission/payout are placeholders "[PRICE]", "[RATE]", "[AMOUNT]"; badge discounts "Peak Bagger II · −10%", "Camp Master · −15%", Plus "−5%", paid by Irbis not the operator (Tours, Gear, OperatorDash).

## (b) Conflicts

Canvas vs summary
1. **Spot verification.** Summary: "Add a Spot ≥3 photos, community verification 3 check-ins" and "discoverer 150 (+5/visit)". Canvas: "Community check-ins — 3 explorers confirm it in person" and then "Official verification — Reviewed for safety & access" (Spot5Submitted); "Verification: 3 community check-ins, then an official review." (MySpots); "Chatkal Juniper Camp was officially verified. +150 Discoverer XP." (Notifs); "Discoverer XP is paid on verification, not on submit." (notes `n_spot`). The canvas adds a mandatory official review, and XP appears to be paid at the official step. Also "verify other explorers’ spots" is a Level 6 unlock (Companions).
2. **Skipping levels.** Summary: levels need XP + lessons + check-ins. Canvas Onb3Experience: "Everyone starts as a Wanderer. Experienced? Pass a short safety quiz to unlock harder places sooner." No rule describes this quiz or what it unlocks.
3. **SOS hold is configurable.** Summary: "SOS hold 3 s". Canvas Safety has a switch "Hold to trigger — 3 seconds, prevents pocket alerts" (on), so the hold can apparently be turned off. ActiveTrip: "SOS — press and hold for 3 seconds".

Inside the canvas (the implementation will have to pick one)
4. **Overnight trips unlock.** Companions L3: "difficulty 3, overnight trips". Level (next companion L4): "Unlocks scrambles, high passes and difficulty-3 overnight trips."
5. **Which tier gates Level 4/5.** Level: "Tier 3 safety lessons 4 / 6"; LessonsHub: "Tier 3 · Pathfinder · you" "Ridge Skills" "4 / 6". Safety: "First aid tier · 4 of 6 done. Two more unlock Ridge Walker." Companions L5: "First-aid tier", but LessonsHub Tier 4 is "Snow & Scrambles" and "First aid I" sits in Tier 2.
6. **Streak requirement.** Summary: daily streak = a lesson or Bu qayer?. LessonsHub: "Daily goal 2/3" with "One more 3-minute lesson keeps your 12-day streak." (goal of 3 lessons, but one is said to be enough).
7. **Per-visit XP before verification.** Spot5Submitted: "+150 Discoverer XP when verified, then +5 XP every time someone checks in here." MySpots shows "Community verified 2/3 · 9 visits · +45 XP" (visit XP paid on an unverified spot).
8. **Campfire badge count.** CampHub "Campfire badges 2 / 8"; CampSpec names five (Poker Face, Sharp Detective, Life Saver, Mind Reader, Campfire Host).
9. **Offline map sizes.** Safety: "540 MB of 2 GB" but listed maps are 312 MB + 180 MB (+ 148 MB not downloaded) = 492 MB.
10. **Free game access.** PlusPaywall: "Bu qayer? packs & duels — Daily + 3 duels" for Free; GameHub shows packs ("Fergana Valley pack", "Autumn Colors pack") and "Friend duel" with no Plus marker or limit counter.

## (c) Screens whose text implies behaviour described nowhere

- Safety: three SOS switches (hold, SMS location, call 112) and a "Test SOS" button; per-contact rows with "Primary".
- TripPlan: switch "Auto-alert if I don't check out"; "Your plan is shared when you tap Start."; Telegram / SMS / Link share chips; packed-gear tracking.
- Spot2Photos: switch "Remove location data from public photos" (on). Spot3Details: estimated difficulty, best months, 7 hazard types, water sources, phone signal, road type ("4×4 needed").
- Settings: Units (km·m / mi·ft), Appearance (Light / Dark / Auto), "Show me in Find buddies", "Share location — Only during an active trip" ("Trips only"), "Public profile", Blocked people, "Delete account in Help"; notification toggles incl. "Trip & safety alerts … Always on" and "Streak reminders — Only when your streak is at risk".
- EditProfile: "Show stats on my profile", "Show my home region", bio "74 / 150", "Backpack colour"; "Change photo".
- PostDetails: switch "Enter Top Shots" ("Eligible: verified visit · round ends Oct 25"); "How did you go? Solo / Friends / Tour" (tour links to operator); tag people "pending".
- Home: "Smart swap" card with "Keep plan / Swap place" when a place turns "Not now"; info button "How the path is built"; "Weekly chest"; weather-shield icon on the streak (Notifs: "the weather shield covered last weekend").
- Place: community ratings (Beauty / Difficulty / Crowding, "312 ratings"), "Latest condition reports · See all 27", condition "Updated 40 min ago · forecast + 3 reports", "First Discoverer" credit with visit count.
- Profile: "Rated by trip buddies" (Reliable, Safety-first, Good company) after trips; "Granite · #7" league chip.
- Level, Home: tapping the avatar opens Level progress; "Continue learning".
- Search: tabs Places / People / Groups / Tours, "Recent" searches, locked place "Opens Jan".
- Buddies: filters Level / region / interests, "Invite", "Verified leader", ratings and "trips together".
- GameResult: "Save to my path · first visit 2× XP"; when a place is "Not now" the button becomes "Save for later" (GameSpec). GameSummary "Remind me tomorrow at 19:00", "Next daily in 6 h 12 m", share card with no place names.
- Operator web dashboard (OperatorDash): create tours, rental items, reschedule, reply to reviews, payouts "Next payout Nov 1", commission set in an admin panel; "Irbis notifies them for you" on a storm reschedule. No requirements for operator accounts exist in the summary.
- Notifs: tabs All / Trips / Social / Rewards, "Mark all read".
- Tours/Gear: date chips, "Reserve for Sat 10 Oct", pickup points with opening hours, level-gated rentals.
- Animation notes in canvas.json (`n_summit` confetti 1.2 s, `n_lvlup` 3 s skippable after 1 s, `n_g_result` line draws 0.6 s, etc.) are motion specs, not business rules.
