# Stradvert Intro — Design

## Style Prompt

Cinematic dark premium. Navy-tinted near-black canvas with a soft steel-blue radial glow breathing behind a single authoritative serif wordmark. Weight, stillness, gravity — the register of a luxury tech reveal. Entrances use slow, decisive eases (`power4.out`, `expo.out`, `sine.out`) — no bounce, no elasticity. The title arrives like a statement, not an announcement.

## Colors

From `palettes/dark-premium.md` row 4:

- `#0D1321` — background (deep navy near-black)
- `#1D2D44` — background depth glow (lifted panel tint)
- `#3E5C76` — muted
- `#748CAB` — accent (steel blue)
- `#F0EBD8` — foreground (warm off-white)

## Typography

- **Fraunces** — serif, weight 900, for the wordmark. Optical-size display, subtle contrast. Not one of the banned defaults.
- **DM Sans** — sans, weight 300, for overline and tagline. Clean, neutral counterweight.

Pairing tension: editorial serif (human, authored) vs. geometric sans (systemic, operational) — fits "AI outreach" concept.

## Motion

- Entrances only (single scene — no transitions, no exits).
- Vary eases: `sine.out`, `expo.out`, `power4.out`, `power2.out`.
- Pacing: slow (0.7–1.4s) for cinematic weight.
- Ambient: glow opacity breathing (not scale — zoom is the default LLM reach).

## What NOT to Do

- No gradient text (`background-clip: text`).
- No cyan-on-dark or purple-to-blue gradients.
- No pure `#000` — always tint navy.
- No elastic/bounce easing — register is premium, not playful.
- No exit animations — single scene ends held, not dissolving.
