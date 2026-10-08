#!/usr/bin/env python3
"""
Generates every animated SVG used by README.md into ./assets
Run:  python build.py
Optional: put your photo at assets/photo.jpg (or photo.jpg next to this file) and run again.
It gets embedded inside the Builder Pass card.
"""
import os, math, random, base64

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
os.makedirs(OUT, exist_ok=True)

BG, PANEL, PANEL2 = "#060B1F", "#0B1433", "#0F1B45"
BLUE, DEEP, RED = "#38BDF8", "#1D4ED8", "#E11D48"
TXT, MUT, GOLD = "#E2E8F0", "#7C8DB5", "#FACC15"
TITLE = "'Arial Black','Impact','Helvetica Neue',Arial,sans-serif"
MONO = "'SFMono-Regular','JetBrains Mono','Consolas','Menlo','Courier New',monospace"
SANS = "'Segoe UI','Helvetica Neue',Arial,sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;")


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


def wrap(w, h, body, defs="", grid=True, r=18):
    g = f'<rect width="{w}" height="{h}" fill="url(#grid)"/>' if grid else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" fill="none">
<defs>
<linearGradient id="gb" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{DEEP}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>
<linearGradient id="gr" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{RED}"/><stop offset="1" stop-color="#FB923C"/></linearGradient>
<linearGradient id="gline" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{DEEP}"/><stop offset="0.5" stop-color="{BLUE}" stop-opacity=".6"/><stop offset="1" stop-color="{RED}"/></linearGradient>
<linearGradient id="gbg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#050A1C"/><stop offset="0.6" stop-color="#0A1640"/><stop offset="1" stop-color="#1A0B2B"/></linearGradient>
<linearGradient id="scan" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BLUE}" stop-opacity="0"/><stop offset="0.5" stop-color="{BLUE}" stop-opacity=".14"/><stop offset="1" stop-color="{BLUE}" stop-opacity="0"/></linearGradient>
<filter id="glow" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<filter id="blur40" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="42"/></filter>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse" patternTransform="translate(0 0)">
<path d="M40 0H0V40" stroke="#1E3A8A" stroke-opacity="0.32" stroke-width="1"/>
<animateTransform attributeName="patternTransform" type="translate" from="0 0" to="40 40" dur="7s" repeatCount="indefinite"/>
</pattern>
<clipPath id="frame"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
{defs}
</defs>
<g clip-path="url(#frame)">
<rect width="{w}" height="{h}" fill="url(#gbg)"/>
{g}
{body}
</g>
<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{r-1}" stroke="url(#gline)" stroke-width="2" fill="none"/>
</svg>'''


def particles(W, H, n, seed):
    rnd = random.Random(seed)
    s = []
    for _ in range(n):
        x, y = rnd.randint(20, W - 20), rnd.randint(60, H - 20)
        r = rnd.choice([1.2, 1.6, 2.2])
        d, b = rnd.uniform(5, 11), rnd.uniform(0, 6)
        c = rnd.choice([BLUE, BLUE, RED, "#FFFFFF"])
        s.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}">'
            f'<animate attributeName="cy" values="{y};{y-60};{y}" dur="{d:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.15;0.9;0.15" dur="{d/2:.1f}s" begin="-{b:.1f}s" repeatCount="indefinite"/></circle>'
        )
    return "".join(s)


def blobs(W, H):
    return f'''<g filter="url(#blur40)" opacity="0.55">
<circle cx="170" cy="110" r="110" fill="{DEEP}"><animate attributeName="cx" values="170;330;170" dur="9s" repeatCount="indefinite"/><animate attributeName="cy" values="110;220;110" dur="11s" repeatCount="indefinite"/></circle>
<circle cx="{W-150}" cy="{H-90}" r="130" fill="{RED}" opacity=".65"><animate attributeName="cx" values="{W-150};{W-300};{W-150}" dur="12s" repeatCount="indefinite"/><animate attributeName="cy" values="{H-90};{H-190};{H-90}" dur="8s" repeatCount="indefinite"/></circle>
<circle cx="{W//2}" cy="{H//2}" r="90" fill="{BLUE}" opacity=".4"><animate attributeName="r" values="90;130;90" dur="10s" repeatCount="indefinite"/></circle>
</g>'''


def scanline(W, H):
    return f'<rect x="0" y="-90" width="{W}" height="90" fill="url(#scan)"><animate attributeName="y" from="-90" to="{H}" dur="6s" repeatCount="indefinite"/></rect>'


def slashes(x, y, color=RED, n=3, size=16, delay=0.0):
    s = []
    for i in range(n):
        px = x + i * 11
        s.append(
            f'<polygon points="{px},{y} {px+8},{y} {px+2},{y+size} {px-6},{y+size}" fill="{color}">'
            f'<animate attributeName="opacity" values="0.25;1;0.25" dur="1.8s" begin="{delay+i*0.25:.2f}s" repeatCount="indefinite"/></polygon>'
        )
    return "".join(s)


def chip(x, y, text, color=BLUE, size=12, h=28, delay=None, font=None):
    font = font or MONO
    w = len(text) * size * 0.62 + 28
    inner = (
        f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{color}" fill-opacity=".10" stroke="{color}" stroke-opacity=".65"/>'
        f'<text x="{x+w/2:.1f}" y="{y+h/2+size*0.35:.1f}" text-anchor="middle" font-family="{font}" font-size="{size}" font-weight="700" fill="{TXT}">{esc(text)}</text>'
    )
    if delay is not None:
        inner = f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.6s" fill="freeze"/>{inner}</g>'
    return inner, w


def appear(t0, total, hold=0.96):
    e = min(t0 + 0.006, hold)
    return (f'<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{t0:.4f};{e:.4f};{hold};1" '
            f'dur="{total}s" repeatCount="indefinite"/>')


# --------------------------------------------------------------------------- HERO
def hero():
    W, H = 1000, 470
    b = [blobs(W, H), particles(W, H, 26, 7), scanline(W, H)]
    b.append(f'<text x="50" y="52" font-family="{MONO}" font-size="14" font-weight="700" fill="{RED}" letter-spacing="3">'
             f'/// ABDUL HADI &#160;/&#160; BUILDER PORTFOLIO &#160;/&#160; 2026</text>')
    # glitch copies
    for col, dx, opa in ((RED, "-7 2", 0.9), ("#22D3EE", "7 -2", 0.9)):
        b.append(
            f'<g opacity="0" font-family="{TITLE}" font-weight="900" font-size="128" letter-spacing="-3" fill="{col}">'
            f'<animate attributeName="opacity" values="0;0;{opa};{opa};0;0" keyTimes="0;0.86;0.88;0.93;0.95;1" dur="5s" repeatCount="indefinite"/>'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 0;{dx};{dx.split()[0].replace("-","") if False else dx};0 0;0 0" keyTimes="0;0.86;0.88;0.93;0.95;1" dur="5s" repeatCount="indefinite"/>'
            f'<text x="50" y="190">ABDUL</text><text x="50" y="308">HADI</text></g>'
        )
    b.append(f'<text x="50" y="190" font-family="{TITLE}" font-weight="900" font-size="128" letter-spacing="-3" fill="#FFFFFF">ABDUL</text>')
    b.append(f'<text x="50" y="308" font-family="{TITLE}" font-weight="900" font-size="128" letter-spacing="-3" fill="url(#gb)">HADI</text>')
    # BUILD. BEYOND.
    b.append(slashes(452, 232, RED, 3, 30))
    b.append(f'<text x="496" y="262" font-family="{TITLE}" font-weight="900" font-size="30" fill="#FFFFFF" letter-spacing="1">BUILD.</text>')
    b.append(f'<text x="496" y="298" font-family="{TITLE}" font-weight="900" font-size="30" fill="#FFFFFF" letter-spacing="1">BEYOND.</text>')
    # rotating roles
    roles = ["AI & Software Builder", "Founder of Zyvora Technologies", "Co-Founder & CTO, Nexus Global Travels",
             "AI Researcher at Vectrah", "Tech Educator, abduljourneyofficial"]
    n = len(roles)
    for i, r in enumerate(roles):
        s, e = i / n, (i + 1) / n
        a = min(s + 0.03, e)
        c = max(e - 0.03, a)
        b.append(
            f'<text x="50" y="352" font-family="{MONO}" font-size="23" font-weight="700" fill="{TXT}" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{s:.4f};{a:.4f};{c:.4f};{e:.4f};1" dur="15s" repeatCount="indefinite"/>'
            f'<tspan fill="{RED}">&gt; </tspan>{esc(r)}<tspan fill="{BLUE}">_</tspan></text>'
        )
    # chips
    x = 50
    for i, t in enumerate(["KATHMANDU, NEPAL", "FINAL YEAR BSc IT", "ZYVORA TECHNOLOGIES", "VECTRAH AI"]):
        g, w = chip(x, 396, t, BLUE if i % 2 == 0 else RED, size=12, h=32, delay=0.4 + i * 0.25)
        b.append(g)
        x += w + 12
    # monogram
    cx, cy = 810, 215
    hexpts = " ".join(f"{62*math.cos(math.radians(60*k-30)):.1f},{62*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))
    b.append(f'''<g transform="translate({cx} {cy})">
<circle r="150" stroke="{BLUE}" stroke-opacity=".45" stroke-width="2" stroke-dasharray="3 13"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="40s" repeatCount="indefinite"/></circle>
<circle r="118" stroke="{RED}" stroke-width="3" stroke-dasharray="70 44" stroke-linecap="round"><animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="16s" repeatCount="indefinite"/></circle>
<circle r="86" stroke="{BLUE}" stroke-width="1.5" stroke-opacity=".8"/>
<g><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="9s" repeatCount="indefinite"/><circle cx="150" cy="0" r="6" fill="{RED}" filter="url(#glow)"/></g>
<g><animateTransform attributeName="transform" type="rotate" from="180" to="540" dur="14s" repeatCount="indefinite"/><circle cx="118" cy="0" r="5" fill="{BLUE}" filter="url(#glow)"/></g>
<polygon points="{hexpts}" fill="url(#gb)" fill-opacity=".28" stroke="{BLUE}" stroke-width="2" filter="url(#glow)"><animate attributeName="stroke-opacity" values="1;.4;1" dur="3s" repeatCount="indefinite"/></polygon>
<text y="16" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="46" fill="#FFFFFF">AH</text>
</g>''')
    return wrap(W, H, "".join(b))


# --------------------------------------------------------------------------- SECTION HEADERS
def section(name, num, kicker, title):
    W, H = 1000, 128
    size = min(54, 880 / (len(title) * 0.74))
    tw = len(title) * size * 0.74
    b = [particles(W, H, 8, hash(name) % 1000)]
    b.append(slashes(50, 24, RED, 3, 16))
    b.append(f'<text x="98" y="38" font-family="{MONO}" font-size="14" font-weight="700" fill="{BLUE}" letter-spacing="3">{esc(num)} / {esc(kicker)}</text>')
    b.append(f'<text x="50" y="98" font-family="{TITLE}" font-weight="900" font-size="{size:.1f}" fill="#FFFFFF" opacity="0">'
             f'<animate attributeName="opacity" from="0" to="1" dur="0.8s" fill="freeze"/>'
             f'<animateTransform attributeName="transform" type="translate" from="-24 0" to="0 0" dur="0.8s" fill="freeze"/>{esc(title)}</text>')
    b.append(f'<rect x="50" y="108" height="4" rx="2" fill="url(#gr)" width="0"><animate attributeName="width" values="0;{tw:.0f};{tw:.0f};0" keyTimes="0;0.35;0.85;1" dur="7s" repeatCount="indefinite"/></rect>')
    b.append(f'<rect x="{W-110}" y="30" width="60" height="60" rx="14" fill="{BLUE}" fill-opacity=".08" stroke="{BLUE}" stroke-opacity=".5"/>'
             f'<text x="{W-80}" y="70" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="28" fill="{BLUE}">{esc(num)}</text>')
    save(name, wrap(W, H, "".join(b)))


# --------------------------------------------------------------------------- TERMINAL
def terminal():
    W, H, T = 1000, 470, 18
    b = []
    b.append(f'<rect x="0" y="0" width="{W}" height="46" fill="#0A1230"/>')
    for i, c in enumerate(("#EF4444", "#FACC15", "#22C55E")):
        b.append(f'<circle cx="{30+i*24}" cy="23" r="7" fill="{c}"/>')
    b.append(f'<text x="{W/2}" y="28" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUT}">abdul@kathmandu: ~/zyvora</text>')
    b.append(blobs(W, H).replace('opacity="0.55"', 'opacity="0.28"'))
    b.append(scanline(W, H))

    def typed(idx, x, y, spans, t0, t1, size=16):
        n = sum(len(t) for t, _ in spans)
        wpx = n * size * 0.6 + 14
        cid = f"tc{idx}"
        clip = (f'<clipPath id="{cid}"><rect x="{x-2}" y="{y-size-3}" height="{size+12}" width="0">'
                f'<animate attributeName="width" values="0;0;{wpx:.0f};{wpx:.0f};0" keyTimes="0;{t0:.4f};{t1:.4f};0.96;1" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
        ts = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in spans)
        return clip + f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="600" xml:space="preserve" clip-path="url(#{cid})">{ts}</text>'

    def out(x, y, spans, t0, size=16):
        ts = "".join(f'<tspan fill="{c}">{esc(t)}</tspan>' for t, c in spans)
        return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" font-weight="600" xml:space="preserve" opacity="0">'
                f'{appear(t0, T)}{ts}</text>')

    P = [("$ ", RED)]
    y, lh, x0 = 94, 26, 36
    b.append(typed(1, x0, y, P + [("whoami", TXT)], 0.03, 0.09))
    y += lh
    b.append(out(x0, y, [("abdul_hadi: founder, builder, educator", BLUE)], 0.11))
    y += lh * 1.5
    b.append(typed(2, x0, y, P + [("cat status.json", TXT)], 0.16, 0.25))
    json_lines = [
        [("{", MUT)],
        [("    \"studying\": ", "#93C5FD"), ("\"BSc IT, final year\"", "#FDE68A"), (",", MUT)],
        [("    \"researching\": ", "#93C5FD"), ("\"AI at Vectrah\"", "#FDE68A"), (",", MUT)],
        [("    \"building\": ", "#93C5FD"), ("\"Zyvora Technologies\"", "#FDE68A"), (",", MUT)],
        [("    \"teaching\": ", "#93C5FD"), ("\"abduljourneyofficial\"", "#FDE68A")],
        [("}", MUT)],
    ]
    for i, sp in enumerate(json_lines):
        y += lh
        b.append(out(x0, y, sp, 0.27 + i * 0.02))
    y += lh * 1.5
    b.append(typed(3, x0, y, P + [("./ship --curiosity --intent", TXT)], 0.46, 0.60))
    y += lh
    b.append(out(x0, y, [("compiling ideas ........ ", MUT), ("done", "#22C55E")], 0.62))
    y += lh
    b.append(out(x0, y, [("all tests passed ", MUT), ("\u2713", "#22C55E")], 0.69))
    y += lh
    b.append(out(x0, y, [("deploying impact to production", BLUE), (" ...", MUT)], 0.76))
    y += lh * 1.4
    b.append(out(x0, y, [("$ ", RED)], 0.84))
    b.append(f'<rect x="{x0+20}" y="{y-15}" width="10" height="19" fill="{BLUE}" opacity="0"><animate attributeName="opacity" values="0;1;0;1;0" dur="1s" begin="0s" repeatCount="indefinite"/></rect>')
    return wrap(W, H, "".join(b))


# --------------------------------------------------------------------------- ID CARD
def idcard():
    W, H = 1000, 520
    photo = None
    for p in (os.path.join(OUT, "photo.jpg"), os.path.join(HERE, "photo.jpg"), os.path.join(HERE, "photo.png")):
        if os.path.exists(p):
            mime = "image/png" if p.endswith(".png") else "image/jpeg"
            photo = f"data:{mime};base64," + base64.b64encode(open(p, "rb").read()).decode()
            break
    rnd = random.Random(11)
    bars, bx = [], 132
    while bx < 380:
        w = rnd.choice([2, 2, 3, 4])
        bars.append(f'<rect x="{bx}" y="418" width="{w}" height="26" fill="#E2E8F0" fill-opacity=".85"/>')
        bx += w + rnd.choice([2, 3, 3, 4])
    if photo:
        pic = f'<image href="{photo}" x="132" y="150" width="256" height="196" preserveAspectRatio="xMidYMid slice" clip-path="url(#ph)"/>'
    else:
        pic = (f'<rect x="132" y="150" width="256" height="196" rx="14" fill="url(#gb)" fill-opacity=".35"/>'
               f'<circle cx="260" cy="226" r="42" fill="#0A1230" stroke="{BLUE}" stroke-width="2"/>'
               f'<path d="M168 346 C168 290 210 272 260 272 C310 272 352 290 352 346Z" fill="#0A1230" stroke="{BLUE}" stroke-width="2"/>'
               f'<text x="260" y="238" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="34" fill="{BLUE}">AH</text>')
    card = f'''<g>
<animateTransform attributeName="transform" type="rotate" values="-2.2 260 0;2.2 260 0;-2.2 260 0" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1" dur="6s" repeatCount="indefinite"/>
<rect x="242" y="-10" width="36" height="116" fill="url(#gb)"/>
<rect x="242" y="-10" width="36" height="116" fill="none" stroke="{BLUE}" stroke-opacity=".6"/>
<text transform="translate(265 -2) rotate(90)" font-family="{MONO}" font-size="11" font-weight="700" fill="#FFFFFF" fill-opacity=".8" letter-spacing="3">BUILD  BEYOND  BUILD  BEYOND</text>
<rect x="248" y="100" width="24" height="24" rx="6" fill="#0A1230" stroke="#CBD5E1" stroke-width="2"/>
<rect x="110" y="112" width="300" height="360" rx="22" fill="#0A1230" stroke="{BLUE}" stroke-width="2" filter="url(#glow)"/>
<rect x="110" y="112" width="300" height="360" rx="22" fill="url(#cardg)"/>
<rect x="110" y="112" width="300" height="6" rx="3" fill="url(#gr)"/>
<text x="132" y="146" font-family="{MONO}" font-size="12" font-weight="700" fill="{TXT}" letter-spacing="2">AH / BUILDER PASS</text>
<text x="388" y="146" text-anchor="end" font-family="{MONO}" font-size="12" font-weight="700" fill="{BLUE}">ZYV 001</text>
{pic}
<text x="132" y="380" font-family="{TITLE}" font-weight="900" font-size="26" fill="#FFFFFF">ABDUL HADI</text>
<text x="132" y="400" font-family="{MONO}" font-size="11" fill="{MUT}" letter-spacing="2">KATHMANDU / NEPAL</text>
<rect x="346" y="356" width="42" height="32" rx="6" fill="{GOLD}"/>
<path d="M346 366H388M346 378H388M360 356V388M374 356V388" stroke="#A16207" stroke-width="1.2"/>
{"".join(bars)}
<text x="132" y="462" font-family="{MONO}" font-size="9" fill="{MUT}" letter-spacing="2">INDEPENDENT CREATOR &#183; FOUNDER</text>
<g clip-path="url(#cc)"><rect x="-260" y="100" width="90" height="400" fill="url(#sheen)" transform="skewX(-18)"><animate attributeName="x" values="-260;520;520" keyTimes="0;0.55;1" dur="5s" repeatCount="indefinite"/></rect></g>
</g>'''
    defs = f'''<linearGradient id="cardg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#0F1B45"/><stop offset="1" stop-color="#1A0B2B"/></linearGradient>
<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity=".22"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>
<clipPath id="cc"><rect x="110" y="112" width="300" height="360" rx="22"/></clipPath>
<clipPath id="ph"><rect x="132" y="150" width="256" height="196" rx="14"/></clipPath>'''
    b = [blobs(W, H), particles(W, H, 22, 5), card]
    # right side
    b.append(slashes(500, 52, RED, 3, 16))
    b.append(f'<text x="548" y="66" font-family="{MONO}" font-size="14" font-weight="700" fill="{BLUE}" letter-spacing="3">BEHIND THE CODE</text>')
    b.append(f'<text x="500" y="132" font-family="{TITLE}" font-weight="900" font-size="46" fill="#FFFFFF">SHIPPING</text>')
    b.append(f'<text x="500" y="182" font-family="{TITLE}" font-weight="900" font-size="46" fill="url(#gb)">REAL THINGS.</text>')
    tiles = [("04", "ROLES HELD"), ("08", "PRODUCTS BUILT"), ("03", "BRANDS RUN")]
    for i, (n, l) in enumerate(tiles):
        tx = 500 + i * 158
        b.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.3+i*0.25:.2f}s" dur="0.6s" fill="freeze"/>
<rect x="{tx}" y="212" width="146" height="100" rx="14" fill="{PANEL2}" stroke="{BLUE}" stroke-opacity=".5"/>
<rect x="{tx}" y="212" width="146" height="4" rx="2" fill="url(#gr)"/>
<text x="{tx+18}" y="270" font-family="{TITLE}" font-weight="900" font-size="46" fill="url(#gb)">{n}</text>
<text x="{tx+18}" y="296" font-family="{MONO}" font-size="11" font-weight="700" fill="{MUT}" letter-spacing="1">{l}</text></g>''')
    b.append(f'<text x="500" y="340" font-family="{MONO}" font-size="12" font-weight="700" fill="{RED}" letter-spacing="3">FOCUS AREAS</text>')
    bars_def = [("AI ENGINEERING", 330), ("SOFTWARE ARCHITECTURE", 300), ("CYBERSECURITY", 262), ("FULL STACK WEB", 318)]
    for i, (l, wv) in enumerate(bars_def):
        yy = 368 + i * 26
        b.append(f'<text x="500" y="{yy+4}" font-family="{MONO}" font-size="12" fill="{TXT}">{l}</text>')
        b.append(f'<rect x="700" y="{yy-5}" width="260" height="10" rx="5" fill="{BLUE}" fill-opacity=".12"/>')
        b.append(f'<rect x="700" y="{yy-5}" width="0" height="10" rx="5" fill="url(#gb)" filter="url(#glow)"><animate attributeName="width" from="0" to="{wv*260/340:.0f}" begin="{0.6+i*0.3:.1f}s" dur="1.4s" fill="freeze"/></rect>')
    b.append(f'''<rect x="500" y="478" width="460" height="2" fill="{BLUE}" fill-opacity=".25"/>
<rect x="500" y="488" width="44" height="18" rx="4" fill="{RED}"/><text x="522" y="501" text-anchor="middle" font-family="{MONO}" font-size="10" font-weight="700" fill="#FFFFFF">NOW</text>
<text x="556" y="502" font-family="{SANS}" font-size="14" font-weight="700" fill="{TXT}">Building scalable software at Zyvora Technologies</text>''')
    return wrap(W, H, "".join(b), defs)


