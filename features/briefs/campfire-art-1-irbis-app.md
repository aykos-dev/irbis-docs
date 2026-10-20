# Brief campfire-art-1-irbis-app — swap campfire placeholders for the owner's art

- Spec: none (asset swap, owner 2026-10-20). Media lists: `design/media/campfire-{core,mafia,xo,crocodile}/MEDIA.md`
- Repo / branches (3, in this order; commit on each):
  1. `fix/campfire-art` — create from `main`: fox, hotspot guide, Mafia role glyphs ×3, Mafia role card art
  2. `feat/campfire-xo` (existing): XO tile glyph
  3. `feat/campfire-crocodile` (existing): Crocodile tile glyph
- Depends on: none

## Assets (ready to copy, already resized @1x/@2x/@3x and cleaned)
Source dir: `/private/tmp/claude-501/-Users-sardor-work-irbis-irbis-docs/da8c5938-5097-49ea-9d53-5711cb756cc4/scratchpad/camp-art/`
Copy into `src/assets/images/campfire/` (new dir), keep file names, all three densities.
- Branch 1: `foxCheering*.png` (84×84, transparent) · `iosHotspotGuide*.jpg` (342×180) ·
  `roleGlyph_{sniper,journalist,immortal}*.png` (40×40, **black glyph on transparent → tint with `tintColor`**) ·
  `roleCard_{boss,mafia,detective,doctor,maniac,lover,bodyguard,civilian,sniper,journalist,immortal}*.jpg` (144×192)
- Branch 2: `gameGlyph_xo*.png` (26×26, black, tint white) · Branch 3: `gameGlyph_croc*.png` (26×26, black, tint white)
Copy only the files for that branch. Pattern: `src/assets/images/pins/index.ts` (+ `src/assets/images.d.ts`).

## Files
- Branch 1 touch: `src/assets/images/campfire/index.ts` (new: export `foxCheering`, `iosHotspotGuide`,
  `roleGlyphImages` {sniper, journalist, immortal}, `roleCards` Record<RoleId, ImageRequireSource>) ·
  `src/features/campfire-core/screens/CampHubScreen.tsx` · `components/IosHotspotGuide.tsx` ·
  `games/mafia/RoleGlyph.tsx` · `games/mafia/RoleCard.tsx` · `campTheme.ts` (sizes only)
- Branch 2 touch: `games/xo/XoGlyph.tsx` · Branch 3 touch: `games/croc/CrocGlyph.tsx`
  (import the PNG directly in the glyph file — no shared index on these branches, avoids merge conflicts)
- Read for patterns: `src/assets/images/pins/index.ts`, `games/mafia/roles.ts`

## Behaviour
- CampHub hero: `foxCheering` PNG replaces `companionFoxSvg` (same `campSizes.heroArt` box); panda stays.
  Remove the now-unused `companionFoxSvg` import from this file only (the SVG file stays, used elsewhere).
- iPhone host guide: picture above the numbered text steps (steps stay), full sheet width,
  `aspectRatio: 342 / 180`, `radii.card` corners, hidden from accessibility (text steps carry the meaning).
- `RoleGlyph`: sniper / journalist / immortal render `<Image source tintColor={color} />` at `size`×`size`;
  the 8 canvas SVG paths stay; delete the 3 placeholder paths (crosshair, notepad, infinity) and update the doc comment.
- `RoleCard`: the coloured tile + glyph under "You are" becomes the role's card art (144×192 via new
  `mafiaSizes.cardArtWidth/cardArtHeight`, `radii.tile`, hidden from accessibility). Role name, team line and texts
  unchanged. Setup rows, host list, out list, game over keep the glyph tiles.
- XO / Croc tiles: `XoGlyph` / `CrocGlyph` render the PNG tinted white at their current size (keep the
  component name and props, so `GameTile` is untouched).
- No other UI or copy changes. No new packages.

## testIDs
Keep existing. Add `maf.card.art` on the role card image.

## Done when
- [ ] each branch: 1–2 tests (role card shows art for a role; RoleGlyph renders an image for sniper; xo/croc glyph renders),
      no existing test edited (if one must change, stop and report), `npm run check` green, committed
- [ ] summary lists the 3 commits and pastes each branch's check output tail
