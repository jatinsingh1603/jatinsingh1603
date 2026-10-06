#!/usr/bin/env python3
"""Render self-contained research artwork for the GitHub profile.

Run: python3 render_evidence_art.py
Uses original vector illustrations and the official marks documented in
profile-assets/SOURCES.md. No network requests or external fonts are needed.
"""
from base64 import b64encode
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'profile-assets'
INK, RED, PAPER = '#101012', '#ed3025', '#f7f5f1'


def image(name, x, y, width, height):
    path = ASSETS / name
    mime = 'image/svg+xml' if path.suffix == '.svg' else 'image/png'
    data = b64encode(path.read_bytes()).decode()
    return f'<image x="{x}" y="{y}" width="{width}" height="{height}" preserveAspectRatio="xMidYMid meet" xlink:href="data:{mime};base64,{data}"/>'


def folder(x, y, width, org, mobile=False):
    phone = org == 'Blinkit'
    amount = '$1,500' if phone else '$500'
    size = 100 if mobile else 90
    tilt = 0 if mobile else (-2 if phone else 2)
    emblem_x = width - 147
    device = f'''<g transform="translate({emblem_x} 31)" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round">
<rect x="16" y="0" width="78" height="126" rx="15"/>
<path d="M42 11h26M46 113h18" stroke-width="4" stroke-linecap="round"/>
<path d="M36 36h26l14 14v37H36Z" stroke="{RED}"/>
<path d="M62 36v14h14M46 62h18M46 72h13" stroke="{RED}" stroke-width="3"/>
</g>''' if phone else f'''<g transform="translate({emblem_x-12} 32)" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round">
<rect x="0" y="0" width="127" height="89" rx="10"/><path d="M45 90v21m37-21v21M31 112h67" stroke-linecap="round"/>
<rect x="46" y="38" width="36" height="30" rx="5" stroke="{RED}"/>
<path d="M53 37v-8a11 11 0 0 1 22 0v8" stroke="{RED}"/>
<circle cx="64" cy="52" r="3" fill="{RED}" stroke="none"/>
</g>'''
    logo = f'<rect x="31" y="217" width="256" height="79" rx="13" fill="{PAPER}"/>' + image('blinkit.png', 53, 232, 212, 49) if phone else image('kraken-icon.png', 31, 215, 82, 82) + f'<text x="131" y="271" fill="{PAPER}" font-size="45" font-weight="700">Kraken</text>'
    status = 'AWARDED' if phone else 'AWARDED · RESOLVED'
    label = 'Android application' if phone else 'Desktop application'
    return f'''<g transform="translate({x} {y}) rotate({tilt} {width/2} 173)">
<rect x="6" y="46" width="{width}" height="320" rx="24" fill="#000000" opacity=".65" filter="url(#depth)"/>
<path d="M0 70V52a16 16 0 0 1 16-16h146a17 17 0 0 1 13 6l21 25h{width-213}a17 17 0 0 1 17 17v234a20 20 0 0 1-20 20H20a20 20 0 0 1-20-20Z" fill="url(#back)" stroke="#76767c" stroke-width="2"/>
<rect x="20" y="7" width="{width-40}" height="238" rx="14" fill="#a8a7a2"/>
<rect x="26" y="0" width="{width-52}" height="238" rx="14" fill="url(#paper)"/>
<text x="48" y="113" fill="{INK}" font-size="{size}" font-weight="700" letter-spacing="-4">{amount}</text>
<text x="49" y="158" fill="#ab231c" font-size="{34 if mobile else 28}" font-weight="700">{status}</text>
{device}
<path d="M0 190h{width}v137a20 20 0 0 1-20 20H20a20 20 0 0 1-20-20Z" fill="url(#cover)" stroke="#79797f" stroke-width="2"/>
<path d="M1 190h{width-2}" stroke="{RED}" stroke-width="3"/>
<path d="M12 196h{width-24}" stroke="#64646a" stroke-width="1"/>
<path d="M12 209v122a13 13 0 0 0 13 13h{width-50}" fill="none" stroke="#34343a" stroke-width="2"/>
{logo}
<text x="33" y="331" fill="#d2d0cc" font-size="{34 if mobile else 28}">{label}</text>
<path d="M{width-39} 217v66" stroke="#45454a" stroke-width="3" stroke-linecap="round"/>
</g>'''


