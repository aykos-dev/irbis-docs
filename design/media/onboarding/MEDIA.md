# Media — onboarding

Owner (2026-10-17): canvas SVGs are final; backpack + native splash ship as placeholders; motion is Lottie
(`lottie-react-native`, new package approved by choosing Lottie).

| File | What | Used on | Format / size | Status |
|---|---|---|---|---|
| canvas asset `9ebec15f…` (`irbisDefault.ts` in app) | Irbis default | Splash, Onb2, Onb3 | SVG | exists · final |
| canvas asset `28945aeb…` (`irbisExcited.ts`) | Irbis excited / waving | Onb1, Onb4 | SVG | exists · final |
| `Splash.dc.html` inline SVG | Splash mountains behind the mascot | Splash | inline SVG | exists on canvas · final · export to app |
| canvas asset `6bbbc6ee…` | Trail illustration | Onb3 tile Beginner | SVG 64×64 | exists on canvas · final · export |
| canvas asset `2ea0b851…` | Lake illustration | Onb3 tile Weekend hiker | SVG 64×64 | exists on canvas · final · export |
| canvas asset `3bcf1e06…` | Peak illustration | Onb3 tile Experienced | SVG 64×64 | exists on canvas · final · export |
| `Onb4Interests.dc.html` inline SVG | 5 interest glyphs (peak, cave, lake, camp, trail) on coloured circles | Onb4 | inline SVG | exists on canvas · final · export |
| canvas asset `beeba664…` | Panda cub — cheering pose | Onb5 | SVG | exists on canvas · final · export |
| canvas assets `d4c16d0e…` `d1b0d619…`(fox, in app) `dba7b962…` `ffe22771…` `55d73e65…` `09bfc86c…` | Companions L2–L7 silhouettes | Onb5 | SVG 40×40, tinted black | exists on canvas · final · export |
| backpack | Orange backpack | Onb5 | SVG | needed · placeholder (simple orange SVG) |
| native launch splash | Static splash before JS loads | cold start | Android XML/PNG, iOS storyboard | needed · placeholder (teal bg + Irbis) |
| `irbis-wave.json` | Irbis waves (2 s loop) + blinks every 4 s | Onb1 | Lottie | needed |
| `irbis-nod.json` | Irbis nods on language tap | Onb2 | Lottie | needed |
| `irbis-clap.json` | Irbis claps in the corner | Onb5 | Lottie | needed |
| `onb5-reveal.json` | Backpack shakes 3×, pops open with confetti (0.8 s), panda tumbles out and waves | Onb5 | Lottie | needed |
