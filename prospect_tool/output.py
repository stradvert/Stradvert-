"""Document output module - generates clean .docx, .txt and animated .html files for VA use."""

import os
import re
import html
import logging
from datetime import datetime

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

logger = logging.getLogger(__name__)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")


def ensure_output_dir():
    """Create output directory if it doesn't exist."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def sanitize_filename(name: str) -> str:
    """Make a brand name safe for use as a filename."""
    return re.sub(r"[^\w\s-]", "", name).strip().replace(" ", "_")


def generate_txt(
    brand_name: str,
    brand_analysis: str,
    outreach_messages: str,
    output_dir: str = None,
) -> str:
    """Generate a clean .txt file with all outreach content.

    Returns the path to the created file.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    ensure_output_dir()

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(brand_name)
    filename = f"{safe_name}_outreach_{date_str}.txt"
    filepath = os.path.join(output_dir, filename)

    lines = []
    lines.append("=" * 70)
    lines.append(f"STRADVERT OUTREACH PACK - {brand_name.upper()}")
    lines.append(f"Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("")

    # Brand analysis section
    lines.append("-" * 70)
    lines.append("BRAND RESEARCH BRIEF")
    lines.append("-" * 70)
    lines.append("")
    lines.append(brand_analysis)
    lines.append("")
    lines.append("")

    # Outreach messages section
    lines.append("-" * 70)
    lines.append("OUTREACH MESSAGES - READY TO COPY & SEND")
    lines.append("-" * 70)
    lines.append("")
    lines.append(outreach_messages)
    lines.append("")
    lines.append("")

    # Footer
    lines.append("=" * 70)
    lines.append("END OF OUTREACH PACK")
    lines.append(f"Agency: Stradvert | streetscaled.com")
    lines.append("=" * 70)

    content = "\n".join(lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info("Created TXT: %s", filepath)
    return filepath


def generate_docx(
    brand_name: str,
    brand_analysis: str,
    outreach_messages: str,
    output_dir: str = None,
) -> str:
    """Generate a clean .docx file with all outreach content.

    Returns the path to the created file.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    ensure_output_dir()

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(brand_name)
    filename = f"{safe_name}_outreach_{date_str}.docx"
    filepath = os.path.join(output_dir, filename)

    doc = Document()

    # Set default font
    style = doc.styles["Normal"]
    font = style.font
    font.name = "Arial"
    font.size = Pt(11)
    font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Title
    title = doc.add_heading(f"Stradvert Outreach Pack", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # Subtitle with brand name and date
    subtitle = doc.add_paragraph()
    run = subtitle.add_run(f"{brand_name}")
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
    subtitle.add_run(
        f"\nGenerated: {datetime.now().strftime('%B %d, %Y')}"
    ).font.size = Pt(10)

    doc.add_paragraph("")  # spacer

    # Brand Research Brief
    doc.add_heading("Brand Research Brief", level=1)

    # Split analysis into paragraphs and add them
    for block in brand_analysis.split("\n\n"):
        block = block.strip()
        if not block:
            continue

        # Check if it's a heading (starts with ** or #)
        if block.startswith("**") and block.endswith("**"):
            heading_text = block.strip("*").strip()
            doc.add_heading(heading_text, level=2)
        elif block.startswith("#"):
            heading_text = block.lstrip("#").strip()
            doc.add_heading(heading_text, level=2)
        else:
            # Handle bold markers within text
            p = doc.add_paragraph()
            parts = re.split(r"(\*\*.*?\*\*)", block)
            for part in parts:
                if part.startswith("**") and part.endswith("**"):
                    run = p.add_run(part.strip("*"))
                    run.bold = True
                else:
                    p.add_run(part)

    doc.add_page_break()

    # Outreach Messages
    doc.add_heading("Outreach Messages - Ready to Copy & Send", level=1)

    instruction = doc.add_paragraph()
    run = instruction.add_run(
        "Copy each message exactly as written. Do not edit. "
        "Each message is ready to send."
    )
    run.italic = True
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.add_paragraph("")  # spacer

    # Split outreach into sections by --- dividers
    sections = re.split(r"\n---+\n", outreach_messages)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        lines = section.split("\n")
        first_line = lines[0].strip()

        # Check if first line is a heading
        if (
            first_line.upper().startswith("DM SCRIPT")
            or first_line.upper().startswith("LINKEDIN")
            or first_line.upper().startswith("INSTAGRAM")
            or first_line.upper().startswith("FOLLOW")
            or first_line.upper().startswith("EMAIL")
        ):
            doc.add_heading(first_line, level=2)
            message_body = "\n".join(lines[1:]).strip()
        else:
            message_body = section

        if message_body:
            # Add the message in a slightly indented, distinct style
            for para_text in message_body.split("\n\n"):
                para_text = para_text.strip()
                if not para_text:
                    continue

                # Channel label lines
                if para_text.startswith("[") and para_text.endswith("]"):
                    p = doc.add_paragraph()
                    run = p.add_run(para_text)
                    run.italic = True
                    run.font.size = Pt(9)
                    run.font.color.rgb = RGBColor(0x88, 0x88, 0x88)
                else:
                    p = doc.add_paragraph()
                    p.paragraph_format.left_indent = Inches(0.25)
                    # Handle any remaining bold markers
                    parts = re.split(r"(\*\*.*?\*\*)", para_text)
                    for part in parts:
                        if part.startswith("**") and part.endswith("**"):
                            run = p.add_run(part.strip("*"))
                            run.bold = True
                        else:
                            p.add_run(part)

        # Add a line break between sections
        doc.add_paragraph("")

    # Footer
    footer_para = doc.add_paragraph()
    footer_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_para.add_run("Stradvert | streetscaled.com")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x99, 0x99, 0x99)

    doc.save(filepath)
    logger.info("Created DOCX: %s", filepath)
    return filepath


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Stradvert Outreach Pack - __BRAND_NAME__</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/0.160.0/three.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js"></script>
<style>
  :root {
    --bg: #0f1115;
    --panel: rgba(23, 26, 33, 0.78);
    --text: #e7e9ee;
    --muted: #9aa3b2;
    --accent: #ff5a1f;
    --accent-2: #ffb347;
    --border: rgba(255, 255, 255, 0.08);
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; background: var(--bg); color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; line-height: 1.6; }

  #shader-bg {
    position: fixed; inset: 0; width: 100vw; height: 100vh;
    z-index: 0; pointer-events: none; opacity: 0.55;
  }
  .wrap { position: relative; z-index: 1; max-width: 860px; margin: 0 auto; padding: 64px 28px 96px; }

  @keyframes fadeInUp {
    from { opacity: 0; transform: translate3d(0, 24px, 0); }
    to   { opacity: 1; transform: translate3d(0, 0, 0); }
  }
  @keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position: 200% 0; }
  }
  @keyframes pulse {
    0%, 100% { transform: scale(1); opacity: 1; }
    50%      { transform: scale(1.08); opacity: 0.85; }
  }
  @keyframes float {
    0%, 100% { transform: translateY(0); }
    50%      { transform: translateY(-6px); }
  }

  .hero {
    padding: 48px 0 32px;
    border-bottom: 1px solid var(--border);
    animation: fadeInUp 0.9s ease both;
    display: flex; align-items: center; justify-content: space-between; gap: 24px;
  }
  .hero-text { flex: 1; min-width: 0; }
  #lottie-hero { width: 140px; height: 140px; flex-shrink: 0; }

  .eyebrow {
    display: inline-block;
    font-size: 12px; letter-spacing: 0.25em; text-transform: uppercase;
    color: var(--accent); margin-bottom: 14px;
    animation: float 3.2s ease-in-out infinite;
  }
  h1 {
    font-size: 44px; margin: 0 0 10px;
    background: linear-gradient(90deg, var(--accent), var(--accent-2), var(--accent));
    background-size: 200% 100%;
    -webkit-background-clip: text; background-clip: text; -webkit-text-fill-color: transparent;
    animation: shimmer 6s linear infinite;
  }
  .meta { color: var(--muted); font-size: 14px; }

  .dot {
    display: inline-block; width: 8px; height: 8px; border-radius: 50%;
    background: var(--accent); margin-right: 8px;
    animation: pulse 1.8s ease-in-out infinite;
  }

  h2 { font-size: 26px; margin: 56px 0 16px; padding-bottom: 8px; border-bottom: 1px solid var(--border); }
  h3 { font-size: 18px; margin: 24px 0 10px; color: var(--accent-2); }

  .section, .card { opacity: 0; }

  .card {
    background: var(--panel);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 22px 24px; margin: 16px 0;
    transition: transform 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease;
  }
  .card:hover {
    transform: translateY(-3px);
    border-color: var(--accent);
    box-shadow: 0 10px 30px rgba(255, 90, 31, 0.12);
  }

  .channel-label {
    display: inline-block; font-size: 11px; letter-spacing: 0.2em; text-transform: uppercase;
    color: var(--muted); margin-bottom: 8px;
  }
  pre {
    white-space: pre-wrap; word-wrap: break-word;
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 14px; color: var(--text); margin: 0;
  }
  .footer {
    margin-top: 80px; padding-top: 24px;
    border-top: 1px solid var(--border);
    text-align: center; color: var(--muted); font-size: 13px;
  }
</style>
</head>
<body>
  <canvas id="shader-bg"></canvas>
  <div class="wrap">
    <header class="hero">
      <div class="hero-text">
        <span class="eyebrow"><span class="dot"></span>Stradvert Outreach Pack</span>
        <h1>__BRAND_NAME__</h1>
        <div class="meta">Generated __GENERATED__</div>
      </div>
      <div id="lottie-hero" aria-hidden="true"></div>
    </header>

    <section class="section">
      <h2>Brand Research Brief</h2>
      __ANALYSIS_HTML__
    </section>

    <section class="section">
      <h2>Outreach Messages &mdash; Ready to Copy &amp; Send</h2>
      <p class="meta">Copy each message exactly as written. No edits needed.</p>
      __MESSAGES_HTML__
    </section>

    <div class="footer">Stradvert &middot; streetscaled.com</div>
  </div>

<script id="vertex-shader" type="x-shader/x-vertex">
  varying vec2 vUv;
  void main() {
    vUv = uv;
    gl_Position = vec4(position, 1.0);
  }
</script>

<script id="fragment-shader" type="x-shader/x-fragment">
  precision highp float;
  varying vec2 vUv;
  uniform float uTime;
  uniform vec2  uResolution;

  // Cheap 2D hash-based noise
  float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
  float noise(vec2 p) {
    vec2 i = floor(p);
    vec2 f = fract(p);
    vec2 u = f * f * (3.0 - 2.0 * f);
    return mix(mix(hash(i + vec2(0,0)), hash(i + vec2(1,0)), u.x),
               mix(hash(i + vec2(0,1)), hash(i + vec2(1,1)), u.x), u.y);
  }
  float fbm(vec2 p) {
    float v = 0.0;
    float a = 0.5;
    for (int i = 0; i < 5; i++) {
      v += a * noise(p);
      p *= 2.02;
      a *= 0.5;
    }
    return v;
  }

  void main() {
    vec2 uv = vUv;
    vec2 p = uv * 2.5;
    float t = uTime * 0.06;
    float n = fbm(p + vec2(t, -t * 0.7));
    float n2 = fbm(p * 1.7 + vec2(-t * 0.5, t));
    vec3 c1 = vec3(0.06, 0.07, 0.09);
    vec3 c2 = vec3(1.00, 0.35, 0.12);
    vec3 c3 = vec3(1.00, 0.70, 0.28);
    vec3 col = mix(c1, c2, smoothstep(0.35, 0.85, n));
    col = mix(col, c3, smoothstep(0.55, 0.95, n2) * 0.45);
    // subtle vignette
    float d = distance(uv, vec2(0.5));
    col *= smoothstep(0.95, 0.25, d);
    gl_FragColor = vec4(col, 1.0);
  }
</script>

<script>
  document.addEventListener("DOMContentLoaded", function () {
    // ---- GSAP scroll-triggered reveals ----
    gsap.registerPlugin(ScrollTrigger);
    gsap.utils.toArray(".section").forEach(function (el) {
      gsap.fromTo(el,
        { opacity: 0, y: 40 },
        { opacity: 1, y: 0, duration: 0.8, ease: "power2.out",
          scrollTrigger: { trigger: el, start: "top 85%" } }
      );
    });
    gsap.utils.toArray(".card").forEach(function (el, i) {
      gsap.fromTo(el,
        { opacity: 0, y: 24, scale: 0.98 },
        { opacity: 1, y: 0, scale: 1, duration: 0.6, delay: i * 0.05,
          ease: "power3.out",
          scrollTrigger: { trigger: el, start: "top 90%" } }
      );
    });

    // ---- Three.js full-screen shader background ----
    (function initShader() {
      var canvas = document.getElementById("shader-bg");
      if (!canvas || typeof THREE === "undefined") return;
      var renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, alpha: true });
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      var scene = new THREE.Scene();
      var camera = new THREE.Camera();
      camera.position.z = 1;

      var uniforms = {
        uTime: { value: 0 },
        uResolution: { value: new THREE.Vector2(window.innerWidth, window.innerHeight) }
      };
      var geometry = new THREE.PlaneGeometry(2, 2);
      var material = new THREE.ShaderMaterial({
        uniforms: uniforms,
        vertexShader: document.getElementById("vertex-shader").textContent,
        fragmentShader: document.getElementById("fragment-shader").textContent
      });
      scene.add(new THREE.Mesh(geometry, material));

      function resize() {
        var w = window.innerWidth, h = window.innerHeight;
        renderer.setSize(w, h, false);
        uniforms.uResolution.value.set(w, h);
      }
      window.addEventListener("resize", resize);
      resize();

      var start = performance.now();
      function animate() {
        uniforms.uTime.value = (performance.now() - start) / 1000;
        renderer.render(scene, camera);
        requestAnimationFrame(animate);
      }
      animate();
    })();

    // ---- Lottie hero animation (inline JSON, no network) ----
    (function initLottie() {
      var container = document.getElementById("lottie-hero");
      if (!container || typeof lottie === "undefined") return;
      var animationData = {
        "v": "5.7.4", "fr": 30, "ip": 0, "op": 90, "w": 200, "h": 200, "nm": "pulse", "ddd": 0, "assets": [],
        "layers": [
          {
            "ddd": 0, "ind": 1, "ty": 4, "nm": "ring", "sr": 1,
            "ks": {
              "o": { "a": 1, "k": [
                { "t": 0, "s": [80] }, { "t": 45, "s": [20] }, { "t": 90, "s": [80] }
              ]},
              "r": { "a": 1, "k": [
                { "t": 0, "s": [0] }, { "t": 90, "s": [360] }
              ]},
              "p": { "a": 0, "k": [100, 100, 0] },
              "a": { "a": 0, "k": [0, 0, 0] },
              "s": { "a": 1, "k": [
                { "t": 0, "s": [80, 80, 100] },
                { "t": 45, "s": [120, 120, 100] },
                { "t": 90, "s": [80, 80, 100] }
              ]}
            },
            "shapes": [
              {
                "ty": "gr", "it": [
                  { "ty": "el", "p": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [80, 80] } },
                  { "ty": "st", "c": { "a": 0, "k": [1, 0.353, 0.122, 1] }, "o": { "a": 0, "k": 100 }, "w": { "a": 0, "k": 6 } },
                  { "ty": "tr", "p": { "a": 0, "k": [0, 0] }, "a": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [100, 100] }, "r": { "a": 0, "k": 0 }, "o": { "a": 0, "k": 100 } }
                ]
              }
            ],
            "ip": 0, "op": 90, "st": 0, "bm": 0
          },
          {
            "ddd": 0, "ind": 2, "ty": 4, "nm": "dot", "sr": 1,
            "ks": {
              "o": { "a": 0, "k": 100 },
              "r": { "a": 0, "k": 0 },
              "p": { "a": 0, "k": [100, 100, 0] },
              "a": { "a": 0, "k": [0, 0, 0] },
              "s": { "a": 1, "k": [
                { "t": 0, "s": [40, 40, 100] },
                { "t": 45, "s": [60, 60, 100] },
                { "t": 90, "s": [40, 40, 100] }
              ]}
            },
            "shapes": [
              {
                "ty": "gr", "it": [
                  { "ty": "el", "p": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [40, 40] } },
                  { "ty": "fl", "c": { "a": 0, "k": [1, 0.702, 0.278, 1] }, "o": { "a": 0, "k": 100 } },
                  { "ty": "tr", "p": { "a": 0, "k": [0, 0] }, "a": { "a": 0, "k": [0, 0] }, "s": { "a": 0, "k": [100, 100] }, "r": { "a": 0, "k": 0 }, "o": { "a": 0, "k": 100 } }
                ]
              }
            ],
            "ip": 0, "op": 90, "st": 0, "bm": 0
          }
        ]
      };
      lottie.loadAnimation({
        container: container,
        renderer: "svg",
        loop: true,
        autoplay: true,
        animationData: animationData
      });
    })();
  });
</script>
</body>
</html>
"""


def _render_analysis_html(brand_analysis: str) -> str:
    """Convert the analysis markdown-ish text into styled HTML blocks."""
    parts = []
    for block in brand_analysis.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        if block.startswith("**") and block.endswith("**"):
            parts.append(f"<h3>{html.escape(block.strip('*').strip())}</h3>")
        elif block.startswith("#"):
            parts.append(f"<h3>{html.escape(block.lstrip('#').strip())}</h3>")
        else:
            escaped = html.escape(block)
            escaped = re.sub(
                r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped
            )
            parts.append(f'<div class="card"><p>{escaped}</p></div>')
    return "\n".join(parts)


def _render_messages_html(outreach_messages: str) -> str:
    """Split messages by --- dividers and wrap each in an animated card."""
    parts = []
    sections = re.split(r"\n---+\n", outreach_messages)
    for section in sections:
        section = section.strip()
        if not section:
            continue
        lines = section.split("\n")
        first_line = lines[0].strip()
        heading_prefixes = ("DM SCRIPT", "LINKEDIN", "INSTAGRAM", "FOLLOW", "EMAIL")
        if first_line.upper().startswith(heading_prefixes):
            heading = html.escape(first_line)
            body = "\n".join(lines[1:]).strip()
            parts.append(
                f'<div class="card">'
                f'<span class="channel-label">{heading}</span>'
                f"<pre>{html.escape(body)}</pre>"
                f"</div>"
            )
        else:
            parts.append(f'<div class="card"><pre>{html.escape(section)}</pre></div>')
    return "\n".join(parts)


def generate_html(
    brand_name: str,
    brand_analysis: str,
    outreach_messages: str,
    output_dir: str = None,
) -> str:
    """Generate a self-contained animated .html file (CSS animations + GSAP).

    Returns the path to the created file.
    """
    if output_dir is None:
        output_dir = OUTPUT_DIR
    ensure_output_dir()

    date_str = datetime.now().strftime("%Y-%m-%d")
    safe_name = sanitize_filename(brand_name)
    filename = f"{safe_name}_outreach_{date_str}.html"
    filepath = os.path.join(output_dir, filename)

    content = (
        HTML_TEMPLATE
        .replace("__BRAND_NAME__", html.escape(brand_name))
        .replace("__GENERATED__", datetime.now().strftime("%B %d, %Y at %I:%M %p"))
        .replace("__ANALYSIS_HTML__", _render_analysis_html(brand_analysis))
        .replace("__MESSAGES_HTML__", _render_messages_html(outreach_messages))
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    logger.info("Created HTML: %s", filepath)
    return filepath


def generate_all(
    brand_name: str,
    brand_analysis: str,
    outreach_messages: str,
    output_dir: str = None,
) -> dict:
    """Generate .txt, .docx and animated .html output files.

    Returns dict with paths to all files.
    """
    txt_path = generate_txt(brand_name, brand_analysis, outreach_messages, output_dir)
    docx_path = generate_docx(
        brand_name, brand_analysis, outreach_messages, output_dir
    )
    html_path = generate_html(
        brand_name, brand_analysis, outreach_messages, output_dir
    )

    return {
        "txt": txt_path,
        "docx": docx_path,
        "html": html_path,
    }
