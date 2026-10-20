# Brief weekly-path-4-irbis-app — smart swap card, done nodes, chest open, debug visit link

- Spec: features/weekly-path.md · ACs in this slice: AC3, AC4, AC5
- Repo / branch: irbis-app · `feat/weekly-path`
- Depends on: weekly-path-2-irbis-api + weekly-path-3-irbis-app (run `npm run gen:api` first)

## Files
- Touch: `src/features/weekly-path/` (components SwapCard, ChestNode (interactive), PathNode done state,
  `swapDismissStore.ts`, `__tests__/`) · `src/features/debug/` (new `pathVisitLink.ts` + hook, like `grantLink.ts`)
  · `src/app/navigation/linking.ts` (debug link, dev/staging only) · `src/shared/i18n/{en,ru,uz}/path.json` ·
  `src/shared/api/generated/` (gen:api only).
- Read for patterns (don't change): `../irbis-docs/design/media/weekly-path/LAYOUT.md` (swap card, gold node, chest
  SVG), `src/features/debug/grantLink.ts` + `hooks/useGrantLink.ts`, `src/shared/hooks/useRequireAccount.ts`
  (log-in prompt), `src/features/lessons/screens/LessonCompleteScreen.tsx` (award result, level-up hand-off),
  `src/shared/components/Motion.tsx`, `Toast.tsx`.

## Behaviour
- AC3 — A not_now node with `swap` != null shows SwapCard under it, unless dismissed:
  - Title `path.swap.title`.
  - Body `path.swap.body`, where `{elev}` is signed ("+1,100" / "−200") and `{day}` is the localized day.
  - Buttons: "See place" → `navigate('Place', { id: swap.place.id })`, and "Keep plan" → store
    `{month}:{position}` in `swapDismissStore` (MMKV, reset when the month changes) and hide the card.
  - QA: `path_swap_shown { position }` when it renders, `path_swap_kept { position }`.
  - `swap == null` → no card.
- AC4 — A `done` node renders gold with a star (LAYOUT.md) and the chip `path.done`.
  - When a node flips from not-done to done between two responses on screen, play the coin shower (Reanimated
    placeholder, ≤1.2 s) and a success haptic.
  - Debug link `irbis://debug/path/visit/<placeId>` (dev/staging only) calls the generated QA visit mutation,
    updates the `usePathGet` cache with the response, and logs `path_visit_debug { placeId }`. Error → Toast.
- AC5 — ChestNode shows `chest.done / chest.required`.
  - Guest tap → `useRequireAccount` prompt (reason `path.chest.loginReason`).
  - `done < required` → a shake + `path.chest.locked` toast.
  - `done === required && !opened` → `usePathOpenChest`: lid-open animation (placeholder: lid tilt + sparkle,
    Reanimated), toast `path.chest.reward` with xp, heavy haptic, invalidate path + my-level queries, and
    `path_chest_opened { month, xp }`. If `levelUps` is non-empty, hand off to LevelUp the same way
    LessonCompleteScreen does.
  - `opened` → the open chest + `path.chest.opened`.
  - Errors: 409 → refetch + locked toast. Others → `errors` toast.

## API
| Method | Path | Request | Response | Errors (code → status) |
|---|---|---|---|---|
| POST | `/v1/path/chest/open` | — | `{ opened, xp, levelUps }` | `PATH_CHEST_LOCKED` 409, `PATH_NOT_FOUND` 404 |
| POST | `/v1/qa/path/visits` | `{ placeId }` | `PathDto` | `PLACE_NOT_ON_PATH` 404 |

## Copy (namespace `path`)
| key | en | ru | uz |
|---|---|---|---|
| swap.title | Try %{name} instead | Попробуйте %{name} | Buning o'rniga %{name} |
| swap.body | %{elev} m, %{km} km from %{original}, clear skies on %{day}. | %{elev} м, %{km} км от %{original}, ясно в %{day}. | %{elev} m, %{original}dan %{km} km, %{day} kuni ochiq havo. |
| swap.see | See place | Посмотреть место | Joyni ko'rish |
| swap.keep | Keep plan | Оставить план | Rejani qoldirish |
| swap.badge | Smart swap | Умная замена | Aqlli almashtirish |
| done | Done | Готово | Bajarildi |
| chest.locked | Check in at all %{required} places to open it | Отметьтесь во всех %{required} местах, чтобы открыть | Ochish uchun barcha %{required} joyda belgilaning |
| chest.reward | Chest opened! +%{xp} XP | Сундук открыт! +%{xp} XP | Sandiq ochildi! +%{xp} XP |
| chest.opened | Opened this month | Открыт в этом месяце | Bu oy ochilgan |
| chest.loginReason | Keep your chest XP | Сохраните XP из сундука | Sandiq XP'ingizni saqlang |

## testIDs · QA events
`path.swap.card` `path.swap.see` `path.swap.keep` `path.chest` `path.node.<n>.done` · `path_swap_shown`
`path_swap_kept` `path_chest_opened` `path_visit_debug`

## Approved packages
none

## Done when
- [ ] Tests: swap card shows / See navigates / Keep hides and persists across remount. Done node renders gold.
  Chest: guest → prompt, locked → toast, 3/3 → mutation + reward toast. Debug link parses and calls the mutation.
- [ ] `npm run check` green, committed on the branch
