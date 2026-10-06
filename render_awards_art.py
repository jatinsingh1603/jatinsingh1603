#!/usr/bin/env python3
"""Render original recognition illustrations from Jatin's public career record.

Run: python3 render_awards_art.py
Only the two recognition-board SVGs are written. No network or dependencies.
The illustrated seal and medals are decorative, not official credential marks.
"""
from html import escape
from math import cos, sin, pi
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "profile-assets"
INK = "#101012"
RED = "#ed3025"
PAPER = "#f7f5f1"


def text(x, y, value, size=28, color=PAPER, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" fill="{color}" font-size="{size}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{escape(value)}</text>')


def rect(x, y, width, height, fill, radius=24, stroke=None):
    border = f' stroke="{stroke}" stroke-width="2"' if stroke else ""
    return (f'<rect x="{x}" y="{y}" width="{width}" height="{height}" '
            f'rx="{radius}" fill="{fill}"{border}/>')


def star(cx, cy, outer, inner, count=5, fill=RED):
    points = []
    for index in range(count * 2):
        angle = -pi / 2 + index * pi / count
        radius = outer if index % 2 == 0 else inner
        points.append(f"{cx + cos(angle) * radius:.2f},{cy + sin(angle) * radius:.2f}")
    return f'<polygon points="{" ".join(points)}" fill="{fill}"/>'


TROPHY = f'''
<ellipse cx="100" cy="191" rx="86" ry="13" fill="#09090b"/>
<path d="M46 27H19v29c0 31 20 45 47 45M154 27h27v29c0 31-20 45-47 45" fill="none" stroke="{RED}" stroke-width="12"/>
<path d="M43 11h114v51c0 41-20 66-57 72-37-6-57-31-57-72Z" fill="#b2afaa"/>
<path d="M43 5h108v51c0 41-18 65-51 72-36-7-57-31-57-72Z" fill="{PAPER}"/>
<path d="M83 126h34v29H83Z" fill="{RED}"/>
<path d="M66 153h68l12 22H54Z" fill="{PAPER}"/>
<rect x="43" y="173" width="114" height="20" rx="6" fill="{RED}"/>
{star(98, 57, 25, 11)}
'''

PODIUM = f'''
<ellipse cx="100" cy="191" rx="91" ry="13" fill="#09090b"/>
<rect x="12" y="126" width="53" height="60" rx="8" fill="#aaa7a2"/>
<rect x="12" y="120" width="53" height="60" rx="8" fill="{PAPER}"/>
<rect x="137" y="106" width="53" height="80" rx="8" fill="#aaa7a2"/>
<rect x="137" y="100" width="53" height="80" rx="8" fill="{PAPER}"/>
<rect x="70" y="58" width="61" height="130" rx="9" fill="#981d17"/>
<rect x="66" y="50" width="66" height="130" rx="9" fill="{RED}"/>
<path d="M84 16h32M100 0v32" stroke="{RED}" stroke-width="6" stroke-linecap="round"/>
{text(99, 117, '2', 57, INK, 700, 'middle')}
'''

MEDAL = f'''
<ellipse cx="100" cy="191" rx="83" ry="13" fill="#09090b"/>
<path d="M53 0h37l24 78-29 12Z" fill="{PAPER}"/>
<path d="M110 0h37l-32 90-29-12Z" fill="{RED}"/>
<path d="M54 138l-7 60 34-17 24 14 8-60Z" fill="#a51e18"/>
<circle cx="100" cy="120" r="61" fill="#8f1a15"/>
<circle cx="100" cy="113" r="61" fill="{RED}"/>
<circle cx="100" cy="113" r="46" fill="{PAPER}"/>
<circle cx="100" cy="113" r="37" fill="none" stroke="{INK}" stroke-width="2"/>
{star(100, 113, 26, 12, fill=INK)}
'''

CTF = f'''
<ellipse cx="100" cy="191" rx="87" ry="13" fill="#09090b"/>
<path d="M36 39v69c0 42 31 70 64 79 33-9 64-37 64-79V39L100 9Z" fill="#8f1a15"/>
<path d="M36 31v69c0 42 31 70 64 79 33-9 64-37 64-79V31L100 1Z" fill="{RED}"/>
<path d="M49 40v58c0 34 23 57 51 67 28-10 51-33 51-67V40l-51-24Z" fill="{PAPER}"/>
{text(100, 118, '7', 75, INK, 700, 'middle')}
<path d="M13 140c-16-36-3-72 13-91M187 140c16-36 3-72-13-91" fill="none" stroke="{PAPER}" stroke-width="4" stroke-linecap="round"/>
<path d="m9 111-9-15m11-4 10-13m-9-5L8 58m182 53 9-15m-10-4-10-13m9-5 4-16" fill="none" stroke="{PAPER}" stroke-width="6" stroke-linecap="round"/>
'''

DIPLOMA = f'''
<g transform="rotate(-7 106 100)">
<rect x="33" y="66" width="142" height="114" rx="9" fill="#aaa7a2"/>
<rect x="26" y="59" width="142" height="114" rx="9" fill="{PAPER}"/>
<path d="M50 88h90M50 106h64M50 124h74" stroke="#aaa7a2" stroke-width="6" stroke-linecap="round"/>
<path d="m130 143-8 37 15-8 14 9-7-38" fill="{RED}"/>
<circle cx="137" cy="140" r="17" fill="{RED}"/>
</g>
<path d="M7 37 104 2l98 35-98 36Z" fill="{RED}"/>
<path d="M49 59v31c30 21 78 21 110 0V59l-55 20Z" fill="#b12119"/>
<path d="M188 40v44" stroke="{PAPER}" stroke-width="4"/>
<path d="M188 81v17" stroke="{PAPER}" stroke-width="9" stroke-linecap="round"/>
'''


def award_card(x, y, width, height, icon, placement, event, detail="", mobile=False):
    size = 32 if mobile else 28
    scale = 0.94 if mobile else 0.82
    center = width / 2
    content = rect(0, 8, width, height, "#09090b")
    content += rect(0, 0, width, height, "#1a1a1d", 24, "#3e3e43")
    content += f'<g transform="translate({center - 100 * scale} 27) scale({scale})">{icon}</g>'
    content += text(center, 231 if mobile else 215, placement, 35 if mobile else 30, PAPER, 700, "middle")
    content += text(center, 280 if mobile else 259, event, size, PAPER, 400, "middle")
    if detail:
        content += text(center, 324 if mobile else 299, detail, size, "#cbc8c4", 400, "middle")
    return f'<g transform="translate({x} {y})">{content}</g>'


def seal(cx, cy, radius):
    result = f'<path d="M{cx - 58} {cy + 51}l-18 105 61-26 20 25 7-104Z" fill="#ba241b"/>'
    result += f'<path d="M{cx + 58} {cy + 51}l18 105-61-26-20 25-7-104Z" fill="{RED}"/>'
    result += star(cx, cy, radius, radius - 11, 18)
    result += f'<circle cx="{cx}" cy="{cy}" r="{radius - 18}" fill="{PAPER}"/>'
    result += f'<circle cx="{cx}" cy="{cy}" r="{radius - 29}" fill="none" stroke="{RED}" stroke-width="2"/>'
    result += f'<g transform="translate({cx - 36} {cy - 39})"><path d="M14 34V20a22 22 0 0 1 44 0v14" fill="none" stroke="{INK}" stroke-width="8"/><rect y="29" width="72" height="54" rx="10" fill="{INK}"/><circle cx="36" cy="52" r="7" fill="{PAPER}"/><path d="M36 53v14" stroke="{PAPER}" stroke-width="5"/></g>'
    return result


def credential_card(x, y, width, height, mobile=False):
    result = rect(0, 0, width, height, PAPER, 24)
    if mobile:
        result += seal(132, 156, 89)
        result += text(266, 113, "CRTP", 76, INK, 700)
        result += text(266, 167, "Certified Red Team", 32, INK)
        result += text(266, 210, "Professional", 32, INK)
        result += text(266, 268, "Altered Security", 32, "#a42119", 700)
    else:
        result += seal(133, 145, 91)
        result += text(272, 101, "CRTP", 76, INK, 700)
        result += text(274, 153, "Certified Red Team", 28, INK)
        result += text(274, 194, "Professional", 28, INK)
        result += text(274, 253, "Altered Security", 30, "#a42119", 700)
    return f'<g transform="translate({x} {y})">{result}</g>'


def education_card(x, y, width, height, mobile=False):
    result = rect(0, 0, width, height, "#1a1a1d", 24, "#3e3e43")
    if mobile:
        result += f'<g transform="translate(36 42) scale(.92)">{DIPLOMA}</g>'
        result += text(270, 80, "B.Tech CSE", 40, PAPER, 700)
        result += text(270, 130, "Cyber Security", 32, PAPER)
        result += text(270, 184, "2027 expected", 32, "#cbc8c4")
        result += text(270, 238, "CGPA 8.31", 32, PAPER, 700)
        result += text(36, 306, "The NorthCap University", 32, PAPER)
    else:
        result += f'<g transform="translate(30 25) scale(.62)">{DIPLOMA}</g>'
        result += text(187, 76, "B.Tech CSE", 32, PAPER, 700)
        result += text(187, 119, "Cyber Security", 28, PAPER)
        result += text(30, 198, "The NorthCap University", 28, PAPER)
        result += text(30, 246, "2027 expected", 28, "#cbc8c4")
        result += text(30, 291, "CGPA 8.31", 30, PAPER, 700)
    return f'<g transform="translate({x} {y})">{result}</g>'


DESCRIPTION = (
    "Recognition: Winner, Eclipse 6.0 Hackathon; 2nd Place in the Security Domain, "
    "India Innovates; 2nd Runner-Up, Sprint4Good; 7th Place, GenCyS 2.0 CTF. "
    "Certified Red Team Professional from Altered Security. "
    "B.Tech Computer Science and Engineering, Cyber Security specialisation, "
    "The NorthCap University, expected 2027, CGPA 8.31. "
    "Original illustrative award objects and seal, not official credential badges."
)


def document(width, height, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="recognition-title recognition-desc">
<title id="recognition-title">Jatin Kumar Singh / Recognition and qualifications</title>
<desc id="recognition-desc">{escape(DESCRIPTION)}</desc>
<style>text {{ font-family: Arial, Helvetica, sans-serif; }}</style>
<rect x="1" y="1" width="{width - 2}" height="{height - 2}" rx="32" fill="{INK}" stroke="#353538" stroke-width="2"/>
{body}
</svg>
'''


def render():
    OUT.mkdir(exist_ok=True)
    desktop = text(48, 64, "RECOGNITION", 32, PAPER, 700)
    desktop += '<path d="M48 84h1184" stroke="#3e3e43" stroke-width="2"/>'
    desktop += award_card(48, 111, 278, 333, TROPHY, "Winner", "Eclipse 6.0")
    desktop += award_card(350, 111, 278, 333, PODIUM, "2nd Place", "India Innovates", "Security Domain")
    desktop += award_card(652, 111, 278, 333, MEDAL, "2nd Runner-Up", "Sprint4Good")
    desktop += award_card(954, 111, 278, 333, CTF, "7th Place", "GenCyS 2.0", "CTF")
    desktop += credential_card(48, 480, 704, 330)
    desktop += education_card(778, 480, 454, 330)
    (OUT / "recognition-board.svg").write_text(document(1280, 852, desktop), encoding="utf-8")

    mobile = text(40, 67, "RECOGNITION", 36, PAPER, 700)
    mobile += '<path d="M40 91h680" stroke="#3e3e43" stroke-width="2"/>'
    mobile += award_card(40, 121, 326, 355, TROPHY, "Winner", "Eclipse 6.0", mobile=True)
    mobile += award_card(394, 121, 326, 355, PODIUM, "2nd Place", "India Innovates", "Security Domain", mobile=True)
    mobile += award_card(40, 504, 326, 355, MEDAL, "2nd Runner-Up", "Sprint4Good", mobile=True)
    mobile += award_card(394, 504, 326, 355, CTF, "7th Place", "GenCyS 2.0", "CTF", mobile=True)
    mobile += credential_card(40, 897, 680, 331, mobile=True)
    mobile += education_card(40, 1257, 680, 349, mobile=True)
    (OUT / "recognition-board-mobile.svg").write_text(document(760, 1646, mobile), encoding="utf-8")
    print("Generated recognition-board.svg and recognition-board-mobile.svg")


if __name__ == "__main__":
    render()
