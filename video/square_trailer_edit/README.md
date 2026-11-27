# Square trailer edit inside a portrait canvas (high production)

Output is 1080x1920. The picture is a 1080x1080 square at y 480 to 1560, with the hook as a headline above it
and a progress bar and the link below. Everything that matters sits inside the centre 4:5 so LinkedIn and X
feed crops keep it. Inside the square: the speaker is cut out from the footage and sits in front of big type,
the location stays sharp and bright, stats count up, cards and charts fly in with 3D, cuts get flashes and
glitches, every frame is rendered several times for real motion blur, then a finishing pass adds bloom,
halation, lens softness and grain. Score and sound design are synthesised.

`comp.js`, `build_s.py` and `cut_s.py` are the worked example from the Koh Samui "view" video: ten scenes plus
the end card. For a new video keep the helpers and rewrite the scenes. The widescreen version is in
`../sales_call_montage`.

No footage, mattes, transcripts, generated images or `data.json` live in this repo.

## Steps

1. **Source and transcript.** Raw into `raw.mp4`. `ffmpeg -i raw.mp4 -ac 1 -ar 16000 a16.wav`, denoise to
   `dn16.wav`, `python3 tr.py a16.wav words.json`.
2. **Cut.** Edit the scene list `S` in `cut_s.py` (scene key and source times), run it: `parts/`, `cut.mov`,
   `scenes.json`. Transcribe the cut again (`words_cut.json`) and read it against the script.
3. **Frames.** `ffmpeg -i cut.mov -q:v 2 fr/%05d.jpg`
4. **Matting.** `python3 rvm.py models/rvm_resnet50_fp32.onnx 0.4 all al` (about half a second per frame on 4 cores).
5. **Prep.** `python3 prep_s.py` for the skin-matched cut-outs (`fg/`) and head track, then `python3 prep_bgs.py`
   for the plates: `bgs/` (sharp, the `view` grade on location scenes) and `bgm/` (mid blur for focus pulls).
6. **Scene data.** Edit the caption groups in `build_s.py` (`[word]` marks emphasis), run it: `data.json`.
   `node measure.js` prints type widths and flags any caption that will not fit on one line.
7. **Compose.** Write the scenes in `comp.js`. `node render3.js still 40,300,900 test` and look at the stills
   before anything else. Check the type sits beside the head, never on the face.
8. **Sound.** `python3 snd_s.py` (events follow the word times) then `MG=-6 ML=4 SG=-2.5 TARGET=-14 ./mix.sh`.
   `ffmpeg -i mix.wav -ac 1 -ar 16000 mix16.wav && python3 wer.py mix16.wav out.json` transcribes the mix to
   prove the voice still reads under the music.
9. **Render.** `node render3.js full 0 <total frames> 4` (about 20 minutes for 58 seconds).
10. **Finish.** `./finish.sh ../../video_out/<topic>_trailer_v1.mp4` : motion blur blend, finishing pass, H.264.
11. **Check** the finished file: frame sheet across the whole video, strips of consecutive frames at each big
    move, loudness, sync, text rules.

## Files

- `comp.html`, `comp.css`, `comp.js` : composition. `render(frame, sub)` is deterministic, `samples(frame)` picks 6 or 2 sub-frames. `canvasUI()` drives the headline, progress bar and footer outside the square.
- `cut_s.py`, `build_s.py` : cut list and scene data (worked example).
- `rvm.py`, `grade.py`, `prep_s.py`, `prep_bgs.py` : matting, grade, cut-outs, plates.
- `snd_s.py`, `mix.sh`, `wer.py` : score, sound design, mix, intelligibility check.
- `render3.js`, `blend.py`, `finish.sh`, `measure.js` : render, motion blur, finishing, layout checks.
- `fakebg_lcm.py`, `fakebg_tiles.py` : the generated "fake view" background (see below).

## Building blocks in comp.js

`plate()` footage with head tracking, dim and focus pull. `typeLine()` big letter-by-letter type with gradient and
light sweep. `captions()` one-line word-by-word captions. `statBlock()` label, big number, sub lines.
Scenes show: type behind the subject, stat count-up, b-roll phone card with picture in picture and tick chips,
comparison cards, a full background replacement with a scan-line wipe (the fake view), duotone treatment with a
scan line, chart card with bars, mirrored word that flips, struck-through phrase, TV wall end card with an
extruded link.

## The fake view

For the line "I could fake this view", the whole background behind the cut-out is swapped for an image of a
grim place and then wiped back, with "Fake view" and "Real view" tags on screen. The camera was locked off, so
the still needs no tracking (check that first: far-field shift between frames should be under a pixel).
The image was generated locally: `fakebg_lcm.py` runs an open-licence latent consistency model with onnxruntime
only (no PyTorch), `fakebg_tiles.py` upscales it in memory-safe tiles. Blur it to the softness of the real
background and flatten the colour a little so it sits with the footage. This is the only place generated
imagery is used, and only because the line is about faking it.

## Models and requirements

- Robust Video Matting: `rvm_resnet50_fp32.onnx` from the RobustVideoMatting v1.0.0 release on GitHub.
- Voice denoise: `bd.rnnn` from the rnnoise-models repository (set `MODELS=<dir>` for `cut_s.py`).
- Image model for the fake view: `SimianLuo/LCM_Dreamshaper_v7` on Hugging Face (MIT licence, ONNX files).
- Python: `numpy scipy opencv-python-headless pillow onnxruntime faster-whisper transformers`. Node with Playwright. ffmpeg.
- The end card wall needs `wall/<name>/%04d.jpg` clips (440x330, about 168 frames each) cut from your own ads.
