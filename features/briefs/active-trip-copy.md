# active-trip — copy

App: i18n namespace `active`, file `src/shared/i18n/<lang>/active.json`. Web: next-intl namespace `live`.
API SMS: key `sms.sos` next to trip-plan's `sms.*`. Taken from the ActiveTrip board; ru/uz are Claude drafts (owner
review). `{x}` = interpolation.

## App (`active.*`)
| Key | en | ru | uz |
|---|---|---|---|
| title | Active trip | Активный поход | Faol sayohat |
| status.onTrack | LIVE · On track | В ПУТИ · Всё по плану | JONLI · Reja bo'yicha |
| status.late | LIVE · Running late | В ПУТИ · Опаздываете | JONLI · Kechikyapsiz |
| status.alerted | Contact alerted | Контакт оповещён | Kontaktga xabar yuborildi |
| backBy | Back by {time} | Вернуться к {time} | {time} gacha qaytish |
| stat.km | km | км | km |
| stat.climb | m climbed | м набора | m ko'tarilish |
| stat.elapsed | elapsed | в пути | o'tdi |
| stat.none | — | — | — |
| findingYou | Finding you… | Ищем вас… | Joylashuvingiz aniqlanmoqda… |
| locationOff | Turn on location to track your route | Включите геолокацию, чтобы записывать маршрут | Yo'nalishni yozish uchun joylashuvni yoqing |
| locationOffCta | Open Settings | Открыть настройки | Sozlamalarni ochish |
| contact.following | {name} is following · last location sent {min} min ago | {name} следит · место отправлено {min} мин назад | {name} kuzatmoqda · joylashuv {min} daq oldin yuborildi |
| contact.justNow | {name} is following · last location sent just now | {name} следит · место отправлено только что | {name} kuzatmoqda · joylashuv hozirgina yuborildi |
| contact.notYet | {name} is following · location not sent yet | {name} следит · место ещё не отправлено | {name} kuzatmoqda · joylashuv hali yuborilmadi |
| shareLive | Share live link | Поделиться ссылкой | Jonli havolani ulashish |
| shareText | Follow my trip to {place}, back by {time}: {url} | Следи за моим походом на {place}, вернусь к {time}: {url} | {place} sayohatimni kuzating, {time} gacha qaytaman: {url} |
| waypoint.next | Next: Waypoint {n} | Далее: точка {n} | Keyingi: {n}-nuqta |
| waypoint.hint | Check in to log your route and earn +10 XP | Отметьтесь, чтобы записать маршрут и получить +10 XP | Yo'nalishni yozish va +10 XP olish uchun belgilaning |
| waypoint.cta | Check in at waypoint | Отметиться на точке | Nuqtada belgilanish |
| waypoint.allDone | All {max} waypoints logged | Все {max} точек отмечены | Barcha {max} nuqta belgilandi |
| waypoint.xp | +{xp} XP | +{xp} XP | +{xp} XP |
| waypoint.tooClose | Walk {m} m more for the next waypoint | Пройдите ещё {m} м до следующей точки | Keyingi nuqtagacha yana {m} m yuring |
| waypoint.tooSoon | Next waypoint in {min} min | Следующая точка через {min} мин | Keyingi nuqta {min} daqiqadan keyin |
| waypoint.inaccurate | GPS is too weak here — try in the open | Слабый GPS — попробуйте на открытом месте | GPS signali zaif — ochiq joyda urinib ko'ring |
| waypoint.queued | Saved — syncs when online | Сохранено — отправим, когда будет сеть | Saqlandi — internet bo'lganda yuboriladi |
| sos.label | SOS | SOS | SOS |
| sos.hold | Hold 3 s | Держите 3 с | 3 s bosib turing |
| sos.a11y | SOS — press and hold for 3 seconds | SOS — нажмите и держите 3 секунды | SOS — 3 soniya bosib turing |
| sos.sent | SOS sent to {name} | SOS отправлен: {name} | SOS yuborildi: {name} |
| sos.tapSend | Tap Send in your SMS app | Нажмите «Отправить» в приложении SMS | SMS ilovasida «Yuborish»ni bosing |
| sos.smsText | SOS from {name} near {place}. Location: {maps}. Live: {url} — Irbis | SOS от {name} у {place}. Место: {maps}. Онлайн: {url} — Irbis | {name}dan SOS, {place} yaqinida. Joylashuv: {maps}. Jonli: {url} — Irbis |
| sos.call | Call for help · {number} | Позвонить спасателям · {number} | Yordam chaqirish · {number} |
| sos.close | Close | Закрыть | Yopish |
| sos.tooSoon | You can send another SOS in {sec} s | Повторный SOS через {sec} с | Keyingi SOS {sec} soniyadan keyin |
| checkout.cta | Check out safely | Завершить безопасно | Xavfsiz yakunlash |
| checkout.confirmTitle | Back safe? | Вернулись благополучно? | Eson-omon qaytdingizmi? |
| checkout.confirmBody | This ends your trip and tells {name} you're back. | Поход завершится, и {name} узнает, что вы вернулись. | Sayohat tugaydi va {name} qaytganingizni biladi. |
| checkout.confirm | I'm back safe | Я вернулся(ась) | Eson-omon qaytdim |
| checkout.cancel | Not yet | Ещё нет | Hali yo'q |
| offline | You're offline | Нет сети | Internet yo'q |
| summary.title | Welcome back! | С возвращением! | Xush kelibsiz! |
| summary.distance | km walked | км пройдено | km yurildi |
| summary.climb | m climbed | м набора | m ko'tarilish |
| summary.time | on the trail | в пути | yo'lda |
| summary.waypoints | waypoints | точек | nuqta |
| summary.xp | XP earned | XP получено | XP olindi |
| summary.done | Done | Готово | Tayyor |

## API SMS (`sms.sos`, user's locale) — same text as `active.sos.smsText` in en / ru / uz.

## Web (`live.*`)
| Key | en | ru | uz |
|---|---|---|---|
| title | {name}'s trip | Поход {name} | {name}ning sayohati |
| place | Going to {place} | Направляется: {place} | Manzil: {place} |
| backBy | Back by {time} | Вернётся к {time} | {time} gacha qaytadi |
| status.on_trip | On trip | В походе | Sayohatda |
| status.late | Running late | Опаздывает | Kechikmoqda |
| status.alerted | Contact alerted | Контакт оповещён | Kontaktga xabar yuborildi |
| status.back_safe | Back safe | Вернулся(ась) благополучно | Eson-omon qaytdi |
| last | Last location {min} min ago | Последнее место {min} мин назад | Oxirgi joylashuv {min} daq oldin |
| lastNone | No location yet | Места пока нет | Hali joylashuv yo'q |
| openMaps | Open in Maps | Открыть на карте | Xaritada ochish |
| ended | This trip has ended | Поход завершён | Bu sayohat tugagan |
| notFound | Link not found | Ссылка не найдена | Havola topilmadi |
| error | Couldn't load the trip | Не удалось загрузить поход | Sayohatni yuklab bo'lmadi |
| retry | Try again | Повторить | Qayta urinish |
| footer | Shared from Irbis | Отправлено из Irbis | Irbis orqali ulashildi |
