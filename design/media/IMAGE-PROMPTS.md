# Image prompts — art the app ships as basic-shape placeholders

Written 2026-10-18 for the owner. Generate, then drop files in the feature folder named in each row; the next
feature run swaps them in. Colours are the tokens in `design/design.md`.

## Shared style block (paste before every prompt)
> Flat vector illustration for a friendly, Duolingo-style outdoor app set in the mountains of Uzbekistan.
> Bold simple shapes with rounded corners, no outlines, no gradients, no texture, no text, no people.
> 2–3 shades per colour for light and shadow. Calm, cheerful, clean. Wide 16:10 landscape, full-bleed
> background, main subject centred, nothing important within 8% of the edges.

Delivery: SVG preferred (flat shapes); else PNG 1170×720 (3× of 390×240). One file per image.

## A. Place heroes — `design/media/places/` (Place screen hero, Explore card thumbnail)
Status: waterfall, canyon, camping are placeholders; peak, lake, cave, trail are the canvas SVGs (accepted as
final, regenerate only if you want the whole set to match).

| File | Main colour | Prompt (after the style block) |
|---|---|---|
| `hero-waterfall.svg` | sky-teal `#2BA3C4` | A tall narrow waterfall dropping from a rocky cliff into a small round pool, white water ribbons, mist puffs at the bottom, juniper bushes on the rocks, layered teal-blue mountains behind, pale blue sky `#E6F6FA`. |
| `hero-canyon.svg` | terracotta `#D9733F` | A deep narrow canyon with tall layered red-orange rock walls, a thin turquoise river winding along the floor, a strip of sky between the walls, small green shrubs on ledges, background tint `#FCEDE4`. |
| `hero-camping.svg` | pine `#3DAA5C` | A small orange tent beside a campfire on a grassy shore, a calm lake and pine-green hills behind, dusk sky with two stars, background tint `#E4F5E7`. |
| `hero-peak.svg` | teal `#1CB0A8` | A single snow-capped summit with a small flag on top, two lower ridges in front, teal and deep-teal slopes, pale sky `#E3F7F5`. |
| `hero-lake.svg` | sky `#4CA9FF` | A calm alpine lake between two mountain slopes, reflection of the peaks in the water, a few rocks on the shore, background `#E7F3FF`. |
| `hero-cave.svg` | purple `#7B61FF` | A rounded cave entrance in a purple rock hill, dark inside with a hint of glowing teal crystals, small rocks at the mouth, background `#ECE7FF`. |
| `hero-trail.svg` | orange `#FF9F1C` | A dirt hiking path zig-zagging up a green hillside toward mountains, a wooden trail marker post, background `#FFF1DA`. |

Example (full prompt, waterfall): *Flat vector illustration for a friendly, Duolingo-style outdoor app set in the
mountains of Uzbekistan. Bold simple shapes with rounded corners, no outlines, no gradients, no texture, no text, no
people. 2–3 shades per colour for light and shadow. Calm, cheerful, clean. Wide 16:10 landscape, full-bleed
background, main subject centred, nothing important within 8% of the edges. A tall narrow waterfall dropping from a
rocky cliff into a small round pool, white water ribbons, mist puffs at the bottom, juniper bushes on the rocks,
layered teal-blue mountains behind, pale blue sky #E6F6FA.*

## B. Place-type icons — `design/media/places/` (Explore pins, filter chips, type pill)
Status: waterfall, canyon placeholders. Best drawn by hand in a vector tool on a 24×24 grid; prompt for a draft.

Icon style block: *Single minimal glyph icon, 24×24 grid, solid white shape on a transparent background, 2 px
rounded strokes or solid fills, no detail smaller than 2 px, must read at 16 px, same weight as a peak / lake / cave
icon set.*

| File | Prompt |
|---|---|
| `icon-waterfall.svg` | A cliff edge on the left with three vertical wavy water lines falling into a small splash. |
| `icon-canyon.svg` | Two tall rock walls facing each other with a thin winding river line between them. |

Also send the final hex colour for each (placeholders now: waterfall `#2BA3C4`, canyon `#D9733F`) so it goes into
`design/design.md`. Map pin PNGs are exported from these icons — no separate art needed.

## C. Onboarding — `design/media/onboarding/`
| File | Status | Prompt (after the style block, but square 1:1, transparent background, no scenery) |
|---|---|---|
| `backpack.svg` | placeholder | A small chunky orange backpack (`#FF9F1C`, shadow `#CC7A00`) with a rounded flap, one front pocket, two short straps and a tiny teal zipper pull, slight 3/4 view, cute proportions. |
| `launch-splash.png` | teal only | Native launch screen: the existing Irbis mascot (canvas asset `9ebec15f…`) centred on solid teal `#1CB0A8` — no prompt needed; export at 1242×2688 and an Android 9-patch, or send the mascot file and we build it. |

Animations (`irbis-wave`, `irbis-nod`, `irbis-clap`, `onb5-reveal`) are Lottie files from an animator, not image
prompts. If you want stills to brief the animator, use the mascot prompt below with the pose named.

Mascot pose prompt (only for animator reference): *Chibi snow-leopard cub "Irbis" with a big round head, soft grey
fur with dark rosettes, pale belly, big friendly eyes, tiny orange backpack, flat vector, no outlines, transparent
background, full body, pose: <waving one paw | nodding with eyes closed | clapping both paws>.*