# --------------------------------------------------------------------------- ORBIT STACK
def orbit():
    W, H = 1000, 520
    cx, cy = 270, 260
    b = [particles(W, H, 18, 3), blobs(W, H).replace('opacity="0.55"', 'opacity="0.3"')]
    rings = [
        (95, 24, 1, BLUE, ["TS", "JS", "C#", "C++"]),
        (160, 36, -1, RED, ["React", "Next", "Node", "Exp", "PY"]),
        (225, 52, 1, BLUE, ["PG", "MySQL", "SB", "VCL", "Git", "GH"]),
    ]
    g = [f'<g transform="translate({cx} {cy})">']
    for r, dur, d, col, nodes in rings:
        g.append(f'<circle r="{r}" stroke="{col}" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="2 8"/>')
        a0, a1 = (0, 360) if d == 1 else (360, 0)
        c0, c1 = (360, 0) if d == 1 else (0, 360)
        g.append(f'<g><animateTransform attributeName="transform" type="rotate" from="{a0}" to="{a1}" dur="{dur}s" repeatCount="indefinite"/>')
        n = len(nodes)
        for k, lab in enumerate(nodes):
            ang = 2 * math.pi * k / n
            x, y = r * math.cos(ang), r * math.sin(ang)
            g.append(
                f'<g transform="translate({x:.1f} {y:.1f})"><g><animateTransform attributeName="transform" type="rotate" from="{c0}" to="{c1}" dur="{dur}s" repeatCount="indefinite"/>'
                f'<circle r="26" fill="{PANEL}" stroke="{col}" stroke-width="2" filter="url(#glow)"/>'
                f'<text y="4" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="#FFFFFF">{lab}</text></g></g>'
            )
        g.append("</g>")
    hexpts = " ".join(f"{44*math.cos(math.radians(60*k-30)):.1f},{44*math.sin(math.radians(60*k-30)):.1f}" for k in range(6))
    g.append(f'<polygon points="{hexpts}" fill="url(#gb)" fill-opacity=".35" stroke="{BLUE}" stroke-width="2" filter="url(#glow)"><animate attributeName="fill-opacity" values=".2;.55;.2" dur="3s" repeatCount="indefinite"/></polygon>')
    g.append(f'<text y="10" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="28" fill="#FFFFFF">AH</text></g>')
    b.append("".join(g))
    b.append(f'<line x1="540" y1="40" x2="540" y2="480" stroke="{BLUE}" stroke-opacity=".3"/>')
    cats = [
        ("01 / LANGUAGES", ["JavaScript", "TypeScript", "Python", "C", "C++", "C#"], BLUE),
        ("02 / FRONTEND & RUNTIME", ["HTML", "CSS", "React", "Next.js", "Node.js"], RED),
        ("03 / BACKEND, DATA & CLOUD", ["Express.js", ".NET", "PostgreSQL", "MySQL", "Supabase", "Vercel", "Railway"], BLUE),
        ("04 / TOOLING", ["Git", "GitHub", "Android Studio"], RED),
    ]
    y, di = 62, 0
    for lab, items, col in cats:
        b.append(f'<text x="570" y="{y}" font-family="{MONO}" font-size="12" font-weight="700" fill="{col}" letter-spacing="2">{esc(lab)}</text>')
        y += 14
        x = 570
        for it in items:
            w = len(it) * 12 * 0.62 + 28
            if x + w > 960:
                x = 570
                y += 38
            c, w = chip(x, y, it, col, size=12, h=28, delay=0.2 + di * 0.12)
            b.append(c)
            x += w + 8
            di += 1
        y += 58
    b.append(f'<text x="570" y="{H-26}" font-family="{MONO}" font-size="11" font-weight="700" fill="{MUT}" letter-spacing="2">CODE IS THE TOOL. IMPACT IS THE POINT.</text>')
    return wrap(W, H, "".join(b))


