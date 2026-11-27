# Video edit pipelines

HTML compositions rendered frame by frame in headless Chrome, encoded with ffmpeg. Sound is synthesised in Python.
No footage, frames, transcripts or scene data are stored here.

| Folder | Style | Frame |
| --- | --- | --- |
| `minimal_portrait_reel/` | Minimal (the default edit), data-driven template | 1080x1920 |
| `claude_founder_reel/` | Minimal, first version, with quote and ranking cards | 1080x1920 |
| `square_trailer_edit/` | Trailer, square picture inside a portrait canvas | 1080x1920 |
| `sales_call_montage/` | Trailer, widescreen | 1920x1080 |

Which style to use and the rules for every edit are in the repo `CLAUDE.md` and the two skills in
`.claude/skills/` (`minimal-edit`, `trailer-edit`).
