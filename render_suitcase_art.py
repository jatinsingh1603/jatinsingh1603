#!/usr/bin/env python3
"""Render the portfolio's rolling suitcase as self-contained GitHub SVG artwork.

Default: python3 render_suitcase_art.py
Still frame: python3 render_suitcase_art.py --time 9.8 --output /tmp/lock.svg
Mobile frame: python3 render_suitcase_art.py --mobile --time 9.8 --output /tmp/lock-mobile.svg

The live SVG uses native CSS transform animation. --time evaluates the same
keyframes and cubic-bezier easing in Python, so PNG/GIF fallbacks can be rendered
without a browser. Official identity mark is reused from components/brand-mark.tsx.
"""
from argparse import ArgumentParser
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'profile-assets'
WORDS = ('SECURITY', 'AUTOMATION', 'BUG BOUNTY', 'RED TEAMING', 'WEB & API',
         'MOBILE VAPT', 'LOG ANALYSIS', 'AI AGENTS', 'GRC')
WHEEL_COUNT = 12
HOLD_SECONDS = 4.0
ROLL_SECONDS = .9
CASCADE_SECONDS = .025
STEP_SECONDS = 5.2
LOOP_SECONDS = STEP_SECONDS * len(WORDS)
INK, RED, PAPER = '#101012', '#ed3025', '#f7f5f1'

MARK = '''<rect width="64" height="64" rx="14" fill="#ed3025"/>
<path d="M49 29A20 20 0 1 0 29 49V42A13 13 0 1 1 42 29H49Z" fill="#101012"/>
<path d="M53 34H46A12 12 0 0 1 34 46V53A19 19 0 0 0 53 34Z" fill="#101012"/>
<path d="M29 22a5 5 0 0 0-2.25 9.47L25 38h8l-1.75-6.53A5 5 0 0 0 29 22Z" fill="#101012"/>'''


def ease(progress):
    """CSS cubic-bezier(.65, 0, .35, 1), solved for its x coordinate."""
    lo, hi = 0.0, 1.0
    for _ in range(35):
        t = (lo + hi) / 2
        x = 3*(1-t)**2*t*.65 + 3*(1-t)*t*t*.35 + t**3
        if x < progress:
            lo = t
        else:
            hi = t
    t = (lo + hi) / 2
    return 3*(1-t)*t*t + t**3


