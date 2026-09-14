# ai-pulse Runtime Sprite Audit

- Atlas: `1536×2288` WebP
- Grid: `8×11` (`88` frames)
- Cell: `192×208` RGBA after decoding
- Atlas SHA-256: `3729fa7413a97df4bd3cf4cfa82f341e4d5f5ed249c5b0772278312213d791c3`
- Method: SHA-256 over every decoded RGBA cell; SHA-256 over each complete 11-frame column.

## Duplicate result

Exact duplicate decoded frames were found:

- `30d4da31db85877f0102e0d56b9559e9d4400fde83c253a19c7c1988b4ed0c64`: R1C8, R4C5, R4C6, R4C7, R4C8, R5C6, R5C7, R5C8, R7C7, R7C8, R8C7, R8C8, R9C7, R9C8

No complete duplicate columns were found.

## Per-frame hashes

| Row | C1 | C2 | C3 | C4 | C5 | C6 | C7 | C8 |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `0182695425db` | `d69cdcc77c59` | `462691094bd3` | `70d7b5326d0f` | `d81d32a827d0` | `19f28af774ce` | `46f6d750e65d` | `30d4da31db85` |
| 2 | `204ba227e679` | `025a58adce24` | `2681b244b762` | `209e953f593a` | `f016cd81c619` | `8095a1545e70` | `769aa4df3271` | `9a9d28d2860a` |
| 3 | `7f7cc5cfaf81` | `516db1bd6be6` | `147baca2010d` | `332d2fed94cf` | `211f64f47649` | `10bf680ca6d4` | `048c975bd46a` | `f7c120d0b42c` |
| 4 | `4a14b6445843` | `cbd3bd7b986e` | `d855ddd1d5f0` | `bff7586b3f64` | `30d4da31db85` | `30d4da31db85` | `30d4da31db85` | `30d4da31db85` |
| 5 | `8048b7314884` | `59a454a30f87` | `2a3c6f0385c5` | `ff3fc8294cef` | `f897c7ffae7a` | `30d4da31db85` | `30d4da31db85` | `30d4da31db85` |
| 6 | `c20636e778d7` | `46409bfe788e` | `1dc042ece144` | `e01f07cb9ad5` | `b8dda33cb1c8` | `d47d7a48bca9` | `1aebc8aa09ac` | `87b2ad985b0e` |
| 7 | `49a635217a2f` | `d96e34967f72` | `5b7011d4a6be` | `7dd53233d79f` | `4a29c22c08ea` | `be26fa89c089` | `30d4da31db85` | `30d4da31db85` |
| 8 | `c3e4d9eddff4` | `45600134a302` | `2a3d1d03f379` | `958071f1b82b` | `277d4da11075` | `c5a0565dcc53` | `30d4da31db85` | `30d4da31db85` |
| 9 | `8b26da456eb6` | `59da0655edf2` | `dfce0116578a` | `371c90bcadd7` | `106c3123e920` | `baaa8798d0f1` | `30d4da31db85` | `30d4da31db85` |
| 10 | `9b8d0578eb3b` | `ca350499e934` | `0387b68e5126` | `559ffcf30f96` | `c6e48336b0cc` | `d4e18a334e59` | `0c24373dc575` | `158c4eee0953` |
| 11 | `bef3546e7ede` | `aa66e56bd9b2` | `1ea388e90daf` | `747d307451ca` | `4a46f951e689` | `dbea64caafbb` | `099b57b6addb` | `c11dd0b102d3` |

## Per-column hashes

- C1: `0351c606bbb915f23fa25d4b579744128b112e9651432cffb1efbc84d6d07248`
- C2: `5f6a3e6d185362af35af6fa698c234c12f1710af8f9b527b67e725c3199d5fa8`
- C3: `a35e8cabdc0e0e70469ff74dbc1763367fe7215af0a0cb098aa65a6723fb408b`
- C4: `7ebbce8fd0aaae93f93d5e678de781f4abb350b3f0b861203f60d92d8270ff20`
- C5: `7d9daf1102161bb1cd22005b548396842d51382769f7303b3641f8eec69fd953`
- C6: `bf82de4c03ae9bd74b3d88b1d7f124ae37af0b842bb95382fae7d9f963b29dc9`
- C7: `490333ee3371d88efff0de43e718acdb1c160d17c25d13edceec3890cda1605c`
- C8: `ea5860b054530eadd699746335d6dfac4bd0489c884a4b8dfa3f542e6990f036`
