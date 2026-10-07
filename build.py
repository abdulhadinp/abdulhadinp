#!/usr/bin/env python3
import os, math, random

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
<filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="4" result="blur"/><feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<pattern id="hud_grid" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="translate(0 0)">
  <path d="M40 0H0V40" stroke="{CYAN}" stroke-opacity="0.14" stroke-width="1"/>
  <circle cx="0" cy="0" r="1.5" fill="{CYAN}" fill-opacity="0.3"/>
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
    return f'''<g opacity="0.15">
<circle cx="160" cy="110" r="130" fill="{MAGENTA}"><animate attributeName="cx" values="160;360;160" dur="10s" repeatCount="indefinite"/><animate attributeName="cy" values="110;240;110" dur="12s" repeatCount="indefinite"/></circle>
<circle cx="{W-160}" cy="{H-100}" r="150" fill="{ROSE}"><animate attributeName="cx" values="{W-160};{W-340};{W-160}" dur="14s" repeatCount="indefinite"/><animate attributeName="cy" values="{H-100};{H-220};{H-100}" dur="9s" repeatCount="indefinite"/></circle>
</g>'''

def chip(x, y, text, color=CYAN, size=11, h=26):
    w = len(text) * size * 0.65 + 24
    return (
        f'<g transform="translate({x:.1f} {y:.1f})">'
        f'<rect width="{w:.1f}" height="{h}" rx="6" fill="{color}" fill-opacity=".12" stroke="{color}" stroke-opacity=".7" stroke-width="1.2"/>'
        f'<circle cx="10" cy="{h/2}" r="3" fill="{color}"/>'
        f'<text x="{18 + (w-18)/2}" y="{h/2+size*0.35}" text-anchor="middle" font-family="{MONO}" font-size="{size}" font-weight="700" fill="{TXT}">{esc(text)}</text>'
        f'</g>'
    ), w

# --------------------------------------------------------------------------- ADVANCED ID CARD (SAFE HUD)
def idcard():
    W, H = 1000, 540
    b = [blobs(W, H), particles(W, H, 22, 77)]

    # Safe Reticle HUD (No complex clip paths)
    reticle = f'''
    <g transform="translate(260 250)">
      <circle r="70" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="6 8" fill="none"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="14s" repeatCount="indefinite"/></circle>
      <circle r="55" stroke="{ROSE}" stroke-width="1.2" stroke-dasharray="20 40" fill="none"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="9s" repeatCount="indefinite"/></circle>
      <circle r="40" fill="{PANEL2}" stroke="{CYAN}" stroke-width="2"/>
      <text y="14" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="38" fill="{CYAN}">AH</text>
      <line x1="-85" y1="0" x2="-50" y2="0" stroke="{CYAN}" stroke-width="2"/>
      <line x1="50" y1="0" x2="85" y2="0" stroke="{CYAN}" stroke-width="2"/>
      <line x1="0" y1="-85" x2="0" y2="-50" stroke="{CYAN}" stroke-width="2"/>
      <line x1="0" y1="50" x2="0" y2="85" stroke="{CYAN}" stroke-width="2"/>
    </g>
    '''

    card = f'''<g>
    <animateTransform attributeName="transform" type="rotate" values="-1.5 260 0;1.5 260 0;-1.5 260 0" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="6s" repeatCount="indefinite"/>
    <!-- Lanyard -->
    <rect x="244" y="-20" width="32" height="110" fill="url(#gb)"/>
    <text transform="translate(264 4) rotate(90)" font-family="{MONO}" font-size="10" font-weight="700" fill="#FFFFFF" letter-spacing="3">BUILDER // 2026</text>
    <rect x="250" y="85" width="20" height="20" rx="4" fill="#030712" stroke="{CYAN}" stroke-width="2"/>
    
    <!-- Hologram Badge Base -->
    <rect x="100" y="95" width="320" height="420" rx="20" fill="{PANEL}" stroke="{CYAN}" stroke-width="2.5"/>
    <rect x="100" y="95" width="320" height="8" rx="4" fill="url(#gneon)"/>
    
    <!-- Badge Top Info -->
    <text x="122" y="124" font-family="{MONO}" font-size="12" font-weight="700" fill="{TXT}" letter-spacing="2">AH // ARCHITECT PASS</text>
    <text x="398" y="124" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}">ZYV-001</text>
    
    <!-- Vector Avatar Layer -->
    <rect x="120" y="130" width="280" height="240" rx="14" fill="{PANEL2}" stroke="{CYAN}" stroke-width="1.5" stroke-dasharray="10 10"/>
    <line x1="120" y1="130" x2="400" y2="130" stroke="url(#laser)" stroke-width="3">
      <animate attributeName="y1" values="130;370;130" dur="3.2s" repeatCount="indefinite"/>
      <animate attributeName="y2" values="130;370;130" dur="3.2s" repeatCount="indefinite"/>
    </line>
    {reticle}
    
    <!-- Corner Brackets -->
    <path d="M 124 150 V 134 H 144 M 376 134 H 396 V 150 M 124 350 V 366 H 144 M 376 366 H 396 V 350" stroke="{CYAN}" stroke-width="2" fill="none"/>
    
    <!-- Identity Fields -->
    <text x="122" y="405" font-family="{TITLE}" font-weight="900" font-size="28" fill="#FFFFFF">ABDUL HADI</text>
    <text x="122" y="428" font-family="{MONO}" font-size="12" font-weight="700" fill="{ROSE}" letter-spacing="1">FOUNDER &amp; AI BUILDER</text>
    <text x="122" y="448" font-family="{MONO}" font-size="11" fill="{MUT}">KATHMANDU NODE // NEPAL</text>
    
    <!-- Barcode + Chip -->
    <rect x="340" y="390" width="56" height="38" rx="6" fill="{GOLD}"/>
    <path d="M340 402H396M340 414H396M358 390V428M378 390V428" stroke="#78350F" stroke-width="1.5"/>
    
    <!-- Safe Scanning Sheen Line -->
    <rect x="100" y="95" width="320" height="420" rx="20" fill="none" stroke="url(#laser)" stroke-width="2">
        <animate attributeName="stroke-dasharray" values="0 2000;2000 0" dur="4s" repeatCount="indefinite"/>
    </rect>
    </g>'''

    b.append(card)

    # Right side: Live System HUD Telemetry
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
          <rect x="0" y="{yy+18}" width="{pct*4.5:.0f}" height="6" rx="3" fill="{col}"/>
        ''')
    b.append('</g>')

    b.append(f'''<g transform="translate(490 500)">
      <circle cx="6" cy="6" r="4" fill="{GREEN}"><animate attributeName="opacity" values="1;0.2;1" dur="1.5s" repeatCount="indefinite"/></circle>
      <text x="18" y="10" font-family="{MONO}" font-size="12" font-weight="700" fill="{TXT}">NOW DEPLOYING: </text>
      <text x="145" y="10" font-family="{MONO}" font-size="12" font-weight="700" fill="{CYAN}">Next-gen SaaS &amp; Agentic AI Solutions</text>
    </g>''')

    return wrap(W, H, "".join(b))

if __name__ == "__main__":
    print("--> Generating ultra-safe vector ID card...")
    save("idcard.svg", idcard())
    print("--> Complete.")