# N111 change log

- Implemented whole-image DSL with Rotate90, Reflect, ColorMap, FloodFill_Background and Gravity_Shift_Pixels.
- Implemented an exact-output BFS with shortest-program witness, three-operation depth limit, unique-array deduplication, and 5,000-expanded-state cap.
- Collected full original 15-family Level-1 training split under frozen N093 B1, without modifying the existing Kaggle submission.
- Audited all nine real rewarded source/terminal images; no exact bounded program found; one search truncated.
- Confirmed five native frame pairs independently match N101 archived source evidence.
- Replayed the 203 successful Level-1 actions independently and inspected Level-2 legal input verbs: seven coordinate-click, two without it; none accepts target colour.
- Distinguishes desired pixel writes from legal native SDK actions; no fabricated Level-2 execution claim.
- Added positive DSL unit tests, native evidence integrity checks, deterministic reproduction commands and checksum manifest.