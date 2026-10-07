#!/usr/bin/env python3
"""
Next-Gen Cybernetic HUD SVG Portfolio Engine for GitHub
Generates ultra-advanced animated SVGs into ./assets
Run: python3 build.py
"""
import os, math, random, base64

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

# Cybernetic Dark Palette
BG, PANEL, PANEL2 = "#030712", "#0A0F24", "#0F1738"
CYAN, BLUE, MAGENTA, ROSE = "#00F0FF", "#38BDF8", "#BD00FF", "#FF0055"
GREEN, TXT, MUT, GOLD = "#00FF66", "#F1F5F9", "#64748B", "#FACC15"
TITLE = "'Arial Black','Impact','Helvetica Neue',Arial,sans-serif"
MONO = "'SFMono-Regular','JetBrains Mono','Consolas','Menlo','Courier New',monospace"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def wrap(w, h, body, defs="", grid=True, r=20):
    g = f'<rect width="{w}" height="{h}" fill="url(#hud_grid)" opacity="0.45"/>' if grid else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>
<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="gr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ROSE}"/><stop offset="1" stop-color="#FF5500"/></linearGradient>
<linearGradient id="gneon" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="0.5" stop-color="{MAGENTA}" stop-opacity=".7"/><stop offset="1" stop-color="{ROSE}"/></linearGradient>
<linearGradient id="gbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#02040A"/><stop offset="0.5" stop-color="#070D1F"/><stop offset="1" stop-color="#14061A"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}" stop-opacity=".22"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>
<linearGradient id="laser" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="0.5" stop-color="{CYAN}" stop-opacity="1"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></linearGradient>

<filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
  <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur"/>
  <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="heavyglow" x="-80%" y="-80%" width="260%" height="260%">
  <feGaussianBlur in="SourceGraphic" stdDeviation="12" result="blur2"/>
  <feMerge><feMergeNode in="blur2"/><feMergeNode in="SourceGraphic"/></feMerge>
</filter>
<filter id="blur50" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="55"/></filter>

<pattern id="hud_grid" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="translate(0 0)">
  <path d="M40 0H0V40" stroke="{CYAN}" stroke-opacity="0.14" stroke-width="1"/>
  <circle cx="0" cy="0" r="1.5" fill="{CYAN}" fill-opacity="0.3"/>
  <animateTransform attributeName="patternTransform" type="translate" from="0 0" to="40 40" dur="8s" repeatCount="indefinite"/>
