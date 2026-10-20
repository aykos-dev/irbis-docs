# Crocodile — test cases (campfire-crocodile AC1–AC8 + campfire-core multi-player)

Players: **A** = emulator-5554 host, **B** = emulator-5556 real joiner, **bots** = `scripts/qa/campbot.py`.
Timer cases use 30 s. Bot JSONL logs are the privacy evidence (who received the word, when).

| id | title | AC | players | steps | expected |
|---|---|---|---|---|---|
| CROC-01 | Tile in hub + picker | AC1 | A | CampHub grid, lobby picker | `camp.hub.game.croc`, `camp.lobby.game.croc` present, no Coming soon — glyph manual |
| CROC-02 | Settings defaults | AC1 | A + 2 bots | Select Crocodile | Timer 60 selected; 3 packs ticked |
| CROC-03 | At least 1 pack | AC1 | A + 2 bots | Untick all 3 packs | Last pack can't be unticked or Start disabled with reason |
| CROC-04 | Fewer than 3 players | AC1 | A + 1 bot | Select Crocodile | Start disabled "Crocodile needs 3+ players" |
| CROC-05 | Too many (16th seat) | core AC6 | A + 15 bots | Add 15th bot | `rejected full` |
| CROC-06 | Pick screen | AC2 | A + B + 2 bots | Start (30 s) | Host "Who shows next?" with all connected seats incl. host; B "The host is choosing who shows" |
| CROC-07 | Word only to describer | AC3 | A + B + 3 bots | Pick bot_1 | Only bot_1 gets `deal croc`; others' logs contain no word id until `result`; B sees "bot_1 is showing" |
| CROC-08 | Describer card (B) | AC3 | A + B + 2 bots | Pick B; hold card | Card shows word, pack name, rule "Show it, don't say it — no words, no sounds", Skip, Start (manual for hold) |
| CROC-09 | Skip | AC3, AC4 | A + B + 2 bots | Describer bot sends crocSkip (ready) and again while running | New `deal` with a different word; `skipped`+1 each time |
| CROC-10 | Timer runs everywhere, time up at 30 s | AC4, AC5 | A + B + 2 bots | Describer bot sends crocStart; wait 30 s | `running` with remainingMs ≈ 30000; B timer counts; after ≈30 s `result timeUp` + word; turns+1 |
| CROC-11 | Guessed | AC5 | A + B + 2 bots | Describer sends crocGuessed while running | All phones "Guessed!" + word; guessed+1, turns+1; back to pick |
| CROC-12 | Guessed / start / skip from non-describer or stale turn | AC3–AC5 | bots | bot_2 (not describer) sends crocGuessed/crocSkip/crocStart; describer sends stale turnNo; double crocGuessed | All ignored; totals change once |
| CROC-13 | Host as describer | AC2 | A + 2 bots | Host picks own seat | Host sees card + Start/Skip/Guessed on its phone |
| CROC-14 | Describer leaves mid-turn | AC6 | A + B + 3 bots | Describer bot `leave` (and a drop by silence) while running | Turn cancelled "<nick> left — the word is not counted", back to pick; reconnecting seat pickable again after reconnect |
| CROC-15 | Join mid-game | AC6 | A + 2 bots + bot_new | New bot hello during pick | Becomes guesser, pickable in next pick |
| CROC-16 | Below 3 players continues | AC6 | A + 2 bots | One bot leaves mid-game | Game goes on |
| CROC-17 | Host removes a player | core AC6, AC6 | A + 3 bots | Long-press/remove describer | Bot `removed`; turn cancelled if describer |
| CROC-18 | End + summary + Play again | AC7 | A + B + 2 bots | After 2 turns host End → confirm | "End the game?"; all phones "Game over", "Words guessed g · Skipped s · Turns t"; B "Waiting for the host"; Play again → totals 0, pick |
| CROC-19 | No repeated words | AC3 | A + 3 bots | Skip 30+ times in one pack set; collect word ids | No id repeats until the pack is exhausted |
| CROC-20 | Host app killed and resumed | AC6 | A + 3 bots | force-stop during running, reopen → Resume | Game resumes; current turn back at "ready" |
| CROC-21 | Old protocol rejected | AC1 | bot | hello with v 4 | `rejected version` |
| CROC-22 | B joins by code | core AC5 | A + B | B Join → code → Join as | "Room found · N players waiting" card; joins lobby |