def tab(org, x, y, width, height=124, mobile=False):
    logo_width = min(width-40, 165)
    center = width/2
    mark = ''
    if org == 'Google':
        mark = image('google.svg', center-logo_width/2, 47, logo_width, 53)
    elif org == 'Meesho':
        mark = image('meesho.svg', center-logo_width/2, 48, logo_width, 47)
    elif org == 'NorthCap':
        mark = image('ncu.svg', 22 if mobile else center-26, 37 if mobile else 28, 66 if mobile else 52, 63 if mobile else 46) + f'<text x="{width-18 if mobile else center}" y="{80 if mobile else 108}" text-anchor="{"end" if mobile else "middle"}" font-size="{34 if mobile else 28}" font-weight="700" fill="{INK}">NorthCap</text>'
    else:
        mark = f'<text x="{center}" y="82" text-anchor="middle" font-size="{43 if mobile else 38}" font-weight="700" fill="{INK}">{org}</text>'
    return f'''<g transform="translate({x} {y})">
<path d="M0 31V14A14 14 0 0 1 14 0h{width//2-29}a14 14 0 0 1 10 4l15 15h{width-width//2-10}a14 14 0 0 1 14 14v{height-47}a14 14 0 0 1-14 14H14A14 14 0 0 1 0 {height-14}Z" fill="{PAPER}"/>
<path d="M20 17h{min(width//2-29,75)}" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>
{mark}
</g>'''


def wrap(width, height, content):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Security research casebook: $2,000 in awarded bounties</title>
<desc id="desc">Blinkit: $1,500 awarded for an Android application arbitrary file read. Kraken: $500 awarded for a desktop application security misconfiguration, resolved. Other research: Google acknowledged and reported; Meta reported; IRCTC acknowledged by CERT-In; NorthCap University authorised testing; Meesho identified. Organisation marks identify research records and do not imply endorsement.</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}}</style>
<defs>
<linearGradient id="cover" x1="0" y1="0" x2=".55" y2="1"><stop stop-color="#37373d"/><stop offset=".3" stop-color="#232327"/><stop offset="1" stop-color="#121215"/></linearGradient>
<linearGradient id="back" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#48484f"/><stop offset="1" stop-color="#1d1d21"/></linearGradient>
<linearGradient id="paper" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#ffffff"/><stop offset=".68" stop-color="#f7f5f1"/><stop offset="1" stop-color="#b3b1ac"/></linearGradient>
<radialGradient id="ambient"><stop stop-color="#731810" stop-opacity=".23"/><stop offset="1" stop-color="#101012" stop-opacity="0"/></radialGradient>
<filter id="depth" x="-.12" y="-.12" width="1.3" height="1.4"><feGaussianBlur stdDeviation="9"/></filter>
</defs>
<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="32" fill="{INK}" stroke="#353538" stroke-width="2"/>
<ellipse cx="{width/2}" cy="{height*.48}" rx="{width*.55}" ry="{height*.43}" fill="url(#ambient)"/>
{content}
</svg>\n'''


desktop = f'''
<text x="64" y="70" fill="#d2d0cc" font-size="30" letter-spacing="2">THE RESEARCH FILES</text>
<text x="58" y="185" fill="{RED}" font-size="109" font-weight="700" letter-spacing="-5">$2,000</text>
<text x="428" y="143" fill="{PAPER}" font-size="32" font-weight="700">BOUNTIES AWARDED</text>
<text x="429" y="183" fill="#c4c2be" font-size="28">Two findings. Documented outcomes.</text>
<path d="M345 580v47h584v-47M173 627h935M173 627v37m234-37v37m234-37v37m234-37v37m233-37v37" fill="none" stroke="#68302c" stroke-width="2"/>
{folder(64,236,552,'Blinkit')}
{folder(664,236,552,'Kraken')}
{tab('Google',64,664,218)}
{tab('Meta',298,664,218)}
{tab('IRCTC',532,664,218)}
{tab('NorthCap',766,664,218)}
{tab('Meesho',1000,664,218)}
'''

mobile = f'''
<text x="50" y="65" fill="#d2d0cc" font-size="34" letter-spacing="1.5">THE RESEARCH FILES</text>
<text x="44" y="173" fill="{RED}" font-size="110" font-weight="700" letter-spacing="-5">$2,000</text>
<text x="414" y="129" fill="{PAPER}" font-size="34" font-weight="700">BOUNTIES</text>
<text x="414" y="168" fill="{PAPER}" font-size="34" font-weight="700">AWARDED</text>
<path d="M379 930v52M160 982h442m-442 0v29m221-29v29m221-29v29M379 1139v35" fill="none" stroke="#68302c" stroke-width="3"/>
{folder(50,220,660,'Blinkit',True)}
{folder(50,605,660,'Kraken',True)}
{tab('Google',50,1010,210,130,True)}
{tab('Meta',275,1010,210,130,True)}
{tab('IRCTC',500,1010,210,130,True)}
{tab('NorthCap',50,1176,321,130,True)}
{tab('Meesho',389,1176,321,130,True)}
'''

(ASSETS/'research-board.svg').write_text(wrap(1280,826,desktop))
(ASSETS/'research-board-mobile.svg').write_text(wrap(760,1354,mobile))
print('Generated research-board.svg and research-board-mobile.svg')
