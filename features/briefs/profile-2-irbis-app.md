# Brief profile-2-irbis-app — EditProfile and avatar picker

- Spec: features/profile.md · ACs in this slice: AC3, AC5
- Repo / branch: irbis-app · `feat/profile`
- Depends on: profile-1-irbis-app (profile route/placeholders) + profile-1/2/3-irbis-api on the branch

## Files
- Touch: `src/features/profile/screens/EditProfileScreen.tsx` (new), `components/RegionSheet.tsx`,
  `components/CurrentPasswordSheet.tsx`, `components/AvatarPicker.tsx`, `src/app/navigation/types.ts`
  (`EditProfile: undefined`), `RootNavigator.tsx`, `src/shared/i18n/{en,ru,uz}/profile.json`, tests ·
  `ios/Irbis/Info.plist` (`NSPhotoLibraryUsageDescription`)
- Read for patterns: `src/features/onboarding/screens/InterestsScreen.tsx` (interest chips),
  `src/features/auth/screens/RecoveryPhoneScreen.tsx` (wizard + sheet), `src/shared/components/Sheet.tsx`,
  `TextField`, `AppButton`, `ListRow`, `Screen`, `Toast`, `useAuth().setUser`, `useMeUpdate`,
  `useMeUploadAvatar`, `useMeDeleteAvatar`, `getMeGetQueryKey`, `src/shared/utils/qaLog`.
- Reuse `profile.regions.<enum>` labels from profile-1. Do not add Photography.

## Behaviour
- AC5 — Screen `EditProfile` with a back/cancel header. Initial values from `useAuth().user`. Fields:
  Name (`displayName`, optional, 2–40 after trim, empty clears); Username (read-only text + “Change” action, or
  editable field); Bio (`bio`, optional ≤150, live `n / 150`); Home region (opens a sheet with the 15 enum values,
  “Not set” clears); I love (five chips: peaks, caves, lakes, camping, trails; 0–5 selected); “Show stats on my
  profile” (default on); “Show my home region” (default off; disabled with “Set a home region first” when none is
  selected, and forced off when the region is cleared). “Backpack colour” is a disabled row with “Coming with
  companion styles”.
- Avatar: show `user.avatarUrl` or initials in a 96 px circle; “Change photo” calls
  `launchImageLibrary({ mediaType: 'photo', selectionLimit: 1, quality: 1 })` — gallery only, no camera, no crop.
  Stage the local `uri`; show “Remove photo” when a photo exists/staged. On Save upload via
  `useMeUploadAvatar` (FormData `file` from `{ uri, type, name }`) or call `useMeDeleteAvatar` when removed. Do not
  touch the network on Cancel. Permission denied, >2 MB, wrong type and upload failure show the exact copy below.
- AC5 save — validate locally; if the username changed, open `CurrentPasswordSheet` before saving (copy below).
  PATCH `displayName`, `bio`, `homeRegion`, `interests`, `preferences.showStats`,
  `preferences.showHomeRegion`; add `username` + `currentPassword` only when the username changed. Use the
  generated `useMeUpdate`; on success `setUser(response)`, toast `edit.saved` (and `edit.usernameChanged` when
  relevant), `qaLog('profile_edit_saved', { fields })`, then `navigation.goBack()`. On failure keep the screen
  open, show inline/field errors and a retry path. Save is disabled while pending. Cancel with unsaved changes asks
  “Discard changes?”.
- Username rules and errors come from the API (`USERNAME_INVALID`, `USERNAME_RESERVED`, `USERNAME_TAKEN`,
  `INVALID_PASSWORD`); map them to the field/sheet, never show the raw server message. The password sheet says
  other devices will be signed out.
- Light/dark via tokens; keyboard-aware `Screen`; long ru/uz labels wrap; 44 px targets; every switch has a role
  and value; avatar picker announces “Profile photo”.

## API (generated hooks)
`useMeUpdate` · `useMeUploadAvatar` · `useMeDeleteAvatar` · `useAuth().setUser` · `getMeGetQueryKey`.