# --------------------------------------------------------------------------- PROJECTS
def projects():
    W, H = 1000, 584
    items = [
        ("ARIA", "Local first AI assistant with smart routing", ["AI", "LOCAL FIRST"]),
        ("School Management SaaS", "Multi tenant platform for schools", ["SaaS", "MULTI TENANT"]),
        ("WhatsApp AI Chatbot SaaS", "AI chatbots for businesses on WhatsApp", ["AI", "WHATSAPP"]),
        ("SkillBridge", "Education and job portal platform", ["EDUCATION", "JOBS"]),
        ("Learning Tracker SaaS", "Subscription learning tracker for students", ["NEXT.JS", "SUPABASE"]),
        ("Kirana Shop App", "Android inventory and ordering for local shops", ["ANDROID", "RETAIL"]),
        ("Restaurant Website Template", "Brandable site built to pitch to restaurants", ["WEB", "TEMPLATE"]),
        ("Nexus Global Travels", "Tours platform, Nepal and abroad packages", ["TRAVEL", "CTO"]),
    ]
    b, defs = [particles(W, H, 14, 9)], []
    cw, ch = 450, 118
    for i, (t, d, tags) in enumerate(items):
        col, row = i % 2, i // 2
        x, y = 40 + col * (cw + 20), 36 + row * (ch + 18)
        cid = f"pc{i}"
        defs.append(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16"/></clipPath>')
        accent = BLUE if (col + row) % 2 == 0 else RED
        tg, tx = [], x + 24
        for tag in tags:
            c, w = chip(tx, y + 84, tag, accent, size=10, h=22)
            tg.append(c)
            tx += w + 8
        b.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{i*0.15:.2f}s" dur="0.6s" fill="freeze"/>
<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="16" fill="{PANEL}" stroke="{accent}" stroke-opacity=".45"/>
<g clip-path="url(#{cid})">
<rect x="{x}" y="{y}" width="{cw}" height="4" fill="{accent}" fill-opacity=".8"/>
<rect x="{x-120}" y="{y}" width="120" height="{ch}" fill="url(#sheen)" transform="skewX(-14)"><animate attributeName="x" values="{x-160};{x+cw+60};{x+cw+60}" keyTimes="0;0.4;1" dur="{6+i%3}s" begin="{i*0.5:.1f}s" repeatCount="indefinite"/></rect>
<text x="{x+cw-16}" y="{y+ch-14}" text-anchor="end" font-family="{TITLE}" font-weight="900" font-size="64" fill="{accent}" fill-opacity=".10">{i+1:02d}</text>
</g>
<circle cx="{x+cw-26}" cy="{y+28}" r="5" fill="{accent}"><animate attributeName="r" values="4;7;4" dur="2s" repeatCount="indefinite"/><animate attributeName="opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/></circle>
<text x="{x+24}" y="{y+44}" font-family="{SANS}" font-weight="800" font-size="20" fill="#FFFFFF">{esc(t)}</text>
<text x="{x+24}" y="{y+68}" font-family="{SANS}" font-size="13" fill="{MUT}">{esc(d)}</text>
{"".join(tg)}</g>''')
    sheen = f'<linearGradient id="sheen" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0"/><stop offset="0.5" stop-color="#FFFFFF" stop-opacity=".07"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></linearGradient>'
    return wrap(W, H, "".join(b), "".join(defs) + sheen)


# --------------------------------------------------------------------------- ROADMAP
def roadmap():
    W, H = 1000, 340
    steps = [
        ("NOW", RED, ["Final year BSc IT", "AI research at Vectrah", "Shipping with Zyvora"]),
        ("NEXT", BLUE, ["Next.js, PostgreSQL", "Python and architecture", "AI agents, automation"]),
        ("GOAL", BLUE, ["Software architect and", "AI builder who gets", "recruited, not applying"]),
        ("VISION", RED, ["Zyvora, a multi", "subsidiary company:", "Technologies, Commerce,", "Academy, Studios"]),
    ]
    b = [blobs(W, H).replace('opacity="0.55"', 'opacity="0.3"'), particles(W, H, 12, 21)]
    b.append(f'<line x1="80" y1="100" x2="920" y2="100" stroke="{BLUE}" stroke-opacity=".3" stroke-width="3" stroke-dasharray="6 8"/>')
    b.append(f'<line x1="80" y1="100" x2="920" y2="100" stroke="url(#gb)" stroke-width="4" stroke-dasharray="0 900"><animate attributeName="stroke-dasharray" values="0 900;840 900;840 900" keyTimes="0;0.7;1" dur="6s" repeatCount="indefinite"/></line>')
    b.append(f'<circle r="8" fill="#FFFFFF" filter="url(#glow)"><animateMotion path="M80 100 H920" dur="6s" repeatCount="indefinite"/></circle>')
    for i, (lab, col, lines) in enumerate(steps):
        x = 140 + i * 240
        b.append(f'<circle cx="{x}" cy="100" r="16" fill="{PANEL}" stroke="{col}" stroke-width="3" filter="url(#glow)"><animate attributeName="r" values="14;19;14" dur="3s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></circle>')
        b.append(f'<circle cx="{x}" cy="100" r="5" fill="{col}"/>')
        b.append(f'<text x="{x}" y="64" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="24" fill="{col}">{lab}</text>')
        ts = "".join(f'<text x="{x}" y="{196+k*24}" text-anchor="middle" font-family="{SANS}" font-size="14.5" font-weight="600" fill="{TXT}">{esc(l)}</text>' for k, l in enumerate(lines))
        b.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.3+i*0.3:.1f}s" dur="0.6s" fill="freeze"/>
<rect x="{x-108}" y="150" width="216" height="150" rx="16" fill="{PANEL}" stroke="{col}" stroke-opacity=".5"/>
<rect x="{x-108}" y="150" width="216" height="4" rx="2" fill="{col}"/>
<text x="{x-92}" y="176" font-family="{MONO}" font-size="10" font-weight="700" fill="{MUT}" letter-spacing="2">0{i+1} / 04</text>{ts}</g>''')
    return wrap(W, H, "".join(b))


