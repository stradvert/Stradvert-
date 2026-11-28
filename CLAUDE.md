# Stradvert: notes for Claude

Stradvert is a street interview ad agency (stradvert.org). This repo holds the prospect outreach tool
(`prospect_tool/`, the `/prospect` command) and the video edit pipelines (`video/`).

**This repository is public.** Never commit raw footage, frames, transcripts, call recordings or call data,
client figures, private rules, credentials or anything personal. Code and public-facing copy only. The
`.gitignore` already blocks the usual working files under `video/`.

## Video edits: two saved styles

| Style | Skill | When to use |
| --- | --- | --- |
| Minimal portrait reel | `minimal-edit` | The default. Most edits. |
| Trailer, high production | `trailer-edit` | Only when asked for trailer, high production, intense or premium. |

Ryan (founder) said on 27 Nov 2026 that the portrait edits are the majority of his edits and the trailer
edit is for when he wants something more intense. Claude's reading of that: if no style is named, build minimal.

Templates, each with a README:

- `video/minimal_portrait_reel/` : data-driven template for the minimal style.
- `video/claude_founder_reel/` : the first minimal edit. Has the quote card and ranking card to copy.
- `video/day_in_the_life/` : story edit with no voiceover (day in the life), built on the minimal template.
- `video/square_trailer_edit/` : trailer style as a square inside a 1080x1920 canvas (daylight footage).
- `video/sales_call_montage/` : trailer style at 1920x1080 (dark call footage).
- `video/raw_review/` : tools for long raws (transcript with host and guest labels, b-roll finder, selects reel, clean-cut tools: loudness strip, word aligner, cut check).
- `video/counter_reel/` : counter edit (a run of no's with X tiles, then the yes), halfway between minimal and trailer.

## Video rules (every edit)

1. No em dashes or en dashes in any on-screen text or caption. Hyphens only inside compound words.
2. The only link on screen is stradvert.org.
3. Graphics show only what is said in the video. Any number on screen must be spoken in the video. No new claims.
4. B-roll: only footage of Ryan, his shoots or his clients' ads. No stock footage, no AI-generated footage.
   Use it only where it shows what is being said, muted, colour matched, and never the same clip twice
   (the end card wall counts). Report which Drive file every shot came from.
5. A recreated screen or search result is labelled "recreated from the call". Never a real company's logo or
   interface. Another speaker gets a role label, never a name.
6. If the source file has captions burned in, ask for the clean file before starting.
7. For a raw, suggest the cut first unless told to go ahead.
8. Audience is founders and marketers who buy ads. Not creators.
9. The private word list, client figures and claims rules are not in this repo because it is public. Before any
   claim, client name, number or link goes on screen, use the brief pasted in the session and Ryan's account
   skills (`stradvert-standing-facts`, `stradvert-proof-vault`). If neither is available, ask him for the hard rules.

How rule 3 works when there is no voiceover (day in the life, 27 Nov 2026): pills may tell the story Ryan gave in
his brief, in plain facts from the footage or the brief. Still no performance claims and no client names. If his
brief and what he says on camera disagree, the edit says what the footage shows, and the reply tells him.

Coached answers: raw footage can contain answers given after someone was asked to pretend or make something up.
Those are never used as genuine, and any line on camera about faking stays out, because it undercuts the pitch that
street ads are real. The honest answer a person gave first can still be used. Point these out to Ryan in the reply.

Counter edits (Ryan's idea, 27 Nov 2026: "a bunch of no's and a counter til we get someone who does"): count only
asks with an answer on camera, keep them in the real order, and the number on screen matches the asks shown. Template
and the shape that worked: `video/counter_reel/`. On 27 Nov 2026 he asked for this one "somewhere halfway between"
the two saved styles, and for every cut to be clean.

Privacy pass before any screen goes in an edit: screen recordings and laptop shots can show a home address, recent
searches, an inbox or a prospect's name. Trim or blur them and say so in the reply. A prospect's brand stays off
screen unless it is on the proof page. Ryan said "dont show my address" about a Maps recording (27 Nov 2026):
that covers where he is staying too, so the start of a route and the name of the villa are blurred.

Music: on the first day in the life (27 Nov 2026) Ryan asked for the music to be taken out. That is one video so
far. Claude's reading: day in the life and vlog style edits go out with voice, natural sound and light effects,
and it is worth asking before adding a score to any edit.

Meme cutaways (28 Nov 2026): Ryan asked for a funny photo after a "dodgy downloads" punchline and sent a mix of memes.
Claude used the one with no real person in it (a cat with human hands). Claude's reading: a cutaway gag never uses a
real person's face or body as the punchline, because the edit then mocks or sexualises them on a brand account.

One exception so far to rule 4. On 27 Nov 2026 Ryan asked for a "I could fake this view" moment to swap the
background to somewhere that looks really bad, then put it back. No such footage exists, so Claude generated
the background locally with an open-licence image model and labelled it "Fake view" on screen. That was
Claude's call for that one gag. Do not use generated imagery anywhere else without asking him.

Clip inserts (28 Nov 2026): a guest described an old file-sharing spam recording and Ryan sent the clip and asked for it
to go in. YouTube blocks downloads from the cloud server, so he screen recorded it. It plays as audio in a retro player
window with a visualiser drawn from its sound, cut before the recording plugs a website (the only link is stradvert.org).
That is a second exception to rule 4, made at his request. Ask before using anyone else's media in another edit.

## Delivery

- Rendered MP4 into `video_out/` (git-ignored), named `<topic>_<style>_v<N>.mp4`, sent with the file tool.
- Portrait 1080x1920 for reels. For LinkedIn and X he wants a square edit placed inside a 1080x1920 canvas
  (27 Nov 2026): headline above, link below, everything that matters inside the centre 4:5 so feed crops keep it.
- If the location is the point of the video, show it off: sharp, bright, as little text over it as possible.
- Reply short. Say which Drive file each b-roll shot came from and what could not be verified.
- Always true and worth saying: audio is checked by measurement and transcription, not by ear, so he should
  listen once before posting. Any music is synthesised in code. The logo in the templates is an SVG redraw of
  his logo, swap in the real file if he uploads it.

## Working practice

- Copy a template into the session scratch folder and work there. Do not render inside the repo.
- Look at stills of every scene before a full render. Check the finished file, not the working files.
- Commit code only, to the session branch. No pull request unless asked.

## Environment notes (cloud sessions)

- Hosts the video work needs allowed in the environment: `drive.google.com`, `drive.usercontent.google.com`
  (Drive downloads) and `huggingface.co` with its CDN hosts (speech, matting and image models). GitHub release
  downloads work without changes.
- Drive download: `curl -L "https://drive.usercontent.google.com/download?id=<ID>&export=download&confirm=t" -o raw.mp4`.
  The file must be shared by link. If the result is an HTML page, it is not.
- Python: `numpy scipy opencv-python-headless pillow onnxruntime faster-whisper` (plus `transformers` for the
  image generator's tokenizer). Node with Playwright is preinstalled.
- Memory is about 16 GB shared by everything in the session. Do not run matting, image generation and a
  render at the same time.