## Copy (`profile.json`; en / ru / uz)
| key | en | ru | uz |
|---|---|---|---|
| `edit.title` | `Edit profile` | `Редактировать профиль` | `Profilni tahrirlash` |
| `edit.name` / `edit.namePlaceholder` | `Name` / `Your name` | `Имя` / `Ваше имя` | `Ism` / `Ismingiz` |
| `edit.username` / `edit.change` | `Username` / `Change` | `Имя пользователя` / `Изменить` | `Foydalanuvchi nomi` / `O‘zgartirish` |
| `edit.bio` / `edit.bioPlaceholder` / `edit.bioCount` | `Bio` / `A line about you` / `%{n} / 150` | `О себе` / `Пара слов о себе` / `%{n} / 150` | `O‘zim haqimda` / `O‘zingiz haqingizda bir og‘iz` / `%{n} / 150` |
| `edit.homeRegion` / `edit.notSet` / `edit.regionTitle` | `Home region` / `Not set` / `Choose your region` | `Домашний регион` / `Не выбран` / `Выберите регион` | `Uy hududi` / `Tanlanmagan` / `Hududingizni tanlang` |
| `edit.interests` / `edit.interestsNote` | `I love` / `Pick up to 5.` | `Мне нравится` / `Выберите до 5.` | `Menga yoqadi` / `5 tagacha tanlang.` |
| `edit.showStats` / `edit.showStatsNote` | `Show stats on my profile` / `Others see your peaks, lakes and distance.` | `Показывать статистику в профиле` / `Другие видят ваши вершины, озёра и расстояние.` | `Profilda statistikani ko‘rsatish` / `Boshqalar cho‘qqilar, ko‘llar va masofani ko‘radi.` |
| `edit.showHomeRegion` / `edit.showHomeRegionNote` / `edit.regionFirst` | `Show my home region` / `Appears under your username.` / `Set a home region first.` | `Показывать домашний регион` / `Показывается под именем пользователя.` / `Сначала выберите регион.` | `Uy hududini ko‘rsatish` / `Foydalanuvchi nomi ostida ko‘rinadi.` / `Avval hududni tanlang.` |
| `edit.changePhoto` / `edit.removePhoto` / `edit.avatar` | `Change photo` / `Remove photo` / `Profile photo` | `Изменить фото` / `Удалить фото` / `Фото профиля` | `Rasmni o‘zgartirish` / `Rasmni o‘chirish` / `Profil rasmi` |
| `edit.backpack` / `edit.backpackSoon` | `Backpack colour` / `Coming with companion styles` | `Цвет рюкзака` / `Появится со стилями компаньона` | `Ryukzak rangi` / `Hamroh uslublari bilan keladi` |
| `edit.save` / `edit.cancel` / `edit.saved` / `edit.error` | `Save` / `Cancel` / `Profile saved` / `Couldn’t save. Try again.` | `Сохранить` / `Отмена` / `Профиль сохранён` / `Не удалось сохранить. Попробуйте ещё раз.` | `Saqlash` / `Bekor qilish` / `Profil saqlandi` / `Saqlab bo‘lmadi. Qayta urinib ko‘ring.` |
| `edit.nameError` / `edit.bioError` / `edit.usernameError` | `2–40 characters.` / `150 characters max.` / `3–20 characters: a–z, 0–9, . or _.` | `2–40 символов.` / `Не больше 150 символов.` / `3–20 символов: a–z, 0–9, . или _.` | `2–40 belgi.` / `Ko‘pi bilan 150 belgi.` / `3–20 belgi: a–z, 0–9, . yoki _.` |
| `edit.taken` / `edit.reserved` | `That username is taken.` / `That username is reserved.` | `Это имя уже занято.` / `Это имя зарезервировано.` | `Bu nom band.` / `Bu nom band qilingan.` |
| `edit.photoPermission` / `edit.photoTooLarge` / `edit.photoType` / `edit.photoFailed` | `Allow photo access in Settings to choose a profile photo.` / `Choose a photo under 2 MB.` / `Choose a JPEG, PNG or WebP photo.` / `Couldn’t upload the photo. Try again.` | `Разрешите доступ к фото в настройках, чтобы выбрать фото.` / `Выберите фото до 2 МБ.` / `Выберите фото JPEG, PNG или WebP.` / `Не удалось загрузить фото. Попробуйте ещё раз.` | `Profil rasmini tanlash uchun sozlamalarda rasmga ruxsat bering.` / `2 MBdan kichik rasm tanlang.` / `JPEG, PNG yoki WebP rasm tanlang.` / `Rasmni yuklab bo‘lmadi. Qayta urinib ko‘ring.` |
| `edit.passwordTitle` / `edit.passwordBody` / `edit.password` / `edit.confirm` / `edit.passwordWrong` / `edit.passwordRequired` / `edit.usernameChanged` | `Confirm your password` / `Changing your username signs out your other devices.` / `Current password` / `Confirm` / `Wrong password.` / `Enter your password.` / `Username changed. Other devices were signed out.` | `Подтвердите пароль` / `При смене имени вы выйдете на других устройствах.` / `Текущий пароль` / `Подтвердить` / `Неверный пароль.` / `Введите пароль.` / `Имя изменено. Другие устройства вышли.` | `Parolni tasdiqlang` / `Foydalanuvchi nomini o‘zgartirsangiz, boshqa qurilmalardan chiqasiz.` / `Joriy parol` / `Tasdiqlash` / `Parol noto‘g‘ri.` / `Parolni kiriting.` / `Nom o‘zgartirildi. Boshqa qurilmalar chiqdi.` |
| `edit.discardTitle` / `edit.discard` / `edit.keepEditing` | `Discard changes?` / `Discard` / `Keep editing` | `Отменить изменения?` / `Отменить` / `Продолжить` | `O‘zgarishlarni bekor qilasizmi?` / `Bekor qilish` / `Tahrirlashda davom etish` |

## testIDs · QA events
`edit-profile.name`, `edit-profile.username`, `edit-profile.bio`, `edit-profile.bio-count`,
`edit-profile.home-region`, `edit-profile.region-{enum}`, `edit-profile.interest-{peaks|caves|lakes|camping|trails}`,
`edit-profile.show-stats`, `edit-profile.show-home-region`, `edit-profile.change-photo`,
`edit-profile.remove-photo`, `edit-profile.backpack-colour`, `edit-profile.save`, `edit-profile.cancel`,
`edit-profile.error`, `edit-profile.password`, `edit-profile.password-confirm` ·
`profile_edit_saved { fields }`, `username_changed`, `avatar_uploaded { sizeBucket }`, `avatar_removed`.

## Approved packages
`react-native-image-picker@8.3.0` (gallery only; no camera/crop package). Add only
`NSPhotoLibraryUsageDescription` = “Irbis uses your photo library to choose a profile photo.”

## Done when
- [ ] tests: validation limits; region clears show-region; interests max 5; staged photo upload/remove on Save;
  Cancel makes no request; username change opens password sheet, wrong password stays, success updates user and
  signs out others; permission/too-large/type errors
- [ ] `npm run check` green (output in summary) · committed on `feat/profile`