def wheel_row(time, column):
    time %= LOOP_SECONDS
    step = int(time // STEP_SECONDS)
    phase = time - step*STEP_SECONDS
    beginning = HOLD_SECONDS + column*CASCADE_SECONDS
    p = min(1.0, max(0.0, (phase-beginning)/ROLL_SECONDS))
    return step + ease(p)


def animation_css(row_height):
    styles = [f'''.roller {{ animation-duration: {LOOP_SECONDS:g}s; animation-iteration-count: infinite;
 animation-timing-function: cubic-bezier(.65,0,.35,1); transform: translateY(0px); }}''']
    for column in range(WHEEL_COUNT):
        frames = ['0% { transform:translateY(0px) }']
        for row in range(len(WORDS)):
            start = row*STEP_SECONDS+HOLD_SECONDS+column*CASCADE_SECONDS
            end = start+ROLL_SECONDS
            frames += [f'{start/LOOP_SECONDS*100:.8f}% {{ transform:translateY({-row*row_height:g}px) }}',
                       f'{end/LOOP_SECONDS*100:.8f}% {{ transform:translateY({-(row+1)*row_height:g}px) }}']
        frames += [f'100% {{ transform:translateY({-len(WORDS)*row_height:g}px) }}']
        styles.append(f'.wheel-{column} {{ animation-name:roll-{column} }}\n@keyframes roll-{column} {{ '+ ' '.join(frames)+' }')
    styles.append('@media (prefers-reduced-motion: reduce) { .roller { animation:none!important; transform:translateY(0px)!important; } }')
    return '\n'.join(styles)


def reels(case_width, row_height, mobile, time):
    left, gap = (28, 3) if mobile else (55, 4)
    span = case_width-left*2
    wheel_width = (span-gap*(WHEEL_COUNT-1))/WHEEL_COUNT
    font_size = 50 if mobile else 86
    baseline = row_height/2+font_size*.355
    words = [w.center(WHEEL_COUNT) for w in (*WORDS, WORDS[0])]
    columns = []
    for column in range(WHEEL_COUNT):
        glyphs = ''.join(f'<text x="{wheel_width/2:.4f}" y="{row*row_height+baseline:.4f}" text-anchor="middle">{escape(word[column])}</text>' for row, word in enumerate(words))
        transform = '' if time is None else f' transform="translate(0 {-wheel_row(time,column)*row_height:.5f})"'
        classes = f' class="roller wheel-{column}"' if time is None else ''
        columns.append(f'''<g transform="translate({left+column*(wheel_width+gap):.4f} 80)">
<rect width="{wheel_width:.4f}" height="{row_height}" rx="5" fill="{PAPER}"/>
<g clip-path="url(#slot)"><g{classes}{transform} fill="#161618" font-size="{font_size}" font-weight="700">{glyphs}</g></g>
<rect width="{wheel_width:.4f}" height="{row_height}" rx="5" fill="url(#reel-shade)"/>
<path d="M0 {row_height/2:g}h{wheel_width:.4f}" stroke="#000000" stroke-opacity=".17"/>
<path d="M1 5v{row_height-10}" stroke="#ffffff" stroke-opacity=".22"/>
</g>''')
    return f'<clipPath id="slot"><rect width="{wheel_width:.4f}" height="{row_height}" rx="5"/></clipPath>', '\n'.join(columns)


def suitcase(width, height, row_height, mobile, time):
    left = 28 if mobile else 55
    slot_def, wheels = reels(width,row_height,mobile,time)
    label_size = 32 if mobile else 28
    handle = f'''<g transform="translate({width/2} 0)">
<rect x="-115" y="-13" width="40" height="28" rx="7" fill="url(#metal)" stroke="#161618"/>
<rect x="75" y="-13" width="40" height="28" rx="7" fill="url(#metal)" stroke="#161618"/>
<path d="M-95-2v-25a18 18 0 0 1 18-18H77a18 18 0 0 1 18 18v25" fill="none" stroke="#131315" stroke-width="22"/>
<path d="M-99-3v-25a20 20 0 0 1 20-20H79a20 20 0 0 1 20 20v25" fill="none" stroke="#68656a" stroke-width="2"/>
</g>'''
    bolts = ''.join(f'<g transform="translate({x} {y})"><circle r="5" fill="url(#metal)" stroke="#09090a"/><path d="M-2 0h4" stroke="#080809"/></g>' for x,y in ((20,20),(width-20,20),(20,height-20),(width-20,height-20)))
    caption_size = 32 if mobile else 28
    return slot_def, f'''{handle}
<rect x="1" y="15" width="{width-2}" height="{height}" rx="31" fill="#09090b" stroke="#793c34" stroke-width="2"/>
<rect width="{width}" height="{height}" rx="31" fill="url(#case-cover)" stroke="#777175" stroke-width="2"/>
<rect x="7" y="7" width="{width-14}" height="{height-14}" rx="26" fill="none" stroke="#ffffff" stroke-opacity=".09"/>
<path d="M31 2h{width-62}" stroke="#ffffff" stroke-opacity=".32"/>
{bolts}
<text x="{left}" y="50" fill="#c2bebe" font-size="{label_size}" letter-spacing="1">SECURITY + AUTOMATION</text>
<rect x="{left-7}" y="73" width="{width-2*left+14}" height="{row_height+14}" rx="10" fill="#070708" stroke="#09090a" stroke-width="2"/>
<path d="M{left} {row_height+88}h{width-left*2}" stroke="#736d72" stroke-width="2"/>
{wheels}
<text x="{width/2}" y="{height-32}" text-anchor="middle" fill="#c2bebe" font-size="{caption_size}">INVESTIGATE. VALIDATE. AUTOMATE.</text>
<g transform="translate({width/2-32} {height-8})"><rect width="64" height="36" rx="6" fill="url(#metal)" stroke="#111113" stroke-width="2"/><rect x="18" y="9" width="28" height="17" rx="4" fill="#111113" stroke="#636167"/></g>'''


def build(mobile=False, time=None):
    width, height = (760,800) if mobile else (1280,650)
    case_width, case_height = (696,288) if mobile else (1148,316)
    case_x, case_y = (32,361) if mobile else (66,273)
    row_height = 128 if mobile else 148
    slot_def, case = suitcase(case_width,case_height,row_height,mobile,time)
    css = animation_css(row_height) if time is None else ''
    name = '<text x="46" y="139" font-size="60" font-weight="600" letter-spacing="-2">Jatin Kumar Singh</text><text x="48" y="193" font-size="34">Information Security Analyst</text>' if mobile else '<text x="61" y="126" font-size="75" font-weight="600" letter-spacing="-2.6">Jatin Kumar Singh</text><text x="66" y="183" font-size="32">Information Security Analyst</text>'
    mark = f'<g transform="translate({638 if mobile else 1122} {226 if mobile else 73}) scale({.9 if mobile else 1.18})">{MARK}</g>'
    # The brand tile is deliberately distinct from the stage, preserving its original mark.
    brand_back = '<rect x="630" y="218" width="75" height="75" rx="19" fill="#101012"/>' if mobile else '<rect x="1112" y="63" width="96" height="96" rx="23" fill="#101012"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">Jatin Kumar Singh · Information Security Analyst</title>
<desc id="desc">The same mechanical suitcase lock as Jatin's portfolio, continuously rolling through Security, Automation, Bug Bounty, Red Teaming, Web and API, Mobile VAPT, Log Analysis, AI Agents, and GRC. Each skill holds for four seconds. Reduced-motion preferences display Security without movement.</desc>
<style>text{{font-family:Arial,Helvetica,sans-serif}}\n{css}</style>
<defs>
<linearGradient id="stage" x1="0" y1="0" x2=".9" y2="1"><stop stop-color="#f74435"/><stop offset=".48" stop-color="#ed3025"/><stop offset="1" stop-color="#db231a"/></linearGradient>
<linearGradient id="case-cover" x1="0" y1="0" x2=".62" y2="1"><stop stop-color="#3c393e"/><stop offset=".35" stop-color="#151516"/><stop offset=".72" stop-color="#252528"/><stop offset="1" stop-color="#0b0b0c"/></linearGradient>
<linearGradient id="metal" x1="0" y1="0" x2=".25" y2="1"><stop stop-color="#858186"/><stop offset=".18" stop-color="#4e4b50"/><stop offset=".51" stop-color="#141416"/><stop offset="1" stop-color="#4e4c52"/></linearGradient>
<linearGradient id="reel-shade" x1="0" y1="0" x2="0" y2="1"><stop stop-color="#000000" stop-opacity=".62"/><stop offset=".35" stop-color="#000000" stop-opacity="0"/><stop offset=".57" stop-color="#000000" stop-opacity="0"/><stop offset="1" stop-color="#000000" stop-opacity=".56"/></linearGradient>
<radialGradient id="ground-shadow"><stop stop-color="#3a0603" stop-opacity=".7"/><stop offset=".6" stop-color="#3a0603" stop-opacity=".34"/><stop offset="1" stop-color="#3a0603" stop-opacity="0"/></radialGradient>
{slot_def}
</defs>
<rect width="{width}" height="{height}" rx="32" fill="url(#stage)"/>
<g fill="#101012">{name}</g>
{brand_back}{mark}
<ellipse cx="{width/2}" cy="{case_y+case_height+37}" rx="{case_width*.58}" ry="63" fill="url(#ground-shadow)"/>
<g transform="translate({case_x} {case_y})">{case}</g>
</svg>\n'''


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--time',type=float,help='Freeze the live timeline at seconds; default animates')
    parser.add_argument('--mobile',action='store_true')
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    if args.output:
        args.output.write_text(build(args.mobile,args.time))
        print(args.output)
    else:
        (ASSETS/'suitcase-cover.svg').write_text(build(False,args.time))
        (ASSETS/'suitcase-cover-mobile.svg').write_text(build(True,args.time))
        print(f'Generated suitcase covers. {len(WORDS)} skills, {LOOP_SECONDS:g}s seamless loop.')

if __name__ == '__main__':
    main()
