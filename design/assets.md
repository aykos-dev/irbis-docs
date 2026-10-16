# Canvas image assets (`/_blob/<id>`)

> **Design-stage art.** All 31 canvas assets are small hand-made SVG files (`image/svg+xml`, 1-5 KB each) stored in the claude.ai canvas asset store, not in this repo. They are placeholders: the mascot, companions, place "photos" and maps are illustrations, not final artwork. Each feature must confirm with the owner whether a given SVG is final before shipping it. The inline SVG/CSS art in section 2 is design-stage too.
> Source: canvas version `1792126344-9e9d` (snapshot 2026-10-16). Board file names are given without `.dc.html`. The canvas is the source of truth.

Totals: 31 assets, 27 used on at least one board, 4 unused (marked UNUSED).

## 1. Image assets

| id | used in (boards) | what it depicts |
|---|---|---|
| `68fc129c9d7433afd4cf66f5c7574e03` | GameEntry, GameSummary, Irbis, Main, OperatorDash | App icon. Teal tile, ridge silhouette, Irbis centred; used as notification/app badge and Operators logo. |
| `9ebec15f083abbb36876b1b8a577ea1b` | ImpReveal, ImpVote, LessonsHub, MySpots, Onb2Language, Onb3Experience, ReportDone, Safety, Splash, WYR | Irbis mascot — default / neutral. Alt "Irbis the snow leopard cub". Splash, speech-bubble guide on onboarding steps, empty/info cards. Not in the mood set on Irbis board but used most widely. |
| `28945aeb0b5964efc16a541c4886feb8` | GameBadges, GameEntry, GameHub, GameSpec, Irbis, MafDay, Onb1Welcome, Onb4Interests, Settings | Irbis mascot — excited (waving). Onboarding welcome, correct answers, game hub header. |
| `443552c224036e8da76bd042b4971bf8` | Irbis | Irbis mascot — proud (summit with flag). Only shown on the Irbis brand board (notification sample "Your spot was verified!"). |
| `9dde5ea7213eff4c8d7f94a43a97ef98` | Home, HomeDark, Irbis | Irbis mascot — worried (umbrella in a storm). Home "Not now" node, storm alerts. |
| `bdd9780b5b61520f5bdf9df8a9366bc4` | GameEntry, Irbis | Irbis mascot — sleepy. Streak-at-risk reminders, empty state, offline. |
| `10d7c4a37401f1367f2af21b82f0ae9a` | Irbis, Leagues | Irbis mascot — sad-but-cute (broken streak flame). League demotion zone. |
| `44b792e405b2dce67f0743e4be0fc2e1` | CampLobby, CampSpec, Companions, GroupChat, Groups, ImpReveal, ImpVote, Leagues, LessonsHub, MafDay, MafEnd, MafNight, Place, PlaceDark, WYR, WhoAmI | Companion L1 — panda cub "Bao" (Wanderer), neutral. Also the generic avatar for Otabek etc. |
| `d4c16d0e9ea4296c5638d9b3cf6bfee5` | CampHub, CampLobby, CampSpec, Companions, GameHub, GroupChat, ImpReveal, ImpVote, Leagues, LessonsHub, MafDay, MafEnd, MafNight, Onb5Companion, Place, PlaceDark, PostDetail, PostDetails, Search, WYR, WhoAmI | Companion L2 — marmot (Burrower), neutral |
| `d1b0d6198561f208461b0f6704094021` | ActiveTrip, Buddies, CampLobby, Companions, CreateTrip, EditProfile, Feed, GameGuess, GameHub, GameResult, GroupChat, Groups, Home, HomeDark, ImpReveal, ImpVote, Leagues, LessonsHub, Level, MafDay, MafEnd, MafNight, Nav, Onb5Companion, PostDetail, Profile, ProfileDark, Quiz, QuizCorrect, QuizWrong, Spot1Gps, Spot4Duplicate, TripPlan, WYR, WhoAmI | Companion L3 — fox (Pathfinder), neutral. The current user (Timur) companion across most boards. |
| `dba7b9623f9af9c690bf93a6ddc5f60b` | Buddies, CampHub, CampLobby, CampSpec, Companions, Feed, GameDuel, GameHub, GroupChat, Groups, ImpReveal, Leagues, LessonsHub, Level, MafDay, MafEnd, MafNight, Onb5Companion, Place, PlaceDark, PostDetail, WYR, WhoAmI | Companion L4 — ibex (Ridge Walker), neutral. Shown black-silhouetted as "next companion" on Level and Lessons. |
| `ffe227711df8d0445b9dfe0a9534a6f4` | Buddies, CampHub, CampLobby, CampSpec, Companions, Feed, GameHub, GroupChat, Groups, ImpReveal, ImpVote, Leagues, MafDay, MafEnd, MafNight, Onb5Companion, Place, PlaceDark, PostDetail, Search, WYR, WhoAmI | Companion L5 — brown bear (Mountain Guardian), neutral |
| `55d73e65f5c5f754c2cbb05b4ea4a0ce` | CampLobby, Companions, ImpReveal, ImpVote, Leagues, MafDay, MafEnd, MafNight, Onb5Companion, WYR, WhoAmI | Companion L6 — golden eagle (Sky Watcher), neutral |
| `09bfc86cfae87bf488a193ee4dab56d8` | Companions, Onb5Companion, PlusPaywall | Companion L7 — snow leopard (Snow Legend), neutral. Only 3 boards; no in-app pose beyond neutral. |
| `beeba6646ed09cf1ddfe63e41e53efb4` | CampHub, MafEnd, Onb5Companion | Companion L1 panda cub — cheering pose. Onboarding companion reveal, Mafia win screen, Campfire hub. |
| `462ee3b41d848c53095996e3c6c9cd45` | CampHub, GameDuel, GameResult, MafEnd, Quiz, QuizCorrect, QuizWrong, TopShotWin | Companion L3 fox — cheering pose. Quiz correct answer, game result/duel winner, Top Shot win, Mafia/Campfire. |
| `95f8b158a1abf050c25de554103067a7` | GameSummary, Spot5Submitted, Summit | Companion L3 fox — proud on summit holding flag. Summit celebration, Spot submitted, Bu qayer? daily summary. |
| `50d9950e59fa02458e7ee6a594563aca` | LevelUp | Companion L3 fox — handing over the backpack. Level-up evolution sequence (outgoing companion). |
| `0c1003d26a9d5fd1e2189c0215a2ab74` | LevelUp, MafEnd | Companion L4 ibex — catching the backpack / pose. Level-up evolution sequence (incoming companion), Mafia win screen. |
| `d8b29a8b752d93f297050ad8b8b4f382` | **UNUSED** | Companion L2 marmot — happy/waving pose with backpack and sparkles. UNUSED on any board. |
| `27834acbbaf9c6d881ede2cfec8d09d3` | **UNUSED** | Companion L1 panda — proud on a summit with teal flag. UNUSED on any board. |
| `7d0ca923c1ec7540f903be8c384dd9ed` | **UNUSED** | Companion L1 panda — bowing / shy pose. UNUSED on any board. |
| `3bcf1e0665966f4e7c7c5bda82dd8d57` | CampHub, CreateTrip, Feed, FeedSpec, GroupChat, Groups, Home, HomeDark, Onb3Experience, PostDetail, PostPhotos, ReportSheet, Search, Spot2Photos, TopShots, Tours | Place illustration — peak (Big Chimgan summit / "Landmark peak"). Generic peak image reused for every peak, experience-level tile, tour, post. |
| `2ea0b851b548b4dce9228408142b7d82` | Explore, Feed, FeedSpec, ImpReveal, MySpots, Onb3Experience, Place, PlaceDark, PostDetail, PostDetails, PostPhotos, TopShots, TripPlan | Place illustration — lake (Urungach Lakes between mountains). Generic lake image reused for every lake and for Place hero. |
| `7000c508ed65b0395bc9ba13d1d81dcd` | Explore, FeedSpec, Groups, MySpots, PostPhotos, Spot2Photos, Spot4Duplicate, TopShots | Place illustration — cave entrance. Generic cave image. |
| `bb7e61cdec3acfef22cb18e86375ffbb` | CampHub, CampJoin, CampSpec, Feed, FeedSpec, MySpots, PostDetail, PostPhotos, Search, TopShots, Tours | Place illustration — camp (tent and campfire by the shore at dusk). Generic camp image; also Campfire hub/join backdrop. |
| `6bbbc6ee6ced1a3bc81f1d2ce372f0fe` | Onb3Experience, PostDetail, PostPhotos, Search, Spot2Photos, Spot4Duplicate, TopShotWin, TopShots | Place illustration — trail / approach path (Gulkam Canyon trail). Generic trail image. |
| `3c359f247bc28d3c219d502ed9bcf7f1` | CreateTrip, Explore, GameGuess, GameResult, GameRound, Gear, Spot1Gps | Map backdrop — light topographic map (390x844). Stand-in for map tiles on Explore, Add a Spot GPS, Create trip, Bu qayer? mini-map, gear pickup. |
| `503359adde6de4ff6ee9e3f4425fa64a` | ActiveTrip, TrailMap | Map backdrop — trail terrain map (390x844). Stand-in under route lines on Trail map and Active trip. |
| `3e544b2c4849c05490b361e1fe5ff4dc` | **UNUSED** | Map backdrop — dark-mode topographic map (#1B2A2F, blue river). UNUSED on any board (dark map exists but no dark map screen references it). |
| `adc9df09c7edf6477c00ce2f292fe37a` | GameEntry, GameGuess, GameHub, GameResult, GameRound, PostDetail, PostPhotos, TopShots | 360 degree panorama stand-in — mountain valley, river, poplars, dirt road, blank road sign, raised wooden platform. Bu qayer? round/teaser and as a post photo. A single static image, not a real 360 viewer or Mapillary imagery. Added 2026-10-09, after the others. |

Pose coverage gaps: only the Irbis mascot has a mood set (5 poses + default). Companions have a neutral pose each; extra poses exist only for fox (cheering, summit flag, handing backpack), ibex (catching backpack), panda (cheering; two unused poses) and marmot (one unused pose). Bear, eagle and snow leopard have neutral only.

## 2. Visuals drawn in code (no image asset)

What the boards render as inline SVG or CSS instead of an image. This art does not exist as a file yet.

| Visual | How the canvas draws it | Boards | Missing as an asset |
|---|---|---|---|
| Badges (64 in the catalog, 23 shown as collected) | Hexagon `clip-path` shape in a flat colour with a 24x24 glyph path (peak, lake, cave, tent, boot, flag, shield, flame, leaf...), a 4 px drop-shadow, grey + padlock when locked; "LIMITED" ribbon for seasonal ones | Badges, GameBadges, Summit, CampHub, FeedSpec, GameSpec, MafEnd, Tours (discount hex), Place ("Badges you can earn here") | All badge artwork: 64+ unique emblems, locked/unlocked variants, 3D flip unlock animation |
| League tier emblems | 5 flat "gems" (hexagon-like shapes) in a row: Pebble brown, Granite grey with a peak glyph, then three unnamed grey placeholders | Leagues | Emblems for Pebble, Granite, Basalt and the two tiers beyond; promotion/demotion art |
| Top Shot badge tiers and frames | Hexagon + camera glyph in bronze/silver/gold, trophy glyph for "Shot of the Fortnight"; "gold frame on profile" is only described | FeedSpec, TopShots, TopShotWin | Bronze/Silver/Gold/Fortnight emblems, the gold profile frame, Legend frame (Level 7), Plus "frames" |
| Place photos | Not drawn in code: only 5 illustration SVGs exist (peak, lake, cave, camp, trail) reused for every place, post and tour | Place, Explore, Feed, Groups, Search, Tours, TopShots | Real photography or per-place art (Place gallery shows a "1 / 48" photo counter; Explore lists "42 places near you"); user post photos; tour cover photos |
| 360 degree imagery | One static panorama SVG as a stand-in; the viewer UI (drag hint, compass, zoom) is CSS overlays | GameRound, GameGuess, GameResult | Real 360 view (spec: Mapillary primary, Google Street View fallback, Irbis community 360s); round imagery per pack |
| User avatars | Companion image on a tinted circle; the profile/edit avatar is an initials circle ("TK") in a CSS circle; "Change photo" and "Backpack colour" controls have no art | Profile, EditProfile, Groups, GroupChat, Feed, Leagues, Camp* | Uploaded profile photos, backpack colour variants, companion styles/frames (Plus), guest/leader avatars |
| Companion extra poses | CSS: `filter: brightness(0)` silhouettes for locked companions | Onb5Companion, LessonsHub, Level | Reaction poses the notes require: happy, thinking, worried (Bu qayer? result by score), concerned (wrong quiz answer), evolution flash, per-level summit poses |
| Map tiles / maps | Static SVG backdrops; pins are rotated rounded-square CSS shapes with glyphs; routes are inline `<path>`; "You are here" is a CSS circle; cluster "12" is a CSS circle | Explore, TrailMap, ActiveTrip, Spot1Gps, CreateTrip, GameGuess, Gear | Real map style, dark map (asset exists but is unused), offline region tiles |
| Place-type and condition icons | Inline 24x24 paths: peak, lake, cave, camp, trail, Go check, Caution "!", Not-now cross, Seasonal, lock | Main (design system), Explore, Home, Place, Search | Icon set as files |
| Home path node map | Inline SVG winding path with CSS ring/core nodes, coin shower and rain particles are only described | Home, HomeDark | Node art, gold-completed state with star, animation assets |
| Lesson unit icons and progress rings | Coloured circle + inline glyph (compass, leaf, padlock, cloud, paw, first-aid cross, mountain, waves, avalanche, bolt) with SVG ring | LessonsHub | Unit artwork, lesson illustrations, quiz question images |
| Currency/stat glyphs | Inline: streak flame, gem (diamond), XP bolt, boot (difficulty/week streak), heart (lives), shield (weather shield, verified) | Home, LessonsHub, Summit, Profile | Gem, heart, flame, boot art as files |
| Summit/celebration effects | CSS confetti rectangles, `repeating-conic-gradient` sunburst, drop-shadow rings | Summit, Onb5Companion, Spot5Submitted, MafEnd, LevelUp | Lottie/animation assets; the backpack drawn as inline SVG on LevelUp |
| Splash mountains | Inline SVG polygons behind the mascot | Splash | Splash illustration |
| Onboarding interest tiles | Coloured circles + glyphs (peak, cave, lake, camp, trail) | Onb4Interests | none required if icon set exists |
| Gear rental items | Inline SVG tent, sleeping bag, crampons on tinted tiles | Gear | Product photos for gear and operators |
| QR code | Hand-drawn static SVG modules | CampLobby | Real generated QR (runtime) |
| Role / game icons | Inline glyphs: imposter mask, mafia hat/crown/moon, detective glass, doctor cross, heart, shield; game tiles | CampHub, CampLobby, Imp*, Maf*, WhoAmI, WYR | Role card art for all Mafia roles ("More roles: Sniper, Journalist, Immortal..."), Who am I? character images (Amir Temur, Navoi, Ulugh Beg, Plov...), would-you-rather pack art |
| Charts | Elevation profile on TrailMap and Operator dashboard bars are inline SVG/CSS | TrailMap, OperatorDash | Real charts (runtime) |
| Feed/Top Shots podium | CSS ranks, medal glyphs | TopShots, TopShotWin | Winners' wall art |
| Weather and hazard icons | Inline sun, cloud, storm, wind glyphs | Home, Place | Weather icon set |
