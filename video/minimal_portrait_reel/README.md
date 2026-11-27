# Minimal portrait reel (the default edit)

Clean 1080x1920 edit: full-bleed talking head with a slow push-in, short word-by-word captions with a yellow
block on the spoken word, white headline pills with a yellow highlight wipe, b-roll cards (the talking head
shrinks into a rounded card underneath), a thin progress bar and a logo end card.

Everything on screen comes from `data.json`. No footage, frames, transcripts or `data.json` live in this repo.

## Steps

1. **Source.** Download the raw. If it already has captions burned in, stop and ask for the clean file.
2. **Transcribe.** `ffmpeg -i raw.mp4 -ac 1 -ar 16000 a16.wav && python3 tr.py a16.wav words_raw.json`
3. **Cut.** Pick the segments (suggest the cut first unless told to go ahead), cut on pauses, build `cut.mov`
   at 30 fps with the cleaned voice, then transcribe the cut again into `words.json`.
4. **Frames.** `ffmpeg -i cut.mov -vf "crop=<portrait crop on the face>,scale=1080:1920" -q:v 2 frames/%05d.jpg`
5. **Captions.** `python3 caps.py words.json data.json` then add the other fields (see `data.example.json`).
   Read every caption group against the audio: fix names, numbers and brand words by hand.
6. **B-roll.** `ffmpeg -ss <s> -t <d> -i clip.mp4 -an -vf "fps=30,crop=...,scale=920:-2" b0/%05d.jpg`
   Muted, colour matched, only where it shows what is being said, never the same shot twice.
7. **Stills first.** `node render.js 30,200,400 test` and look at them. Then `node render.js` for all frames.
8. **Sound and encode.** `python3 snd.py && ./encode.sh ../../video_out/<topic>_minimal_v1.mp4`
9. **Check** the finished file: frame sheet, loudness near -14 LUFS, captions match the words, text rules.

## data.json

| field | meaning |
| --- | --- |
| `nf` | frames of footage in `frames/` |
| `total` | total frames including the end card (usually `nf + 66`) |
| `vd` | seconds where the end card starts (`nf / 30`) |
| `cuts` | shot boundaries in seconds, starting with 0 and ending with `vd` (the push-in resets on each) |
| `caps` | caption groups: `[[["word", time], ...], ...]` (from `caps.py`) |
| `lastEnd` | end time of the last spoken word |
| `pills` | headline pills: `{text, s, e, wipe}`; wrap key words in `**` for the yellow wipe; add `"sub": true` for a small line under the pill |
| `broll` | b-roll cards: `{s, e, dir, n, y, h}` (frames in `dir/%05d.jpg`, `n` frames, card top `y`, height `h`) |
| `focus` | push-in origin in percent, set it on the face (default `[52, 36]`) |
| `shrinkTop` | vertical offset of the footage inside the shrunken card (default `-450`) |
| `capPlate` | `true` dark plate behind captions (default), `false` bare text with shadow |
| `link` | end card link (default `stradvert.org`) |
| `cards` | tall cards (a phone screen recording, a rendered page): `{s, e, dir, n, x, y, w, h, r, bezel}`. By default the footage dims and blurs behind the card. `dim: false` keeps it sharp, `hard: true` ends the card on the cut, `pop` and `origin` grow it out of a point, `lead` delays its first frame |
| `layouts` | split screen: the footage moves into its own rounded card `{s, e, hard, x, y, w, h, r, imw, imx, imy}` (`imw` is the width the footage is drawn at inside the card, `imx` and `imy` its offset) |
| `lists` | tick lists: `{s, e, y, dim, rows: [{text, at}]}`, each row ticks at its `at` time |
| `capEnd` | optional end time per caption group (same order as `caps`), so a caption clears before a cut |
| `cutFx` | per-shot push-in: `{"<cut index>": {"zoom": 0.1, "focus": [50, 47]}}` |

A pill with `"sub": true` is the small bracketed second line. It sits on its own dark plate so it reads over bright sky.
For an edit with no voiceover (a day in the life), see `../day_in_the_life/`.

Custom cards (quote card, ranking, status card) are in `../claude_founder_reel/comp.html`: copy the block you need.

## Requirements

Node with Playwright (preinstalled in Claude Code cloud sessions), ffmpeg, Python with `numpy scipy faster-whisper`.
