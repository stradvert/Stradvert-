# Counter reel: a run of no's, then the yes

Ryan's idea (27 Nov 2026): "a bunch of no's and a counter til we get someone who does". The style sits halfway between
the minimal edit and the trailer edit: full-bleed footage and the minimal captions and pills, plus punch-ins, X slams
with a buzzer, a freeze, confetti, emoji stickers and a synthesised comedy score. No cut-outs, no big type behind people.

No footage, frames, transcripts, edit lists or `data.json` live in this repo.

## Shape that worked (second cut: 39 seconds)

1. **Hook, about 3 s.** The funniest wrong answer, not the host to camera. The headline pill is on screen in frame one
   (`s` below 0), the bracketed second line lands half a second later. Jump cuts with a punch-in.
2. **The counter.** Every ask in the real order. Each no lands a red X (buzzer, stamp, screen shake, red edge flash) that
   flies into a row of tiles under the headline. The theme adds a layer every couple of no's.
3. **False hope.** A yellow "?" tile pulses, a drumroll runs and dips under the answer, the no lands, then a freeze in
   black and white with a tally line ("0 for 7") and a sad trombone.
4. **Payoff.** A pill sets it up ("Then person #8 showed up"), a choir swells under them, and the yes gets a check, a
   win word, confetti and a flash over a freeze that zooms in.
5. **The yeses.** The best answers from people who did, over an upbeat groove, with "(wait for the last one)" under
   the headline. The groove tape-stops before the last punchline so it plays dry, and the end hit comes back with the
   comment question pill and the link.

Pacing that Ryan asked for on the second cut (27 Nov 2026): "every line adds anticipation", "not spending too long on
one person unless necessary". What that meant in practice: drop any line that does not move towards the yes (a setup
like "just guess", a side joke after a no), split a question from its answer and punch in on the answer, cut long
thinking pauses down to about half a second, and reframe inside a long answer on a key word.

## Series (one shoot cut into parts that lead into each other)

First used 27 Nov 2026 for a three part series: part 1 the counter, ending on a teaser of part 2; part 2 a fast recap
montage of the no's and the story of the one who knew; part 3 the best yeses, ending on the comment question. Each
part ends on its cliffhanger: a question or a line cut before the answer, then a card for the next part.

- `badge` `{text, s, e}`: the "PART 1" tag above the headline.
- `card` `{s, title, sub}`: dims the last frame (hold it with a freeze in the edit list) and slams the next part's title.
  The sub line is a question or a tease, never a claim ("(who is that?)", "(his answer)").
- `noTiles: true` with `xScale` and `xHold`: quick X stamps for a montage, no tile row and no counter number.
- A recap montage keeps the real order: use the no's that happened before the moment it leads into.
- `snd_cues.py data.json music.wav sfx.wav` builds the sound from a cue list (`cues` in data.json) instead of the
  fixed counter shape: theme, roll, trombone, swell, hit, aah, groove, button, tension, sting, impact, buzz, buzzer,
  tock, boing, pop, whoosh, scratch, bell. Instruments live in `synth.py`.
- `cut.py` takes `ain` on a piece whose picture cut sits right against the previous word: the audio starts a few ms later.

## Counter rules (see the repo `CLAUDE.md`)

- Count only asks with an answer on camera, keep them in the real order, and the tiles on screen match the asks shown.
- A hook taken from another part of the day is not counted.
- Coached answers are never used as genuine.

## Steps

1. Raw review first (`../raw_review/`): transcript, speakers, then pick the lines.
2. Place every cut. `../raw_review/strip.py a48.wav <from>:<to>` shows the gap, `../raw_review/align.py` gives word edges.
   In-point on a frame boundary about 0.1 to 0.15 s before the first sound, out-point after the last sound has died.
   Where two people overlap, cut at the dip and use a short fade (`fin`, `fout`) or end the audio a few ms late (`aout`).
