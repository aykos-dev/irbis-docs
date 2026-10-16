# Irbis — Design tokens (source of truth)

Mirrored verbatim by:
- `irbis-app/src/shared/constants/{colors,typography,spacing}.ts`
- `irbis-web/src/shared/styles/tokens.css`

New visual values are added **here first**, then mirrored in the same change. All colour pairings
must meet WCAG AA. Values are TBD until design lands — names are fixed now so code can reference them.

## Colour roles (light / dark)
| Token | Light | Dark | Use |
|---|---|---|---|
| `surface` | TBD | TBD | screen background |
| `surface-raised` | TBD | TBD | cards, sheets |
| `on-surface` | TBD | TBD | primary text |
| `on-surface-muted` | TBD | TBD | secondary text, placeholders |
| `border` | TBD | TBD | inputs, dividers |
| `primary` / `on-primary` | TBD | TBD | primary actions |
| `success` / `warning` / `error` / `info` | TBD | TBD | states, toasts, field validation |
| `focus-ring` | TBD | TBD | web focus outline |

## Typography
Family: TBD (Regular / Medium / Bold files). Sizes with line height and `maxFontSizeMultiplier` (app):
`display`, `title-lg`, `title`, `body-lg`, `body`, `body-sm`, `body-xs`, `label`.

## Spacing
Scale: `0, 50 (2), 100 (4), 150 (6), 200 (8), 300 (12), 400 (16), 500 (20), 600 (24), 800 (32), 1000 (40)` — values in px/pt.

## Radii
`none, sm, md, lg, xl, full` — TBD.

## Elevation
`0–3`, each defined as iOS shadow (color, opacity, radius, offset) + Android `elevation` + web `box-shadow`.

## Motion
`press 150ms`, `enter 200–250ms`, `layout 300ms`; easing out-cubic (enter), in-cubic (exit).
