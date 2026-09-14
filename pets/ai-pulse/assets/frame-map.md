# AI Pulse Frame Map

AI Pulse deliberately keeps artwork in every cell of the `8×11` v2 atlas.
The frames currently selected by Codex form complete core animations. The 14
remaining cells are authored as semantic continuations rather than empty
padding, so they can be reused if a future runtime plays complete eight-frame
rows.

Rows and columns below are one-based, matching the contact sheet. Runtime row
indices are one less than the displayed row number.

| Contact-sheet row | State | Current core | Extended or auxiliary frames |
| ---: | --- | --- | --- |
| R1 | Idle / sleep | C1-C6: awake, blink, yawn, tire, lie down, sleep | C7: extended wake/celebration frame; C8: settle back to neutral |
| R2 | Run right | C1-C8: complete exaggerated rightward run | None |
| R3 | Run left | C1-C8: complete exaggerated leftward run | None |
| R4 | Wave | C1-C4: neutral, greeting, wave, warm response | C5-C8: raised-hand flourish, energetic response, and settle frames |
| R5 | Jump / handstand | C1-C5: anticipation, launch, flight, rotation, inversion | C6-C8: handstand hold, recovery rotation, and landing |
| R6 | Failure / fatigue | C1-C8: surprise, dizziness, fatigue, collapse, and recovery | None |
| R7 | Waiting / water break | C1-C6: waiting, thirst, receive water, drink, finish, relief | C7-C8: water/electric flourish and neutral reset |
| R8 | Active work / music | C1-C6: headphones appear, listening, groove, and active beat | C7-C8: electric musical flourish and neutral reset |
| R9 | Review | C1-C6: inspect, magnify, investigate, and review code | C7-C8: successful sparkle and neutral reset |
| R10 | Look directions A | C1-C8: 000° through 157.5° | None |
| R11 | Look directions B | C1-C8: 180° through 337.5° | None |

## Compatibility rule

- Never depend on an auxiliary frame to complete a current runtime state.
- Keep every auxiliary frame visually related to the state in its row.
- Preserve all 88 authored cells when exporting the runtime WebP.
- Treat future eight-frame playback as an adaptation target, not a guarantee:
  if Codex changes row semantics, update this map before remapping the atlas.

