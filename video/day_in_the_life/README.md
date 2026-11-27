# Story edit: a day in the life (minimal style, worked example)

A montage with no voiceover: the story is carried by short pills, the speaker's own lines are captioned, and the
music follows the story. It renders with the minimal template in `../minimal_portrait_reel/` (copy `comp.html`,
`render.js` and `fonts/` from there). This folder holds the parts that are specific to a story edit.

No footage, frames, transcripts or `data.json` live in this repo.

## Shape that worked

1. **Hook (0 to 3s):** the strangest picture in the footage first, with the context pill already on screen in
   frame one, a bracketed second line half a second later, and one clear spoken line.
2. **Rewind:** "The plan", told fast (phone screen recording as a card).
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
5. Cards: a phone screen recording cropped to the screen (`m/`), or a page rendered to frames (`sb.js` renders one
   element of an HTML page, frame by frame).
6. `build_d.py` : captions typed by hand per line with source word times, pills, cards, tick list. Writes `data.json`.
7. Stills, then the full render with the template's `render.js`.
8. `python3 snd_d.py && ./mix_d.sh` : score and effects from the segment times, then the mix. Transcribe `mix.wav`
   and compare with the captions.
9. `./encode_d.sh ../../video_out/<topic>_minimal_v1.mp4` and check the finished file.

## Checks that mattered

- **Privacy pass on every screen.** A Maps recording opened on a home address and recent searches: start the clip
  after them. A meeting title showed the other person's name: blur it. An inbox was visible: do not use the shot.
- **Other people.** Avoid shots where a passer-by or staff member's face is close to camera.
- **The brief against the footage.** If the brief says one thing and the speaker says another on camera, the edit
  says what the footage shows.
- **Quiet, distant speech** (filmed from across a table) does not survive clean-up. Carry that beat with a pill.
- **Captions never hang over a cut.** `build_d.py` clears the last group of a line before the next shot.
