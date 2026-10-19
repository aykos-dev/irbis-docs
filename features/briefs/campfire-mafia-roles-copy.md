# campfire-mafia — role table + role copy (shared by briefs 1–3)

Role ids are stable (wire + tests). Order = setup order. Colours/glyphs: `design/media/campfire-mafia/MEDIA.md`
(8 glyph paths are in the brief 1 "Glyphs" list; sniper/journalist/immortal = draw crosshair / notepad / infinity).

| id | team | colour | glyph |
|---|---|---|---|
| boss | mafia | #8F1F1F | crown |
| mafia | mafia | #D93636 | hat |
| detective | town | #1F74C7 | glass |
| doctor | town | #2E8B57 | cross |
| maniac | solo | #6A4FE8 | moon |
| lover | town | #C93A6B | heart |
| bodyguard | town | #0C807A | shield |
| sniper | town | #B5651D | crosshair (placeholder) |
| journalist | town | #8A6D1F | notepad (placeholder) |
| immortal | town | #4E7D8C | infinity (placeholder) |
| civilian | town | #5E6E74 | person |

## Keys `maf.role.<id>.name` / `.desc` (setup row) / `.night` (card line 1)
| key | en | ru | uz |
|---|---|---|---|
| boss.name | Mafia Boss | Босс мафии | Mafiya boshlig'i |
| boss.desc | Leads the mafia vote. Checks if a player is the Detective. | Ведёт голосование мафии. Проверяет, комиссар ли игрок. | Mafiya ovozini boshqaradi. O'yinchi detektivmi — tekshiradi. |
| boss.night | At night wake with the mafia, choose the victim, then ask the narrator if one player is the Detective. | Ночью просыпайтесь с мафией, выберите жертву, затем спросите ведущего, комиссар ли один игрок. | Tunda mafiya bilan uyg'oning, qurbonni tanlang, so'ng boshlovchidan bir o'yinchi detektivmi deb so'rang. |
| mafia.name | Mafia | Мафия | Mafiya |
| mafia.desc | Wakes with the boss and chooses a victim. | Просыпается с боссом и выбирает жертву. | Boshliq bilan uyg'onib, qurbon tanlaydi. |
| mafia.night | At night wake with the mafia and pick one player to kill together. | Ночью просыпайтесь с мафией и вместе выберите, кого убить. | Tunda mafiya bilan uyg'oning va birgalikda kimni o'ldirishni tanlang. |
| detective.name | Detective | Комиссар | Detektiv |
| detective.desc | Checks one player each night: mafia or not. | Каждую ночь проверяет одного игрока: мафия или нет. | Har tun bir o'yinchini tekshiradi: mafiyami yoki yo'q. |
| detective.night | At night point at one player — the narrator shows you if they're mafia. | Ночью укажите на игрока — ведущий покажет, мафия ли он. | Tunda bir o'yinchini ko'rsating — boshlovchi u mafiyami, bildiradi. |
| doctor.name | Doctor | Доктор | Shifokor |
| doctor.desc | Saves one player each night. Self once. | Спасает одного игрока за ночь. Себя — один раз. | Har tun bir o'yinchini qutqaradi. O'zini — bir marta. |
| doctor.night | At night pick one player to save. If the mafia picked them, nobody dies. You can save yourself once. | Ночью выберите, кого спасти. Если мафия выбрала его, никто не умрёт. Себя можно спасти один раз. | Tunda kimni qutqarishni tanlang. Mafiya uni tanlagan bo'lsa, hech kim o'lmaydi. O'zingizni bir marta qutqara olasiz. |
| maniac.name | Maniac | Маньяк | Manyak |
| maniac.desc | Plays alone. Wins if last one standing. | Играет один. Побеждает, если останется последним. | Yakka o'ynaydi. Oxirgi qolsa, yutadi. |
| maniac.night | At night wake alone and pick one player to kill. | Ночью просыпайтесь один и выберите, кого убить. | Tunda yolg'iz uyg'oning va kimni o'ldirishni tanlang. |
| lover.name | Lover | Любовница | Oshiq |
| lover.desc | Blocks one player's night action. | Блокирует ночное действие одного игрока. | Bir o'yinchining tungi harakatini to'sadi. |
| lover.night | At night pick one player — their night action doesn't work tonight. | Ночью выберите игрока — его ночное действие сегодня не сработает. | Tunda bir o'yinchini tanlang — uning tungi harakati bu kecha ishlamaydi. |
| bodyguard.name | Bodyguard | Телохранитель | Tansoqchi |
| bodyguard.desc | Protects one player; dies in their place. | Охраняет игрока и погибает вместо него. | Bir o'yinchini qo'riqlaydi; uning o'rniga o'ladi. |
| bodyguard.night | At night pick one player to guard. If they're attacked, you die instead. | Ночью выберите, кого охранять. Если на него нападут, умрёте вы. | Tunda kimni qo'riqlashni tanlang. Unga hujum qilinsa, o'rniga siz o'lasiz. |
| sniper.name | Sniper | Снайпер | Snayper |
| sniper.desc | One shot per game, at night. | Один выстрел за игру, ночью. | O'yinda bitta o'q, tunda. |
| sniper.night | Once per game, at night, you can shoot one player. Choose wisely. | Один раз за игру ночью вы можете застрелить игрока. Выбирайте с умом. | O'yinda bir marta, tunda bir o'yinchini otishingiz mumkin. Oqilona tanlang. |
| journalist.name | Journalist | Журналист | Jurnalist |
| journalist.desc | Compares two players: same team or not. | Сравнивает двух игроков: одна команда или нет. | Ikki o'yinchini solishtiradi: bir jamoadami yoki yo'q. |
| journalist.night | At night point at two players — the narrator shows if they're on the same team. | Ночью укажите на двух игроков — ведущий покажет, в одной ли они команде. | Tunda ikki o'yinchini ko'rsating — boshlovchi ular bir jamoadami, bildiradi. |
| immortal.name | Immortal | Бессмертный | O'lmas |
| immortal.desc | Can't be killed at night. Only the vote takes them out. | Ночью его не убить. Выбывает только по голосованию. | Tunda o'ldirib bo'lmaydi. Faqat ovoz bilan chiqadi. |
| immortal.night | Night kills don't work on you. Only the town's vote can take you out. | Ночные убийства на вас не действуют. Выбыть можно только по голосованию. | Tungi o'ldirishlar sizga ta'sir qilmaydi. Faqat shahar ovozi sizni chiqara oladi. |
| civilian.name | Civilian | Мирный житель | Tinch aholi |
| civilian.desc | No night action. Finds the mafia by talking. | Без ночного действия. Ищет мафию в разговоре. | Tungi harakati yo'q. Mafiyani suhbatda topadi. |
| civilian.night | You sleep at night. No night action. | Ночью вы спите. Ночного действия нет. | Tunda uxlaysiz. Tungi harakat yo'q. |