# --------------------------------------------------------------------------- SERVICES
def services():
    W, H = 1000, 320
    cards = [
        ("WEBSITES & SaaS", ["Business websites,", "portals and SaaS", "built to scale"], "web"),
        ("AI CHATBOTS", ["WhatsApp and web bots", "trained on your", "business data"], "chat"),
        ("AUTOMATION", ["Lead, email and", "workflow automation", "that saves hours"], "gear"),
        ("MOBILE APPS", ["Android apps for", "inventory, orders", "and local business"], "phone"),
    ]
    b = [particles(W, H, 12, 33)]
    for i, (t, lines, ic) in enumerate(cards):
        x, y = 40 + i * 235, 30
        col = BLUE if i % 2 == 0 else RED
        if ic == "web":
            icon = f'<rect x="0" y="0" width="60" height="44" rx="7" stroke="{col}" stroke-width="3"/><path d="M0 12H60" stroke="{col}" stroke-width="3"/><circle cx="9" cy="6" r="2" fill="{col}"/><circle cx="17" cy="6" r="2" fill="{col}"/><rect x="10" y="20" width="24" height="5" rx="2" fill="{col}" fill-opacity=".6"><animate attributeName="width" values="10;38;10" dur="3s" repeatCount="indefinite"/></rect><rect x="10" y="30" width="38" height="5" rx="2" fill="{col}" fill-opacity=".35"/>'
        elif ic == "chat":
            icon = f'<path d="M8 0H52A8 8 0 0 1 60 8V34A8 8 0 0 1 52 42H26L10 54V42H8A8 8 0 0 1 0 34V8A8 8 0 0 1 8 0Z" stroke="{col}" stroke-width="3"/><circle cx="18" cy="21" r="3.5" fill="{col}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle><circle cx="30" cy="21" r="3.5" fill="{col}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" begin=".25s" repeatCount="indefinite"/></circle><circle cx="42" cy="21" r="3.5" fill="{col}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" begin=".5s" repeatCount="indefinite"/></circle>'
        elif ic == "gear":
            icon = f'<g transform="translate(30 26)"><circle r="21" stroke="{col}" stroke-width="9" stroke-dasharray="9 7.5"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="10s" repeatCount="indefinite"/></circle><circle r="12" stroke="{col}" stroke-width="3"/></g>'
        else:
            icon = f'<rect x="12" y="-4" width="36" height="60" rx="9" stroke="{col}" stroke-width="3"/><rect x="24" y="2" width="12" height="3" rx="1.5" fill="{col}"/><rect x="19" y="14" width="22" height="22" rx="5" fill="{col}" fill-opacity=".35"><animate attributeName="fill-opacity" values=".15;.6;.15" dur="2.5s" repeatCount="indefinite"/></rect>'
        ts = "".join(f'<text x="{x+22}" y="{y+150+k*22}" font-family="{SANS}" font-size="14" fill="{MUT}">{esc(l)}</text>' for k, l in enumerate(lines))
        b.append(f'''<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{i*0.2:.1f}s" dur="0.6s" fill="freeze"/>
<rect x="{x}" y="{y}" width="215" height="215" rx="18" fill="{PANEL}" stroke="{col}" stroke-opacity=".5"/>
<rect x="{x}" y="{y}" width="215" height="4" rx="2" fill="{col}"/>
<g transform="translate({x+22} {y+34})">{icon}</g>
<text x="{x+22}" y="{y+120}" font-family="{TITLE}" font-weight="900" font-size="17" fill="#FFFFFF">{esc(t)}</text>{ts}</g>''')
    b.append(f'''<rect x="40" y="262" width="920" height="38" rx="19" fill="url(#gr)" fill-opacity=".14" stroke="{RED}" stroke-opacity=".7"/>
<circle cx="70" cy="281" r="5" fill="#22C55E"><animate attributeName="opacity" values="1;.2;1" dur="1.6s" repeatCount="indefinite"/></circle>
<text x="500" y="286" text-anchor="middle" font-family="{MONO}" font-size="13" font-weight="700" fill="{TXT}" letter-spacing="3">OPEN FOR FREELANCE PROJECTS AND COLLABORATIONS</text>''')
    return wrap(W, H, "".join(b))