3. `python3 cut.py raw.mov a48.wav a48_dn.wav edl.json` (48 kHz mono of the raw, and the same through `arnndn` at
   `mix=1`). Writes `frames/`, `voice_raw.wav`, `segs_out.json`. `AUDIO_ONLY=1` rebuilds just the voice.
4. `python3 ../raw_review/cutcheck.py voice_raw.wav segs_out.json`: every piece must read complete on its own.
5. `python3 level.py voice_raw.wav lines.json` (`[[t0, t1, who]]`, H host, G guest, L laugh, `-` no voice) writes `voice.wav`.
6. `data.json` (fields below), copy `fonts/` from `../minimal_portrait_reel/`, stills with `node render.js 0,150,300 test`,
   then `node render.js` for every frame.
7. `python3 snd.py data.json music.wav sfx.wav && MG=-9 ./mix.sh` gives `mix.wav` at -14 LUFS.
8. `python3 ../raw_review/cutcheck.py mix.wav segs_out.json` on the final mix: the captions must match what it hears.
   Encode like `../day_in_the_life/encode_d.sh`.

## data.json

| field | meaning |
| --- | --- |
| `nf`, `total` | frames in `frames/` (no end card: the video loops) |
| `shots` | `{k, t0, t1, f0, z0, z1, fx, fy, sx, sy, freeze, pop, grey, bright, steps}`: zoom from `z0` to `z1`, the point `fx, fy` (fraction of the source frame) sits at `sx, sy` on screen. `pop` punches in on the cut, `grey` is the black and white freeze, `bright` flashes the payoff freeze. `steps` reframe inside a long line, cut on a word: `[{t, z0, z1, fx, fy, sx, sy, pop}]` |
| `caps`, `capEnd`, `who` | caption groups `[[word, time], ...]` on the output timeline, optional end time per group, H or G |
| `xs` | the time each no lands (one X and one tile each) |
| `q` | `[start, end, slot, pulse faster from]`: a "?" tile waiting on a maybe; slot `len(xs)` is the yes |
| `check`, `checkEnd` | the yes lands, and when the check and win word leave |
| `fz` | `[t0, t1]` of the freeze after the last no (the last X holds through it) |
| `zeroText`, `winText` | the tally line on the freeze and the win word |
| `stripOn` | when the tile row is on screen |
| `pills` | `{text, s, e, wipe, sub?, cta?, top?}`; `**word**` gets the yellow wipe, `<br>` breaks the line, `cta` is the end question, `top` moves a pill or sub line (a sub under a one-line pill sits at 272) |
| `stickers` | emoji `{e, s, d, x, y, r}` that pop in on a word |
| `whips` | section changes (zoom blur and a whoosh) |
| `snd` | section anchors for the score: `theme [t0,t1]`, `roll [t0,t1,dip0,dip1]`, `swell t0`, `groove [t0,t1]`, `tapestop` seconds, `button t` |
| `link` | the only link on screen (stradvert.org) |

## Checks that mattered

- **The noise reducer runs 10 ms late.** `arnndn` output is 480 samples behind its input at 48 kHz. Blending it with the
  original without shifting it makes a comb filter that smears consonants: on the first build a punchline transcribed as
  nonsense. `cut.py` shifts it before blending. `arnndn`'s own `mix=` option already lines the two up.
- **Transcript times are not cut points.** A line's first word can be 0.3 to 0.5 s off in the transcript. The first plan
  would have clipped the hook's first word. Place every in-point from the strip and the aligner.
- **Short pieces read wrong on their own.** A one-word "No." can come back as "Thank you" from the checker; confirm it in
  the full pass.
- **Captions:** at most four words and never wider than 920 px (the comp scales down anything wider, but split it instead).
- **Keep the X off faces:** it slams at chest height and flies up into the row.
- **Nothing loud under a key answer:** the drumroll dips under the maybe, and the music stops for the last punchline.
