# Brief onboarding-2-irbis-app — flow shell, splash, Meet Irbis, Language

- Spec: features/onboarding.md · ACs in this slice: AC1, AC2, AC3
- Repo / branch: irbis-app · `feat/onboarding` (create from main if missing; slices stack on it)
- Depends on: none (api slice not needed here)

## Files
- Touch: `src/features/onboarding/` (new: navigator, screens Splash/Welcome/Language, `OnboardingHeader`,
  `onboardingStore.ts`) · `src/app/navigation/{RootNavigator,types,linking}.tsx|ts` · `src/shared/storage/index.ts`
  (keys) · `src/shared/i18n/{en,ru,uz}/onboarding.json` + register the namespace · move
  `src/features/auth/components/LanguageSheet.tsx` → `src/shared/components/` (features never import each other;
  update auth's imports, no other change) · new `src/shared/components/Motion.tsx` · native launch background.
- Read for patterns (don't change): `src/features/auth/screens/LogInScreen.tsx`, `src/features/auth/components/BackButton.tsx`,
  `src/shared/components/{Mascot,Screen,AppButton,Pressable,Icon}.tsx`, `src/shared/i18n/index.ts`,
  `src/shared/hooks/useLocale.ts`, `src/shared/utils/{haptics,qaLog}.ts`, `src/shared/contexts/auth.tsx`,
  `docs/architecture.md` (RootNavigator: Splash + Onboarding before MainTabs).

## Behaviour
- AC1 — RootNavigator initial route = `Onboarding` when storage `onboarding.done` is unset AND no signed-in session;
  otherwise `MainTabs` (signed-in at launch → set the flag). Onboarding stack: Splash → Welcome → Language →
  Experience → Interests → Companion. This slice builds only Splash/Welcome/Language (no empty stub screens);
  Continue on Language ends onboarding (`via: 'finish'`) until slice 3 points it at Experience. Splash: teal bg token, Irbis default 200 in
  a white-12% circle, wordmark `irbis`, tagline, 3 dots; 1500 ms then replace with Welcome. Ending onboarding (any
  way) = set `onboarding.done = '1'`, `reset` to MainTabs, `onboarding_end { via }`.
- AC2 — Welcome: bubble, Irbis excited 280 (Motion `irbis-wave`), title, body, `Get started` → Language,
  `I already have an account` → `navigate('Auth',{screen:'LogIn'})`. When the session becomes signed-in while
  onboarding is mounted → end with `via: 'login'`. Closing Log in returns to Welcome. Top-right chip: globe +
  current locale code upper-case, opens LanguageSheet; a pick calls `setLocale` (live).
- AC3 — `OnboardingHeader` for steps 2–4: back chevron (→ goBack; Android back same), progress bar + label
  "Step N of 4" (N = 1/2/3), ✕ (→ end, `via: 'close'`, no experience/interests saved). Language screen: radiogroup
  UZ/RU/EN rows (code badge, native title, subtitle), selected = `getLocale()`; tap → `setLocale` at once,
  selection haptic, Motion `irbis-nod`, `onboarding_language { locale }`. Continue always enabled.
- Motion.tsx: `<Motion name fallback />` renders `LottieView` when a source for `name` is registered in a typed
  map in the same file, else `fallback` (the static Mascot). No sources exist yet (owner Q13: placeholders); the map
  is the only place to add them. Respect reduced motion (no autoplay).
- Native launch placeholder: Android launch theme `windowBackground` and iOS LaunchScreen background = teal brand
  token (#0E8A83), no image. Owner Q10 placeholder.
- QA-only deep link (same gate as `irbis://debug/lang`): `irbis://debug/onboarding/reset` clears `onboarding.done`
  and restarts at Splash; `irbis://debug/onboarding/done` sets it.
- `onboarding_step { step }` on each screen focus.

## Copy (namespace `onboarding`; uz uses o‘ g‘ and ’ like existing uz files)
| key | en | ru | uz |
|---|---|---|---|
| splash.tagline | Explore. Learn. Come back safe. | Исследуй. Учись. Возвращайся невредимым. | Kashf et. O‘rgan. Eson-omon qayt. |
| welcome.bubble | Salom! I'm Irbis. I'll guide you to peaks, lakes and caves — and back home safely. | Салом! Я Ирбис. Проведу тебя к вершинам, озёрам и пещерам — и обратно домой целым. | Salom! Men Irbisman. Seni cho‘qqilar, ko‘llar va g‘orlarga boshlab boraman — va uyga eson-omon qaytaraman. |
| welcome.title | Explore Central Asia, one summit at a time | Открывай Центральную Азию — вершина за вершиной | Markaziy Osiyoni kashf et — cho‘qqima-cho‘qqi |
| welcome.body | Weekly paths built for your level, the season and the weather. | Маршруты на каждую неделю — под твой уровень, сезон и погоду. | Darajang, mavsum va ob-havoga mos haftalik yo‘nalishlar. |
| welcome.getStarted | Get started | Начать | Boshlash |
| welcome.haveAccount | I already have an account | У меня уже есть аккаунт | Menda allaqachon akkaunt bor |
| welcome.langChip (a11y) | Change language | Сменить язык | Tilni o‘zgartirish |
| header.back / header.close | Back / Close | Назад / Закрыть | Orqaga / Yopish |
| header.progress | Step %{n} of 4 | Шаг %{n} из 4 | %{n}-qadam, jami 4 |
| language.bubble | Which language should I speak? | На каком языке мне говорить? | Qaysi tilda gaplashay? |
| language.sub.uz / .ru / .en | Uzbek · Lotin yozuvi / Russian / English | Узбекский · Lotin yozuvi / Русский / Английский | O‘zbek tili · Lotin yozuvi / Rus tili / Ingliz tili |
| language.footnote | You can change this any time in Profile › Settings. Place names stay in their local spelling. | Язык можно сменить в любой момент: Профиль › Настройки. Названия мест остаются в местном написании. | Tilni istalgan vaqt Profil › Sozlamalar bo‘limida o‘zgartirish mumkin. Joy nomlari mahalliy yozilishida qoladi. |
| continue | Continue | Продолжить | Davom etish |
Row titles are fixed (not translated): `Oʻzbekcha`, `Русский`, `English`.

## testIDs · QA events
`onboarding.splash` `onboarding.welcome` `onboarding.get-started` `onboarding.have-account` `onboarding.lang-chip`
`onboarding.back` `onboarding.close` `onboarding.progress` `onboarding.lang-{uz|ru|en}` `onboarding.continue` ·
`onboarding_step { step }` `onboarding_language { locale }` `onboarding_end { via, experience?, interestsCount }`

## Approved packages
`lottie-react-native` — latest stable that supports RN 0.88 New Arch (check npm + its README; no Expo); pin exact.
Run `pod install` if the repo's iOS setup expects it; report the version.

## Done when
- [ ] tests for AC1–AC3 (1–3 each; navigator gate, end-onboarding sets flag, language tap persists), `npm run check`
  green, committed on `feat/onboarding`; reply ≤10 lines with commit hash + check tail
