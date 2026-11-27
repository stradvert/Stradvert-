# Raw review: long street interview raws

Turns an hour of street interviews into a labelled transcript, a b-roll list and a selects reel, so hooks can be
picked before anything is edited. No footage, transcripts or results are stored here.

## Steps

```bash
ffmpeg -i raw.mov -vn -ac 1 -ar 16000 a16.wav
```

```bash
python3 transcribe.py a16.wav segs
```

Writes `segs.jsonl` line by line as it goes (about twice real time on 4 CPU cores), then `segs.words.json`.

```bash
python3 speakers.py a16.wav models/wespeaker_r34.onnx 2
```

Voice embeddings every half second (about 4 minutes for an hour of audio).

```bash
python3 label.py segs.jsonl
```

`turns.json`: who is talking, HOST or GUEST. The host is the one voice heard right across the file. Labels are
right on long turns and rough on fast back and forth, so check a line against the footage before quoting it.

```bash
python3 broll.py raw.mov
```

`broll.json` and `broll_sheet.jpg`: stretches with no guest speech and a moving camera (walking shots).

```bash
python3 selects.py raw.mov clips.json selects.mp4
```

A review reel. `clips.json` is a list of `[start_s, end_s, "LABEL"]`, and each clip is labelled with its raw timecode.

## When reading the transcript

- Mark any answer given after someone was asked to pretend or make something up. Those never go out as genuine.
  The honest answer they gave first can still count.
- For a counter edit, count only asks with an answer on camera, keep them in the real order, and make the number
  on screen match the asks shown.
- Check who people are before captioning a place: tourists in Times Square are "people in New York", not "New Yorkers".

## Models

- Speech: faster-whisper `medium.en` (downloads on first run; set `HF_HUB_DISABLE_XET=1` if it stalls).
- Voices: wespeaker ResNet34-LM, ONNX, CC BY 4.0, from `Wespeaker/wespeaker-voxceleb-resnet34-LM` on Hugging Face
  (`voxceleb_resnet34_LM.onnx`). Not stored in this repo.