# --------------------------------------------------------------------------- CONNECT
def connect():
    W, H = 1000, 290
    b = [blobs(W, H), particles(W, H, 18, 44), scanline(W, H)]
    rings = "".join(
        f'<circle cx="140" cy="145" r="10" stroke="{BLUE}" stroke-width="2"><animate attributeName="r" values="10;110" dur="3.6s" begin="{k*1.2:.1f}s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="3.6s" begin="{k*1.2:.1f}s" repeatCount="indefinite"/></circle>'
        for k in range(3))
    b.append(rings)
    b.append(f'<circle cx="140" cy="145" r="30" fill="url(#gb)" filter="url(#glow)"/><text x="140" y="156" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="28" fill="#FFFFFF">AH</text>')
    b.append(f'<text x="290" y="46" font-family="{MONO}" font-size="14" font-weight="700" fill="{RED}" letter-spacing="3">/// START A CONVERSATION</text>')
    b.append(f'<text x="286" y="138" font-family="{TITLE}" font-weight="900" font-size="82" fill="#FFFFFF">LET\'S</text>')
    b.append(f'<text x="286" y="222" font-family="{TITLE}" font-weight="900" font-size="82" fill="url(#gb)">CONNECT.</text>')
    b.append(f'<text x="290" y="262" font-family="{MONO}" font-size="14" fill="{MUT}" letter-spacing="2">BUILD SOMETHING GREAT. Ideas. Opportunities. Your next move.</text>')
    b.append(slashes(880, 190, RED, 3, 60))
    return wrap(W, H, "".join(b))


