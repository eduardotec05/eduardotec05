#!/usr/bin/env python3
"""
Build a neofetch-style info card SVG to sit beside eduardo-ascii.svg.
Dimensions: 735 x 600 (scales cleanly to 490 x 400 alongside 370 x 400 portrait).
"""
import html
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "info-card.svg")
STATIC = bool(os.environ.get("STATIC"))

W, H = 735, 600
PAD = 24
TITLEBAR_H = 30
KEY_X = PAD + 4
VAL_X = PAD + 140
LINE_H = 22.5

BG = "#0d1117"
BG2 = "#111722"
FRAME = "#30363d"
MUTED = "#7d8590"
INK = "#c9d1d9"
KEY = "#ffa657"       # neofetch orange key
SECTION = "#58a6ff"   # terminal blue section title
GREEN = "#3fb950"
ACCENT = "#22d3ee"

ROWS = [
    ("host",),
    ("kv", "Now", "Full Stack Engineer @ CUTepa (Institutional Univ. Platform)"),
    ("kv", "Prev", "Full Stack & AI Developer @ CUAltos (UDG)"),
    ("kv", "Honors", "Top 20 @ Oracle ONE Hackathon (SentimentAPI Microservice)"),
    ("kv", "Education", "B.S. Computer Engineering @ Universidad de Guadalajara"),
    ("gap",),
    ("sec", "Technical Stack"),
    ("kv", "Languages", "TypeScript, JavaScript, Python, Java, C++, SQL"),
    ("kv", "Frontend", "Angular 20 (Signals, Standalone), React, Tailwind CSS"),
    ("kv", "Backend", "NestJS, Node.js, Spring Boot, Django, Flask"),
    ("kv", "Databases", "PostgreSQL, MongoDB, TypeORM, SQLAlchemy"),
    ("kv", "Cloud & DevOps", "AWS (S3, Lambda, Secrets), Google Cloud, Docker, CI/CD"),
    ("kv", "Core Focus", "Clean Architecture, Microservices, REST APIs, Security"),
    ("gap",),
    ("sec", "Certifications & Highlights"),
    ("bul", "Data Science Specialization — Oracle Next Education & Alura"),
    ("bul", "Google Cybersecurity & Google Cloud Foundations Certified"),
    ("bul", "Engineered NSGA-II Multi-Objective Genetic AI platform for teams"),
    ("bul", "Enterprise university portal architect (Keycloak, OpenPay, Gemini AI)"),
]


def esc(s):
    return html.escape(s)


def rise(inner, i):
    """Fade + subtle slide up on load, staggered by row."""
    if STATIC:
        return f"<g>{inner}</g>"
    delay = 0.15 + i * 0.05
    return (
        f'<g opacity="0" transform="translate(0,6)">{inner}'
        f'<animate attributeName="opacity" from="0" to="1" begin="{delay:.2f}s" dur="0.4s" fill="freeze"/>'
        f'<animateTransform attributeName="transform" type="translate" from="0 6" to="0 0" '
        f'begin="{delay:.2f}s" dur="0.4s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/></g>'
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, monospace">',
    '<defs>'
    f'<linearGradient id="ibg" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG2}"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>',
    f'<rect width="{W}" height="{H}" rx="12" fill="url(#ibg)"/>',
    f'<rect x="0.5" y="0.5" width="{W-1}" height="{H-1}" rx="12" fill="none" stroke="{FRAME}" stroke-width="1" stroke-opacity="0.8"/>',
    f'<line x1="0" y1="{TITLEBAR_H}" x2="{W}" y2="{TITLEBAR_H}" stroke="{FRAME}" stroke-opacity="0.6"/>',
]

for i, dotcol in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
    parts.append(f'<circle cx="{PAD + i*16}" cy="{TITLEBAR_H/2}" r="5" fill="{dotcol}"/>')
parts.append(f'<text x="{W/2}" y="{TITLEBAR_H/2 + 4}" fill="{MUTED}" font-size="12" '
             f'text-anchor="middle">eduardo@github: ~$ neofetch --profile</text>')

y = TITLEBAR_H + 28
for i, row in enumerate(ROWS):
    kind = row[0]
    if kind == "gap":
        y += LINE_H * 0.4
        continue
    if kind == "host":
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" font-size="14.5" font-weight="700">'
            f'<tspan fill="{GREEN}">eduardo</tspan><tspan fill="{MUTED}">@</tspan>'
            f'<tspan fill="{ACCENT}">github</tspan></text>'
            f'<line x1="{KEY_X+142}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.8"/>'
        )
    elif kind == "sec":
        title = esc(row[1])
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{SECTION}" font-size="12.5" font-weight="700">'
            f'&#8212; {title}</text>'
            f'<line x1="{KEY_X + 16 + len(row[1])*8.5}" y1="{y-4:.1f}" x2="{W-PAD}" y2="{y-4:.1f}" '
            f'stroke="{FRAME}" stroke-opacity="0.8"/>'
        )
    elif kind == "kv":
        key, val = esc(row[1]), esc(row[2])
        inner = (
            f'<text x="{KEY_X}" y="{y:.1f}" fill="{KEY}" font-size="12.5" font-weight="700">{key}</text>'
            f'<text x="{VAL_X}" y="{y:.1f}" fill="{INK}" font-size="12.5">{val}</text>'
        )
    elif kind == "bul":
        txt = esc(row[1])
        inner = (
            f'<circle cx="{KEY_X+4}" cy="{y-4:.1f}" r="3" fill="{GREEN}"/>'
            f'<text x="{KEY_X+16}" y="{y:.1f}" fill="{INK}" font-size="12.5">{txt}</text>'
        )
    else:
        continue
    parts.append(rise(inner, i))
    y += LINE_H

parts.append("</svg>")
svg = "".join(parts)
with open(OUT, "w") as f:
    f.write(svg)
print(f"wrote {OUT} ({len(svg)} bytes; {W}x{H})")
