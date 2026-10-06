#!/usr/bin/env python3
"""Build accessible, self-contained navigation artwork for the visual profile."""
from pathlib import Path
from html import escape

OUT = Path(__file__).resolve().parent / 'profile-assets'
ICONS = {
    'portfolio': '<path d="M10 25h20l8 10h39v43H10z"/><path d="M10 43h67"/><circle cx="46" cy="59" r="9"/><path d="m53 66 10 10"/>',
    'resume': '<path d="M22 12h33l15 15v59H22z"/><path d="M55 12v16h15M34 43h24M34 56h24M34 69h15"/>',
    'linkedin': '<circle cx="23" cy="26" r="5"/><path d="M23 42v35M41 77V43m0 13c0-19 28-20 28 0v21"/>',
    'contact': '<rect x="9" y="26" width="69" height="48" rx="7"/><path d="m12 30 32 25 31-25"/>',
}
LABELS = {'portfolio': 'PORTFOLIO', 'resume': 'RÉSUMÉ', 'linkedin': 'LINKEDIN', 'contact': 'CONTACT'}
for name, icon in ICONS.items():
    label = LABELS[name]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="112" viewBox="0 0 400 112" role="img" aria-labelledby="title"><title id="title">Open {escape(label.lower())}</title>
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#29292c"/><stop offset="1" stop-color="#101012"/></linearGradient></defs>
<rect x="1" y="1" width="398" height="110" rx="22" fill="url(#bg)" stroke="#49494d" stroke-width="2"/>
<rect x="17" y="17" width="78" height="78" rx="19" fill="#ed3025"/>
<g transform="translate(23 15) scale(.75)" stroke="#f7f5f1" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" fill="none">{icon}</g>
<text x="116" y="69" fill="#f7f5f1" font-family="Arial,Helvetica,sans-serif" font-size="35" font-weight="700">{label}</text></svg>'''
    (OUT / f'link-{name}.svg').write_text(svg)
print('Generated four navigation graphics')