def button(name, label, handle, col, glyph):
    W, H = 260, 64
    g = f'<text x="34" y="39" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="14" fill="#FFFFFF">{glyph}</text>'
    if glyph == "PLAY":
        g = '<polygon points="28,24 28,42 43,33" fill="#FFFFFF"/>'
    body = f'''<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="16" fill="{PANEL}" stroke="{col}" stroke-width="2"><animate attributeName="stroke-opacity" values="1;.35;1" dur="2.8s" repeatCount="indefinite"/></rect>
<circle cx="34" cy="32" r="18" fill="{col}"/>{g.replace('y="39"','y="37"')}
<text x="64" y="29" font-family="{SANS}" font-weight="800" font-size="16" fill="#FFFFFF">{label}</text>
<text x="64" y="47" font-family="{MONO}" font-size="10.5" fill="{MUT}">{esc(handle)}</text>
<text x="{W-26}" y="38" text-anchor="end" font-family="{TITLE}" font-size="18" fill="{col}">&#8594;<animate attributeName="x" values="{W-30};{W-22};{W-30}" dur="1.6s" repeatCount="indefinite"/></text>'''
    svg = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" fill="none">{body}</svg>'
    save(name, svg)


# --------------------------------------------------------------------------- FOOTER
def footer():
    W, H = 1000, 190
    b = [particles(W, H, 10, 77)]
    for k, (col, amp, spd, y0, op) in enumerate(((DEEP, 16, 9, 120, .55), (BLUE, 12, 6, 132, .4), (RED, 10, 12, 146, .55))):
        pts = [f"{x},{y0+amp*math.sin(x/ (W/ (4*math.pi)))+0:.1f}" for x in range(0, 2 * W + 1, 20)]
        d = "M" + " L".join(pts) + f" L{2*W},{H} L0,{H}Z"
        b.append(f'<path d="{d}" fill="{col}" fill-opacity="{op}"><animateTransform attributeName="transform" type="translate" from="0 0" to="-{W/2:.0f} 0" dur="{spd}s" repeatCount="indefinite"/></path>')
    b.append(f'<text x="{W/2}" y="66" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="30" fill="url(#gb)">CURIOUS BY DEFAULT.</text>')
    b.append(f'<text x="{W/2}" y="104" text-anchor="middle" font-family="{TITLE}" font-weight="900" font-size="30" fill="#FFFFFF">BUILDING WITH INTENT.</text>')
    b.append(f'<text x="{W/2}" y="{H-14}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="#FFFFFF" fill-opacity=".8" letter-spacing="3">ABDUL HADI &#183; ZYVORA TECHNOLOGIES &#183; KATHMANDU</text>')
    return wrap(W, H, "".join(b))


