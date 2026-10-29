# Brief check-in-4-irbis-app — guest check-ins → demo account, Secure your account

- Spec: features/check-in.md · ACs: AC6, AC8 · ADR: decisions/ADR-006-demo-accounts.md
- Repo / branch: irbis-app · `feat/check-in` (stacks on brief 3; same rule about the owner's uncommitted files)
- Depends on: check-in-3-irbis-app, check-in-2-irbis-api

## Files
- Touch: `src/features/check-in/` (queue sync) · `src/shared/contexts/auth.tsx` (+ guest merge hook-in) ·
  `src/features/auth/screens/ProfileScreen.tsx` (demo card, sign-out confirm) · new `SecureAccountScreen` in
  `src/features/auth/` · navigation route · i18n `auth.secure.*`, `checkin.demo.*`
- Read for patterns: auth sign-up flow (token storage via tokenManager, `onMerged` / `notifySignInSettled`, guest
  merge), log-in prompt sheet, sign-up form validation + keyboard rules (`docs/engineering-standards.md` keyboard)

## Behaviour
- AC6 — Guests: Check in does NOT open the log-in prompt; a passing fix is queued exactly as offline (Summit opens
  queued). Sync, when the queue is non-empty and the user is a guest and online: `POST /v1/auth/demo { locale }` →
  store the session exactly like a sign-up (same code path), run the existing guest merge, then send the queue.
  Toast "Your progress is saved as {username}". 429 DEMO_LIMIT/RATE_LIMITED → keep the queue, retry next trigger.
  Never create two demo accounts concurrently (single-flight). QA event `demo_account_created {}`.
- AC8 — `me.isDemo`: account Profile shows the username and `profile.secure-card` "Secure your account — set a
  username and password so you can log in on any phone." → SecureAccountScreen: `secure.username` (prefilled with
  the demo username, editable), `secure.password`, `secure.confirm`, `secure.terms` (same terms checkbox + link as sign-up, owner 2026-10-29), `secure.submit` → `useMeSecure` with `acceptTerms`; 400 TERMS_REQUIRED → same message as sign-up; 409
  USERNAME_TAKEN → field error; success → toast "Account secured", back, refresh me; QA `account_secured {}`.
  Sign out while isDemo → confirm sheet "You'll lose {username}'s progress unless you secure it." (Sign out /
  Secure account).
- ru/uz copy: natural text.

## Done when
- [ ] tests: guest check-in queued → online sync creates demo then sends; DEMO_LIMIT keeps queue; secure form
  success + USERNAME_TAKEN; demo sign-out asks first
- [ ] `npm run check` green; commits on `feat/check-in`, no push
