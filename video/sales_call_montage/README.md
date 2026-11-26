# Sales call montage (premium pass)

Pipeline that turns a call recording into a cinematic montage: cut-out subject with a blurred, darkened
background, big type behind the speaker, 3D graphic scenes, motion blur and a finishing pass.

Private inputs are not in this repo: the call recording, the transcript, word timings and the scene data
(`data.json`, `scenes.json`, `words.json`). Rebuild them from the source footage.

## Steps

1. Cut the scenes and process the voices (per-scene cut list, noise removal, voice disguise for the other speaker).
2. `python3 rvm.py <model.onnx> 0.4 all al` : video matting, one alpha matte per frame.
3. `python3 prep.py` : filmic grade, per-scene skin and exposure correction, cut-outs (`fg/`) and blurred plates (`bg/`).
4. Build `data.json` (scene times, word timings, head track) for the composition.
5. `node render3.js full 0 <frames> 4` : renders `comp.html` in headless Chrome with several sub-frame samples per frame.
6. `python3 snd3.py && ./mix.sh` : synthesised stereo score and sound design, then the voice, music and effects mix.
7. `./finish.sh out.mp4` : blends sub-frames (motion blur), adds bloom, halation, lens softness and grain, encodes H.264.

## Files

- `comp.html`, `comp.css`, `comp.js` : the composition. `render(frame, sub)` is deterministic.
- `grade.py`, `prep.py`, `rvm.py` : colour and matting.
- `snd3.py`, `mix.sh` : sound.
- `render3.js`, `blend.py`, `finish.sh` : render and finishing.