if __name__ == "__main__":
    save("hero.svg", hero())
    save("terminal.svg", terminal())
    save("idcard.svg", idcard())
    save("orbit.svg", orbit())
    save("projects.svg", projects())
    save("roadmap.svg", roadmap())
    save("services.svg", services())
    save("connect.svg", connect())
    save("footer.svg", footer())
    section("sec1.svg", "01", "FROM THOUGHT TO THING", "IDEAS. BUILT DIFFERENT.")
    section("sec2.svg", "02", "BUILDER CREDENTIALS", "REAL WORK. REAL IMPACT.")
    section("sec3.svg", "03", "MY ENGINE ROOM", "TOOLS CHANGE. CURIOSITY DOESN'T.")
    section("sec4.svg", "04", "THINGS I BUILD", "IDEAS INTO PRODUCTS.")
    section("sec5.svg", "05", "THE ROADMAP", "WHERE THIS IS GOING.")
    section("sec6.svg", "06", "WORK WITH ME", "LET'S BUILD YOUR IDEA.")
    section("sec7.svg", "07", "LIVE FROM GITHUB", "THE COMMITS DON'T LIE.")
    button("btn-linkedin.svg", "LinkedIn", "in/abdulhadinp", "#0A66C2", "in")
    button("btn-youtube.svg", "YouTube", "@AbdulHadiNPL", "#E11D48", "PLAY")
    button("btn-instagram.svg", "Instagram", "@abdulhadinp", "#C13584", "IG")
    button("btn-portfolio.svg", "Portfolio", "abdulhadi.com.np", "#1D4ED8", "AH")
    button("btn-kaggle.svg", "Kaggle", "kaggle.com/abdulhadinp", "#0891B2", "K")
    button("btn-email.svg", "Email me", "abdulhadi4172@gmail.com", "#EA4335", "@")
    print("Done. Generated", len(os.listdir(OUT)), "files in", OUT)
