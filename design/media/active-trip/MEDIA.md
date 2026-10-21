# Media — active-trip

Screen: `ActiveTrip` (canvas). Canvas asset ids from `design/assets.md`.

| File | What | Used on | Format / size | Status (exists · needed · placeholder OK) |
|---|---|---|---|---|
| `companionFox.ts` (canvas `d1b0d619…`) | Current user's companion, neutral | ActiveTrip bottom sheet ("Next: …") | SVG | exists · final |
| map backdrop (canvas `503359ad…`) | Trail terrain map stand-in | ActiveTrip background | — | replaced by the real MapLibre map (places already uses it) |
| route line, waypoint pins (✓ done / numbered next), "You are here" dot, distance chip | Map overlays | ActiveTrip map | drawn (MapLibre layers + tokens) | exists (drawn) |
| SOS radial progress ring (3 s hold) | Ring fills around the SOS button | ActiveTrip SOS | Reanimated, no file | exists (drawn) |
| waypoint check-in ring fill + floating "+10 XP" chip | Celebration on waypoint check-in | ActiveTrip | Reanimated, no file | exists (drawn) · a Lottie could replace it later |
| contact initial avatar | Circle with the contact's first letter | "Malika is following" row | tokens, no file | exists (drawn) |
| SOS / check-in / check-out icons | Button icons | ActiveTrip buttons | shared `Icon` set | exists if `Icon` has them · else placeholder OK (generic icon) |
