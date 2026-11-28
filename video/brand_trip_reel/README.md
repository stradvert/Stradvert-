# Brand trip reel: a client's street ad in the client's own look, with a trippy payoff

First used 28 Nov 2026 for a free 30 second version of a client's winning street ad. Ryan asked to "change edits but take
major inspiration from the winning ad", to keep "all the same points", to use the brand's colours and type, to make the
spoon "highlight", and for "trippy effects" that "really elevate the video". Output is 1080x1350 (4:5) to match the ad
it is based on.

No footage, frames, transcripts, edit lists or `data.json` live in this repo.

## Shape that worked (30 s)

1. **Fresh hook.** A line the running ad does not open on, so the client gets a new creative to test rather than a
   copy of one already live. The product is lit up in the first frame (glow, ring, sparkles, a light sweep, the rest of
   the frame dimmed).
2. **What it is, then trust.** The explanation, the social proof line, then stamps for the spoken trust claims
   (each stamp only says what is said).
3. **The taste.** The product reaches the mouth with a light burst and a punch-in.
4. **"N minutes later".** A honey drip floods the screen, the number and "minutes later" sit on it (the number is
   spoken just before), then the honey slides away into the trip.
5. **The trip.** WebGL pass on the footage: wave warp, colour split, hue swing, bloom, mirror flashes on cuts, a
   honeycomb overlay, half-time phased music. It peaks on the reaction word and settles under the next line.
6. **Call to action.** A URL bar types in, an urgency stamp if it is spoken, then an end card with the product, the
   URL and the spoken tagline.

## Files

- `cut.py`: many raw files, 60 fps portrait, to 30 fps frames and a voice stem. Edit list in source seconds,
  `ain`/`aout`/`aend` for tight joins (`aend` lets the picture run on under the end card with the audio stopped).
  Needs `<src>.48.wav` and `<src>.dn48.wav` (arnndn) per raw in the audio folder.
- `comp.html`: the composition. Brand colours are the `:root` variables, titles use Anton (in `fonts/`), captions use
  Montserrat (copy from `../minimal_portrait_reel/fonts/`).
- `score.py`: music and effects, synthesised, using `../counter_reel/synth.py`. Reads cue times from `data.json`.
- `render.js`: renders at 1080x1350. Mix with `../counter_reel/level.py` and `mix.sh` (level.py needs 16 bit input).

## data.json

| field | meaning |
| --- | --- |
| `shots` | framing per piece, as in the counter reel (`z0 z1 fx fy sx sy pop steps`), source is 1080x1920 |
| `caps`, `capEnd` | caption groups `[[word, time, emphasis], ...]` |
| `spots` | product highlight: `{s, e, amt, glow, r, sweep?, keys: [[frame, x, y], ...]}`, x and y as fractions of the source frame |
| `bursts` | light burst `{t, x, y}` |
| `trip`, `pulse`, `kal` | trip envelope `{s, e, amt, in, out}`, short pulses `{t, d, amt}`, mirror flash windows `[t0, t1]` |
| `title`, `stamps`, `stickers` | hook title lines, stamps `{text, s, e, x, y, rot, cls}`, emoji stickers |
| `timer`, `honey`, `later` | the countdown dial (`label`), the drip `{s, full, out, e}`, the "minutes later" card (`n`, `w`) |
| `bees`, `url`, `end`, `whips` | flying emoji, the URL bar, the end card (`url`, `jar` image, `tag`, `pill`), zoom-blur cuts |

## Checks that mattered

- **The brand's site may block automated access** (a bot check). Do not try to get round it. Match colours and type
  from the client's own winning ad and the product in the footage, and ask Ryan for the brand files.
- **Coached lines stay out.** Raws can contain directions to the talent ("deny me at first", "that part there is the
  ... part"). Keep them out and tell Ryan which takes were directed.
- **Off-mic speech fools the aligner.** If a quiet speaker's words land on the next loud word, align a wider span and pin
  the times.
- **Put stamps where nobody's face is**, shot by shot. The same y does not work for a wide shot and a close-up.
- **Raw audio can already be clipped** when the host talks close to the mic. Level it down and say so.
