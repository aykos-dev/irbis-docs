# Brief lessons-admin-5-irbis-web — lesson editor

- Spec: features/lessons-admin.md · ACs in this slice: AC7
- Repo / branch: irbis-web · `feat/lessons-admin`
- Depends on: brief lessons-admin-4-irbis-web (pages, icons, i18n namespace)

## Files
- Touch: `src/app/(admin)/lessons/[tierId]/[lessonId]/page.tsx` · `src/features/lessons-admin/` (editor components,
  form schema, hooks) · `src/shared/i18n/messages/{en,ru,uz}.json` (`lessonsAdmin.editor.*`) · `next.config.ts`
  only if needed to show the image URL host (prefer plain `<img>` for admin previews)
- Read for patterns: `src/features/conditions/components/override-section.tsx`, `write-errors.ts`, `schemas.ts`,
  `src/features/lessons-admin/*` from slice 4

## Behaviour (AC7)
- Loads `GET /v1/admin/lessons/{id}`; header: back to tier, title (UI locale), status badge.
- Title uz/ru/en + icon picker. Questions list (max 15; "Add question" disabled at 15): each card numbered, with
  prompt, hint, options (2–4: add / remove option; radio "Correct"), explanation, wrong-answer explanation — each an
  input group with three labelled fields uz / ru / en and a small "missing" dot per blank locale. Remove question
  (confirm), move up / down.
- Image per question: file input (accept jpeg/png/webp) → `POST /v1/admin/lesson-images` (multipart) → preview from
  `url`; Remove clears it; 415 / 413 shown inline under the input ("Use JPEG, PNG or WebP" / "Max 2 MB").
- Save draft → `PUT` whole lesson. Publish → save first if dirty, then `POST publish`. Unpublish. Delete (draft only,
  confirm) → back to tier page.
- Server `fieldErrors` (paths like `questions.3.options.1.ru`, `title.uz`) map to the exact input (red border +
  message) and a counter "N fields missing to publish" (`lessonsAdmin.editor.missingCount`, plural-aware).
- Unsaved changes: browser beforeunload + in-app navigation confirm.
- States: skeleton, error + retry, saving disables buttons, toast on success.

## Copy (lessonsAdmin.editor)
| key | en | ru | uz |
|---|---|---|---|
| saveDraft | Save draft | Сохранить черновик | Qoralamani saqlash |
| publish | Publish | Опубликовать | Eʼlon qilish |
| unpublish | Unpublish | Снять с публикации | Eʼlondan olish |
| addQuestion | Add question | Добавить вопрос | Savol qoʻshish |
| correct | Correct | Верный | Toʻgʻri |
| missingCount | {count} fields missing to publish | Для публикации не заполнено полей: {count} | Eʼlon qilish uchun {count} ta maydon toʻldirilmagan |
| unsaved | You have unsaved changes. Leave anyway? | Есть несохранённые изменения. Всё равно уйти? | Saqlanmagan oʻzgarishlar bor. Baribir chiqasizmi? |
| imageType | Use JPEG, PNG or WebP | Используйте JPEG, PNG или WebP | JPEG, PNG yoki WebP dan foydalaning |
| imageSize | Max 2 MB | Максимум 2 МБ | Koʻpi bilan 2 MB |
Field labels (Prompt, Hint, Options, Explanation, Wrong-answer explanation, Image, Remove) — en/ru/uz in the same style.

## testIDs
`lessons.editor`, `lessons.editor.title.<uz|ru|en>`, `lessons.editor.icon`, `lessons.editor.q.<n>`,
`lessons.editor.q.<n>.correct.<i>`, `lessons.editor.q.<n>.image`, `lessons.editor.add-question`, `lessons.editor.save`,
`lessons.editor.publish`, `lessons.editor.unpublish`, `lessons.editor.delete`, `lessons.editor.missing-count`

## Approved packages
none

## Done when
- [ ] 2–3 Vitest tests (fieldErrors map to inputs + count; add/remove/limit 15; correct radio), `npm run check` green (paste), committed
- [ ] reply ≤10 lines