## Keys `maf.team.<team>.day` / `.win` (card lines 2–3) and `maf.team.<team>` (chip)
| key | en | ru | uz |
|---|---|---|---|
| town | TOWN | ГОРОД | SHAHAR |
| mafia | MAFIA | МАФИЯ | MAFIYA |
| solo | SOLO | ОДИНОЧКА | YAKKA |
| town.day | By day talk, find the mafia and vote them out. Keep your role quiet. | Днём обсуждайте, ищите мафию и голосуйте против неё. Не раскрывайте роль. | Kunduzi suhbatlashing, mafiyani toping va unga qarshi ovoz bering. Rolingizni oshkor qilmang. |
| town.win | You win when every mafia member and the maniac are out. | Вы побеждаете, когда выбыли вся мафия и маньяк. | Barcha mafiya va manyak chiqqanda yutasiz. |
| mafia.day | By day blend in and steer the vote away from your team. | Днём не выделяйтесь и уводите голосование от своих. | Kunduzi ko'zga tashlanmang va ovozni jamoangizdan chalg'iting. |
| mafia.win | You win when the mafia equals or outnumbers everyone else. | Вы побеждаете, когда мафии столько же или больше, чем остальных. | Mafiya qolganlarga teng yoki ko'p bo'lganda yutasiz. |
| solo.day | By day trust nobody and steer the vote to suit you. | Днём никому не верьте и направляйте голосование себе на пользу. | Kunduzi hech kimga ishonmang va ovozni o'zingizga foydali tomonga buring. |
| solo.win | You win if you're the last one standing, or one of the last two. | Вы побеждаете, если останетесь последним или одним из двух последних. | Oxirgi yoki oxirgi ikkitadan biri bo'lib qolsangiz, yutasiz. |
