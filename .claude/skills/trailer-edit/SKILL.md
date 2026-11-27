---
name: trailer-edit
description: Stradvert's high production "trailer" edit. The speaker is cut out from the footage with big type behind them, stat count-ups, 3D cards and charts, flash and glitch cuts, real motion blur, bloom and grain, and a full synthesised score. Square, 16:9 or portrait. Use only when asked for a "trailer", "high production", "intense", "premium" or "super high" edit, or "like the call montage" or "like the Koh Samui one". Otherwise use minimal-edit.
---

# Trailer edit (high production)

Ryan said (27 Nov 2026) most edits are the minimal portrait style, and this one is for when he wants
something more intense. Claude's reading of that: only build this when he asks for it by name or by reference.

Templates: `video/square_trailer_edit/` (1080x1080, daylight footage, worked example with ten scenes) and
`video/sales_call_montage/` (1920x1080, dark call footage). Steps are in each README. Budget about two hours
end to end for a one minute video: matting, prep and render are the slow parts.

## The look

- Speaker cut out with video matting and placed over the same footage, so type and graphics can sit **behind** them.
- Big condensed type (Anton) with a gradient fill, glow and a light sweep, landing letter by letter on the key word. Yellow `#FCEF00` for the word that matters, white for the rest. Wide italic Archivo for labels.
- Captions: one line at the bottom, words appear as spoken, emphasised words in wide yellow italic caps, next word ghosted.
- One graphic idea per scene: stat with a count-up, comparison cards, chart card with bars, b-roll in a tilted card with picture in picture, a background-only wipe, a duotone treatment with a scan line, a struck-through phrase.
- Cuts: white flash, a two-frame negative, RGB split, whip between locations, punch-in on every shot. Light camera shake and impact shakes on the hits.
- Motion blur from 6 sub-frames on busy frames and 2 on quiet ones. Finishing pass: bloom, warm halation, slight lens softness, fine grain.
- End card: wall of old TVs playing his ads in grey behind the logo and an extruded link.
- Sound: tempo fitted to the picture events, pad, sub bass, piano motif, pulse, drums, plus a hit, riser, whoosh or tick on every graphic. Music lows stay up, music mids duck under the voice. About -14 LUFS.

## Formats

- **LinkedIn and X:** a 1080x1080 picture inside a 1080x1920 canvas (Ryan asked for this on 27 Nov 2026: "a square within the portrait"). Picture at y 480 to 1560, the hook as a headline above it, progress bar and link below. Keep everything that matters inside the centre 4:5 (y 285 to 1635) so feed crops do not cut it. `video/square_trailer_edit/` is built this way.
- **Widescreen 1920x1080:** `video/sales_call_montage/`.
- Captions and graphics stay inside the picture, so the picture still works if a platform crops to it.

## How to build

1. Follow the steps in the template README in a scratch folder. Keep the helpers (`plate`, `typeLine`, `captions`, `statBlock`), rewrite the scenes for the new script.
2. For a raw: transcribe, then **suggest the cut first** unless told to go ahead. One scene per idea, 3 to 7 seconds each.
3. Render stills of every scene before the full render. Most of the work is fixing what the stills show.
4. Sound after the picture is locked, because every sound follows a word time.
5. Full render, finishing pass, then check the finished file.

## What went wrong before (so it does not again)

- **Type hidden by the head.** The free column beside a close-up speaker is narrow. Measure every big word with `measure.js` and size it to fit. A letter tucked behind the hair is fine, a hidden word is not. Numbers must always be fully readable.
- **Background lost.** If the location is the point (he asked for square to keep the view), show it off. After the first cut Ryan said the view was not coming through, so: sharp plate with no added blur, the brighter `view` grade that keeps cloud detail, a light caption scrim, the speaker framed to one side, small punch-ins, and blur or dim only while big type is up.
- **"Fake" gags.** When he says he could fake something, make the fake obvious and funny, then put the real thing back (he asked for the view to swap to "somewhere really bad"). The camera was locked off, so a still background needed no tracking. Label it on screen ("Fake view", then "Real view"). A generated image was used once for this and is the only allowed use of generated imagery, ask before doing it again.
- **Captions wrapping.** Keep each group on one line. Split the group, do not shrink the type.
- **B-roll repeated.** A clip used as b-roll must not also play on the end card wall. Swap the wall tiles.
- **Blown-out sky.** Daylight footage needs the higher bloom threshold in `square_trailer_edit/finish.sh`. The call settings are for dark footage.
- **Black first frame.** No fade in from black. The first frame is the thumbnail.
- **Pink or grey skin.** Pull skin hue per pixel towards a natural tone and match exposure per scene (`prep`), and check stills of every scene.
- **Count-ups.** Keep them under a second and end exactly on the spoken number.
- **Effect labels.** A label on a simulated effect says what the edit shows ("Fake view"). Never claim a tool made it.
- **Reading off notes.** When he looks down to read, let a graphic carry the scene.

## Rules

Follow "Video rules" in the repo `CLAUDE.md`. They are short and they are hard rules.

## Checks before sending

- Frame sheet across the whole finished file, strips of consecutive frames at each big move, and the first frame.
- Transcribe the final mix and compare with the clean voice: word error should stay within a couple of percent.
- Loudness about -14 LUFS, peaks under -1 dBFS, cuts land on the expected frames, audio in sync.
- Scan every on-screen string for em dashes, en dashes, and anything on the private word list. Only link on screen is the site.
- Every number on screen is spoken in the video. Length inside what was asked.

## Deliver

Rendered MP4 in `video_out/<topic>_trailer_v<N>.mp4`, sent with the file tool. Reply short: the cut, which Drive
file each b-roll shot came from, and anything that could not be verified (stat sources, music is synthesised,
audio checked by measurement and transcription only, so he should listen once before posting).