</pattern>
<clipPath id="frame"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
{defs}
</defs>
<g clip-path="url(#frame)">
<rect width="{w}" height="{h}" fill="url(#gbg)"/>
{g}
{body}
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r-1}" stroke="url(#gneon)" stroke-width="1.8" fill="none" opacity="0.85"/>
<!-- Outer HUD Tech Brackets -->
<path d="M 2 24 V 2 H 24 M {w-24} 2 H {w-2} V 24 M 2 {h-24} V {h-2} H 24 M {w-24} {h-2} H {w-2} V {h-24}" stroke="{CYAN}" stroke-width="3" fill="none" filter="url(#glow)"/>
</svg>'''


def particles(W, H, n, seed):
    rnd = random.Random(seed)
    s = []
    for _ in range(n):
        x, y = rnd.randint(30, W - 30), rnd.randint(60, H - 30)
        r = rnd.choice([1.2, 1.8, 2.4])
        d, b = rnd.uniform(4, 9), rnd.uniform(0, 5)
        c = rnd.choice([CYAN, BLUE, ROSE, MAGENTA, "#FFFFFF"])
        s.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}">'
            f'<animate attributeName="cy" values="{y};{y-70};{y}" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.1;0.95;0.1" dur="{d/2:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(s)


def blobs(W, H):
    return f'''<g filter="url(#blur50)" opacity="0.6">
<circle cx="160" cy="110" r="130" fill="{MAGENTA}"><animate attributeName="cx" values="160;360;160" dur="10s" repeatCount="indefinite"/><animate attributeName="cy" values="110;240;110" dur="12s" repeatCount="indefinite"/></circle>
<circle cx="{W-160}" cy="{H-100}" r="150" fill="{ROSE}" opacity=".7"><animate attributeName="cx" values="{W-160};{W-340};{W-160}" dur="14s" repeatCount="indefinite"/><animate attributeName="cy" values="{H-100};{H-220};{H-100}" dur="9s" repeatCount="indefinite"/></circle>
<circle cx="{W//2}" cy="{H//2}" r="110" fill="{CYAN}" opacity=".35"><animate attributeName="r" values="90;150;90" dur="11s" repeatCount="indefinite"/></circle>
</g>'''


def scanline(W, H):
    return f'<rect x="0" y="-120" width="{W}" height="120" fill="url(#scan)"><animate attributeName="y" from="-120" to="{H+60}" dur="5s" repeatCount="indefinite"/></rect>'


def chip(x, y, text, color=CYAN, size=11, h=26, font=None):
    font = font or MONO
    w = len(text) * size * 0.65 + 24
    return (
        f'<g transform="translate({x:.1f} {y:.1f})">'
        f'<rect width="{w:.1f}" height="{h}" rx="6" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".7" stroke-width="1.2"/>'
        f'<circle cx="10" cy="{h/2}" r="3" fill="{color}"/>'
        f'<text x="{18 + (w-18)/2}" y="{h/2+size*0.35}" text-anchor="middle" font-family="{font}" font-size="{size}" font-weight="700" fill="{TXT}">{esc(text)}</text>'
        f'</g>'
    ), w


# --------------------------------------------------------------------------- HERO HUD
def hero():
    W, H = 1000, 480
    b = [blobs(W, H), particles(W, H, 32, 101), scanline(W, H)]
    
    # Telemetry header bar
    b.append(f'''<g transform="translate(48 38)">
      <circle cx="6" cy="6" r="5" fill="{GREEN}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.3;1" dur="1.8s" repeatCount="indefinite"/></circle>
      <text x="22" y="10" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}" letter-spacing="3">STATUS: LIVE // SYS_CORE: OPTIMAL // KATHMANDU NODE [27.7172° N, 85.3240° E]</text>
    </g>''')

    # Cyberpunk Glitch ABDUL HADI
    for col, dx, opa in ((ROSE, "-6 2", 0.85), (CYAN, "6 -2", 0.85)):
        b.append(
            f'<g opacity="0" font-family="{TITLE}" font-weight="900" font-size="118" letter-spacing="-3" fill="{col}">'
            f'<animate attributeName="opacity" values="0;0;{opa};{opa};0;0" keyTimes="0;0.88;0.90;0.94;0.96;1" dur="4.5s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{dx};0 0" keyTimes="0;0.88;0.90;0.94;1" dur="4.5s" repeatCount="indefinite"/>'
            f'<text x="48" y="175">ABDUL</text><text x="48" y="285">HADI</text></g>'
        )
    b.append(f'<text x="48" y="175" font-family="{TITLE}" font-weight="900" font-size="118" letter-spacing="-3" fill="#FFFFFF">ABDUL</text>')
    b.append(f'<text x="48" y="285" font-family="{TITLE}" font-weight="900" font-size="118" letter-spacing="-3" fill="url(#gb)">HADI</text>')

    # Tagline badge
    b.append(f'''<g transform="translate(435 210)">
      <rect width="180" height="74" rx="8" fill="{PANEL}" stroke="{ROSE}" stroke-width="1.8" filter="url(#glow)"/>
      <path d="M 0 10 L 10 0 M 180 64 L 170 74" stroke="{ROSE}" stroke-width="2"/>
      <text x="18" y="32" font-family="{TITLE}" font-weight="900" font-size="22" fill="#FFFFFF" letter-spacing="2">BUILD.</text>
      <text x="18" y="58" font-family="{TITLE}" font-weight="900" font-size="22" fill="{ROSE}" letter-spacing="2">BEYOND.</text>
    </g>''')

    # Cycling Roles
    roles = [
        "AI Architect & Systems Engineer",
        "Founder & Lead Builder @ Zyvora Technologies",
        "Co-Founder & CTO @ Nexus Global Travels",
        "AI Researcher @ Vectrah (Edge Models)",
        "Creator @ HadiTechNepal & abduljourneyofficial"
    ]
    n = len(roles)
    for i, r in enumerate(roles):
        s, e = i / n, (i + 1) / n
        a = min(s + 0.025, e)
        c = max(e - 0.025, a)
        b.append(
            f'<text x="48" y="340" font-family="{MONO}" font-size="21" font-weight="700" fill="{TXT}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{s:.4f};{a:.4f};{c:.4f};{e:.4f};1" dur="16s" repeatCount="indefinite"/>'
            f'<tspan fill="{ROSE}">&gt; </tspan>{esc(r)}<tspan fill="{CYAN}">_</tspan></text>'
        )

    # Dynamic Audio Waveform Visualizer
    b.append(f'<g transform="translate(48 375)">')
    for k in range(32):
        bx = k * 14
        h0 = random.randint(6, 16)
        h1 = random.randint(22, 38)
        dur = random.uniform(0.7, 1.6)
        b.append(f'<rect x="{bx}" y="20" width="8" height="{h0}" rx="4" fill="url(#gneon)">'
                 f'<animate attributeName="height" values="{h0};{h1};{h0}" dur="{dur:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="20;{20-(h1-h0)/2};20" dur="{dur:.2f}s" repeatCount="indefinite"/>'
                 f'</rect>')
    b.append('</g>')

    # Badges
    x = 48
    for t, col in [("KATHMANDU, NP", CYAN), ("BSc (HONS) IT", BLUE), ("ZYVORA TECH", ROSE), ("VECTRAH AI", MAGENTA)]:
        c, w = chip(x, 428, t, col)
        b.append(c)
        x += w + 14

    # Cyber Kinetic Monogram (Right side)
    cx, cy = 810, 240
    hexpts = " ".join(f"{74*math.cos(math.radians(60*k-30)):.1f},{74*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))
    b.append(f'''<g transform="translate({cx} {cy})">
      <circle r="160" stroke="{CYAN}" stroke-opacity=".25" stroke-width="1.5" stroke-dasharray="4 16"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="45s" repeatCount="indefinite"/></circle>
      <circle r="130" stroke="{ROSE}" stroke-width="2.5" stroke-dasharray="90 50" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="18s" repeatCount="indefinite"/></circle>
      <circle r="96" stroke="{CYAN}" stroke-width="2" stroke-dasharray="4 8" opacity=".7"/>
      <g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="8s" repeatCount="indefinite"/><circle cx="160" cy="0" r="7" fill="{CYAN}" filter="url(#glow)"/></g>
      <g><animateTransform attributeName="transform" type="rotate" from="180" to="540" dur="12s" repeatCount="indefinite"/><circle cx="130" cy="0" r="6" fill="{ROSE}" filter="url(#glow)"/></g>
      <polygon points="{hexpts}" fill="{PANEL}" stroke="url(#gneon)" stroke-width="3" filter="url(#glow)"><animate attributeName="stroke-width" values="2;4;2" dur="2.5s" repeatCount="indefinite"/></polygon>
      <text y="18" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="52" fill="#FFFFFF">AH</text>
    </g>''')

    return wrap(W, H, "".join(b))


# --------------------------------------------------------------------------- ADVANCED ID CARD (HOLO HUD)
def idcard():
    W, H = 1000, 540
    photo = None

    candidates = [
        os.path.join(HERE, "photo.png"), os.path.join(HERE, "photo.PNG"),
        os.path.join(HERE, "photo.jpg"), os.path.join(HERE, "photo.jpeg"),
        os.path.join(OUT, "photo.png"), os.path.join(OUT, "photo.jpg")
    ]
    found_path = next((p for p in candidates if os.path.exists(p)), None)

    if found_path:
        try:
            # Check file size
            raw_bytes = open(found_path, "rb").read()
            # If larger than 800KB, attempt PIL resize if available
            if len(raw_bytes) > 800 * 1024:
                try:
                    from PIL import Image
                    import io
                    im = Image.open(io.BytesIO(raw_bytes))
                    im.thumbnail((500, 500), Image.Resampling.LANCZOS)
                    buf = io.BytesIO()
                    im.save(buf, format="PNG", optimize=True)
                    raw_bytes = buf.getvalue()
                    print(f"--> [OPTIMIZED] Resized photo to {len(raw_bytes)//1024} KB for GitHub Camo limits.")
                except ImportError:
                    print("--> [NOTE] Install Pillow ('pip install pillow') if image file is too large.")
            
            ext = os.path.splitext(found_path)[1].lower()
            mime = "image/png" if "png" in ext else "image/jpeg"
            b64_data = base64.b64encode(raw_bytes).decode("utf-8")
            photo = f"data:{mime};base64,{b64_data}"
            print(f"--> [SUCCESS] Embedded photo from: {found_path} ({len(raw_bytes)//1024} KB)")
        except Exception as e:
            print(f"--> [ERROR reading photo]: {e}")
    else:
        print("--> [WARNING] No photo file found! Falling back to 'AH' monogram.")

    if photo:
        pic = f'<image href="{photo}" x="120" y="130" width="280" height="240" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo_clip)"/>'
    else:
        pic = (f'<rect x="120" y="130" width="280" height="240" rx="14" fill="{PANEL2}"/>'
               f'<circle cx="260" cy="230" r="50" fill="{PANEL}" stroke="{CYAN}" stroke-width="2"/>'
               f'<text x="260" y="248" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="44" fill="{CYAN}">AH</text>')

    # Reticle HUD
    reticle = f'''
    <g transform="translate(260 250)">
      <circle r="60" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="6 8" opacity="0.6"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></circle>
      <circle r="40" stroke="{ROSE}" stroke-width="1.2" stroke-dasharray="20 40" opacity="0.8"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="9s" repeatCount="indefinite"/></circle>
      <line x1="-75" y1="0" x2="-45" y2="0" stroke="{CYAN}" stroke-width="2"/>
      <line x1="45" y1="0" x2="75" y2="0" stroke="{CYAN}" stroke-width="2"/>
      <line x1="0" y1="-75" x2="0" y2="-45" stroke="{CYAN}" stroke-width="2"/>
      <line x1="0" y1="45" x2="0" y2="75" stroke="{CYAN}" stroke-width="2"/>
    </g>
    <line x1="120" y1="130" x2="400" y2="130" stroke="url(#laser)" stroke-width="3" filter="url(#glow)">
      <animate attributeName="y1" values="130;370;130" dur="3.2s" repeatCount="indefinite"/>
      <animate attributeName="y2" values="130;370;130" dur="3.2s" repeatCount="indefinite"/>
    </line>
    '''

    card = f'''<g>
    <animateTransform attributeName="transform" type="rotate" values="-2 260 0;2 260 0;-2 260 0" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="7s" repeatCount="indefinite"/>
    <rect x="244" y="-20" width="32" height="110" fill="url(#gb)"/>
    <text transform="translate(264 4) rotate(90)" font-family="{MONO}" font-size="10" font-weight="700" fill="#FFFFFF" letter-spacing="3">BUILDER // 2026</text>
    <rect x="250" y="85" width="20" height="20" rx="4" fill="#030712" stroke="{CYAN}" stroke-width="2"/>
    
    <rect x="100" y="95" width="320" height="420" rx="20" fill="{PANEL}" stroke="{CYAN}" stroke-width="2.5" filter="url(#glow)"/>
    <rect x="100" y="95" width="320" height="8" rx="4" fill="url(#gneon)"/>
    
    <text x="122" y="124" font-family="{MONO}" font-size="12" font-weight="700" fill="{TXT}" letter-spacing="2">AH // ARCHITECT PASS</text>
    <text x="398" y="124" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}">ZYV-001</text>
    
    {pic}
    {reticle}
    
    <path d="M 124 150 V 134 H 144 M 376 134 H 396 V 150 M 124 350 V 366 H 144 M 376 366 H 396 V 350" stroke="{CYAN}" stroke-width="2" fill="none"/>
    
    <text x="122" y="405" font-family="{TITLE}" font-weight="900" font-size="28" fill="#FFFFFF">ABDUL HADI</text>
    <text x="122" y="428" font-family="{MONO}" font-size="12" font-weight="700" fill="{ROSE}" letter-spacing="1">FOUNDER &amp; AI BUILDER</text>
    <text x="122" y="448" font-family="{MONO}" font-size="11" fill="{MUT}">KATHMANDU NODE // NEPAL</text>
    
    <rect x="340" y="390" width="56" height="38" rx="6" fill="{GOLD}"/>
    <path d="M340 402H396M340 414H396M358 390V428M378 390V428" stroke="#78350F" stroke-width="1.5"/>
    
    <g clip-path="url(#badge_clip)">
      <rect x="-260" y="90" width="110" height="430" fill="url(#holo_sheen)" transform="skewX(-20)">
        <animate attributeName="x" values="-260;540;540" keyTimes="0;0.5;1" dur="4.5s" repeatCount="indefinite"/>
      </rect>
    </g>
    </g>'''

    defs = f'''
    <clipPath id="badge_clip"><rect x="100" y="95" width="320" height="420" rx="20"/></clipPath>
    <clipPath id="photo_clip"><rect x="120" y="130" width="280" height="240" rx="14"/></clipPath>
    <linearGradient id="holo_sheen" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{CYAN}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{CYAN}" stop-opacity=".35"/>
      <stop offset="1" stop-color="{CYAN}" stop-opacity="0"/>
    </linearGradient>
    '''

    b = [blobs(W, H), particles(W, H, 22, 77), card]

    b.append(f'''<g transform="translate(490 85)">
      <text x="0" y="24" font-family="{MONO}" font-size="13" font-weight="700" fill="{ROSE}" letter-spacing="3">// SYSTEM PROFILE &amp; STATS</text>
      <text x="0" y="70" font-family="{TITLE}" font-weight="900" font-size="44" fill="#FFFFFF">ENGINEERED FOR</text>
      <text x="0" y="116" font-family="{TITLE}" font-weight="900" font-size="44" fill="url(#gb)">HIGH IMPACT.</text>
    </g>''')

    metrics = [("04", "ROLES ACTIVE"), ("08+", "SHIPPED APPS"), ("100%", "OWNERSHIP")]
    for i, (val, lbl) in enumerate(metrics):
        tx = 490 + i * 158
        b.append(f'''<g transform="translate({tx} 230)">
          <rect width="144" height="96" rx="12" fill="{PANEL}" stroke="{CYAN}" stroke-opacity="0.4" stroke-width="1.5"/>
          <rect width="144" height="4" rx="2" fill="url(#gr)"/>
          <text x="18" y="52" font-family="{TITLE}" font-weight="900" font-size="40" fill="url(#gb)">{val}</text>
          <text x="18" y="78" font-family="{MONO}" font-size="11" font-weight="700" fill="{TXT}" letter-spacing="1">{lbl}</text>
        </g>''')

    bars = [
        ("AI AGENTS & LOCAL LLMS", 92, CYAN),
        ("FULL STACK ARCHITECTURE", 95, BLUE),
        ("DISTRIBUTED CLOUD SYSTEMS", 88, MAGENTA),
        ("CYBERSECURITY & NETWORKING", 84, ROSE)
    ]
    b.append(f'<g transform="translate(490 365)">')
    for i, (skill, pct, col) in enumerate(bars):
        yy = i * 32
        b.append(f'''
          <text x="0" y="{yy+12}" font-family="{MONO}" font-size="12" font-weight="700" fill="{TXT}">{skill}</text>
          <text x="450" y="{yy+12}" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="700" fill="{col}">{pct}%</text>
          <rect x="0" y="{yy+18}" width="450" height="6" rx="3" fill="{PANEL2}"/>
          <rect x="0" y="{yy+18}" width="{pct*4.5:.0f}" height="6" rx="3" fill="{col}" filter="url(#glow)"/>
        ''')
    b.append('</g>')

    b.append(f'''<g transform="translate(490 500)">
      <circle cx="6" cy="6" r="4" fill="{GREEN}" filter="url(#glow)"><animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/></circle>
      <text x="18" y="10" font-family="{MONO}" font-size="12" font-weight="700" fill="{TXT}">NOW DEPLOYING: </text>
      <text x="145" y="10" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}">Next-gen SaaS &amp; Agentic AI Solutions</text>
    </g>''')

    return wrap(W, H, "".join(b), defs)


# --------------------------------------------------------------------------- REVOLUTIONARY ORBIT MATRIX
def orbit():
    W, H = 1000, 520
    cx, cy = 260, 260
    b = [particles(W, H, 20, 42), blobs(W, H)]
    
    rings = [
        (85, 20, 1, CYAN, ["TS", "Python", "JS", "C++"]),
        (150, 32, -1, ROSE, ["React", "Next.js", "Node", "FastAPI", "Tailwind"]),
        (215, 48, 1, BLUE, ["PostgreSQL", "Supabase", "Docker", "Vercel", "Linux", "Git"]),
    ]
    
    g = [f'<g transform="translate({cx} {cy})">']
    for r, dur, d, col, nodes in rings:
        g.append(f'<circle r="{r}" stroke="{col}" stroke-opacity=".25" stroke-width="1.8" stroke-dasharray="4 8"/>')
        a0, a1 = (0, 360) if d == 1 else (360, 0)
        c0, c1 = (360, 0) if d == 1 else (0, 360)
        g.append(f'<g><animateTransform attributeName="transform" type="rotate" from="{a0}" to="{a1}" dur="{dur}s" repeatCount="indefinite"/>')
        n = len(nodes)
        for k, lab in enumerate(nodes):
            ang = 2 * math.pi * k / n
            x, y = r * math.cos(ang), r * math.sin(ang)
            g.append(
                f'<g transform="translate({x:.1f} {y:.1f})"><g><animateTransform attributeName="transform" type="rotate" from="{c0}" to="{c1}" dur="{dur}s" repeatCount="indefinite"/>'
                f'<circle r="25" fill="{PANEL}" stroke="{col}" stroke-width="2" filter="url(#glow)"/>'
                f'<text y="4" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#FFFFFF">{lab}</text></g></g>'
            )
        g.append("</g>")

    hexpts = " ".join(f"{46*math.cos(math.radians(60*k-30)):.1f},{46*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))
    g.append(f'<polygon points="{hexpts}" fill="{PANEL}" stroke="{CYAN}" stroke-width="2.5" filter="url(#glow)"><animate attributeName="stroke-opacity" values=".4;1;.4" dur="2.5s" repeatCount="indefinite"/></polygon>')
    g.append(f'<text y="9" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="28" fill="#FFFFFF">AH</text></g>')
    b.append("".join(g))

    # Divider line
    b.append(f'<line x1="530" y1="40" x2="530" y2="480" stroke="{CYAN}" stroke-opacity=".2" stroke-width="1.5" stroke-dasharray="6 6"/>')

    # Categorized skill badges
    cats = [
        ("01 / CORE LANGUAGES", ["TypeScript", "JavaScript", "Python", "C", "C++", "C#", "SQL"], CYAN),
        ("02 / FRONTEND & UI ARCHITECTURE", ["React", "Next.js", "Tailwind CSS", "HTML5", "CSS3"], BLUE),
        ("03 / BACKEND, DATA & CLOUD", ["Node.js", "Express", "PostgreSQL", "Supabase", "Vercel", "Docker"], MAGENTA),
        ("04 / DEV ENVIRONMENT & OPS", ["macOS (Apple Silicon)", "Linux / Kali", "Git", "VS Code"], ROSE),
    ]

    y = 54
    for lab, items, col in cats:
        b.append(f'<text x="560" y="{y}" font-family="{MONO}" font-size="12" font-weight="700" fill="{col}" letter-spacing="2">{esc(lab)}</text>')
        y += 14
        x = 560
        for it in items:
            w = len(it) * 11 * 0.65 + 24
            if x + w > 960:
                x = 560
                y += 36
            c, w = chip(x, y, it, col, size=11, h=26)
            b.append(c)
            x += w + 8
        y += 50

    b.append(f'<text x="560" y="{H-24}" font-family="{MONO}" font-size="11" font-weight="700" fill="{MUT}" letter-spacing="2">&gt; CONTINUOUS INTEGRATION. CURIOUS BY DEFAULT.</text>')
    return wrap(W, H, "".join(b))


# --------------------------------------------------------------------------- RUN ENGINE
if __name__ == "__main__":
    print("--> Synthesizing Next-Gen Cybernetic HUD assets...")
    save("hero.svg", hero())
    save("idcard.svg", idcard())
    save("orbit.svg", orbit())
    print("Done. Generated Next-Gen HUD assets in:", OUT)