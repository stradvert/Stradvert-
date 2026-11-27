---
name: minimal-edit
description: Stradvert's default video edit, used for most videos. Clean portrait reel (1080x1920) with word-by-word captions, white headline pills, b-roll cards, a progress bar and a logo end card. Use when asked to edit a raw or a clip and no style is named, or for a "minimal", "clean", "simple", "normal" or "usual" edit. For the intense trailer look use trailer-edit instead.
---

# Minimal edit (the default)

Ryan said (27 Nov 2026) the portrait edits are the majority of his edits, and the trailer edit is for when he
wants something more intense. Claude's reading of that: when no style is named, build this one.

Template: `video/minimal_portrait_reel/` (steps and `data.json` fields are in its README). Custom cards to copy
from: `video/claude_founder_reel/comp.html`.

## The look

- 1080x1920, 30 fps. Full-bleed footage, face about a third down the frame, slow push-in on every shot, hard jump cuts on pauses.
- Colours: near-black `#111`, white, one accent `#FCEF00`. Font: Montserrat 500 to 800.
- **Captions:** 2 to 4 words, one line, weight 800 at 64px on a dark rounded plate. The word being spoken sits on a yellow block with dark text. Verbatim, split on pauses and punctuation.
- **Pills:** white rounded headline at the top, one idea each, key words get a yellow wipe. One on screen at a time, 3 to 5 per video.
- **B-roll:** a rounded card in the top half while the talking head shrinks into a card underneath. 2.5 to 3.5 seconds each, slow zoom. Use it to break up long stretches of talking head.
- **Cards:** quote card, ranking, status card. Only when they show something said in the video.
- Thin yellow progress bar on the top edge. End card: logo and a white pill with the link, about 2 seconds.
- **Sound:** soft pad and a light pluck, a whoosh on layout changes, a tick on highlights. Voice clearly on top, about -14 LUFS.
- Not in this style: cut-outs, big type behind the speaker, flashes, glitches, count-ups. Calm and readable is the point.

## How to build

1. Follow the steps in `video/minimal_portrait_reel/README.md` in a scratch folder. Copy the template there, do not render inside the repo.
2. For a raw: transcribe, then **suggest the cut first** (hook, best moments, length) unless told to go ahead. Keep the hook that is already there if it works.
3. Fill `data.json`: captions from `caps.py`, then pills, b-roll and timings by hand. Read every caption against the audio.
4. Render stills and look at them before the full render. Fix anything over the face, off the frame or wrapping.
5. `snd.py`, `encode.sh`, then check the finished file, not the working files.

## Story edits (day in the life, no voiceover)

Worked example and scripts: `video/day_in_the_life/` (its README has the shape and the checks).

- Open on the strangest picture in the footage with the context pill already on screen in frame one. The bracketed second line lands half a second later. One clear spoken line in the first two seconds.
- Then rewind and tell it in order. Ryan's own lines carry the story as captions, pills fill the gaps, one idea per shot.
- Stop the music for the punchline. Bring it back on the next cut.
- Phone screen recordings and pages he showed on a call go in as tall cards over the dimmed footage. A workflow reads best as a three-row tick list.
- Do the privacy pass on every screen before it goes in (see `CLAUDE.md`).
- If the brief and the footage disagree, cut what the footage shows and tell him.

## Rules

Follow "Video rules" in the repo `CLAUDE.md`. They are short and they are hard rules.

## Checks before sending

- Frame sheet across the whole video viewed, plus the first frame (it is the thumbnail, never black or blank).
- Captions match the spoken words (transcribe the final mix and compare).
- Every number, name and claim on screen is spoken in the video. Only link on screen is the site.
- No em dashes or en dashes in any on-screen text.
- Loudness about -14 LUFS, peaks under -1 dBFS, picture and sound in sync.
- Length inside what was asked.

## Deliver

Rendered MP4 in `video_out/<topic>_minimal_v<N>.mp4`, sent with the file tool. Reply short: what the cut is,
which Drive file each b-roll shot came from, and anything that could not be verified. Audio is checked by
measurement and transcription only, so say that he should listen once before posting.
