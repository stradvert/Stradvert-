# Story edit: a day in the life (minimal style, worked example)

A montage with no voiceover: the story is carried by short pills, the speaker's own lines are captioned, and the
music follows the story. It renders with the minimal template in `../minimal_portrait_reel/` (copy `comp.html`,
`render.js` and `fonts/` from there). This folder holds the parts that are specific to a story edit.

No footage, frames, transcripts or `data.json` live in this repo.

## Shape that worked

1. **Hook (0 to 3s):** the strangest picture in the footage first, with the context pill already on screen in
   frame one, a bracketed second line half a second later, and one clear spoken line.
2. **Rewind:** "The plan", told fast. The phone screen recording plays next to the shot of him on his phone (split screen:
   the footage moves into a card on the left, the recording grows out of his phone on the right).
3. **The story**, in the speaker's own words, cut on pauses.
4. **The punchline** with the music stopped.
5. **The work:** what the day was actually for, one idea per shot (call, what was shown on the call, what happens after it).
6. **Close:** one wry line, a last spoken tag, end card.

## Steps

1. Transcribe the raw (`../minimal_portrait_reel/tr.py`), build contact sheets, list every usable spoken line with its time.
2. `cut_d.py` : edit the three lists at the top. `PIC` is picture (key, start, end in the source). `VOICE` is sound
   that can start on any shot, so a line can run as voiceover over other pictures. `AMB` is natural sound, kept low.
   Writes `frames/`, `voice.wav`, `amb.wav`, `segs.json`.
3. `python3 trw.py voice16.wav words_cut.json` : transcribe the voice stem. Any word with low confidence gets a second
   look: try a slightly different in or out point, or trim it. Captions say what is audible.
4. `fix_frames.py` : punch in on a laptop, lift a backlit shot, blur anything private (reads `frames_raw/`, writes `frames/`).
5. Cards: `maps_card.py` turns a phone screen recording into card frames (`m/`) and keeps a soft blur on the start of the
   route in every frame (it follows the blue location dot as the map pans and zooms). Look at its check sheet before
   using the card. `sb.js` renders one element of an HTML page to frames.
6. `build_d.py` : captions typed by hand per line with source word times, pills, cards, tick list. Writes `data.json`.
7. Stills, then the full render with the template's `render.js`.
8. Sound, one of two ways. Transcribe `mix.wav` afterwards and compare with the captions.
   - No music: `MUSIC=0 python3 snd_d.py && ./mix_nomusic.sh` : voice on top, natural sound about 10 dB under it, light
     effects, nothing tonal. Loudness is set from the speech so quiet stretches stay quiet.
   - With a score: `python3 snd_d.py && ./mix_d.sh`.
9. `./encode_d.sh ../../video_out/<topic>_minimal_v1.mp4` and check the finished file.

## Checks that mattered

- **Privacy pass on every screen.** A Maps recording opened on a home address and recent searches: start the clip
  after them. The route started at the place he was staying: blur the start of the route and the name next to it. A meeting title showed the other person's name: blur it. An inbox was visible: do not use the shot.
- **Other people.** Avoid shots where a passer-by or staff member's face is close to camera.
- **The brief against the footage.** If the brief says one thing and the speaker says another on camera, the edit
  says what the footage shows.
- **Quiet, distant speech** (filmed from across a table) does not survive clean-up. Carry that beat with a pill.
- **A spoken line over a shot of him not saying it looks wrong.** Put voiceover lines over point-of-view or scenery shots.
- **Captions never hang over a cut.** `build_d.py` clears the last group of a line before the next shot.
