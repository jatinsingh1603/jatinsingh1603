#!/usr/bin/env python3
"""Generate quiet navigation artwork with authentic, self-contained branding."""
from copy import deepcopy
from html import escape
from pathlib import Path
import xml.etree.ElementTree as ET

OUT = Path(__file__).resolve().parent / 'profile-assets'
SVG = 'http://www.w3.org/2000/svg'
ET.register_namespace('', SVG)
ET.register_namespace('xlink', 'http://www.w3.org/1999/xlink')

# Exact geometry and colours from portfolio/components/brand-mark.tsx.
PORTFOLIO_MARK = '''<svg x="25" y="22" width="52" height="52" viewBox="0 0 64 64" fill="none">
<rect width="64" height="64" rx="14" fill="#ed3025"/>
<path d="M49 29A20 20 0 1 0 29 49V42A13 13 0 1 1 42 29H49Z" fill="#101012"/>
<path d="M53 34H46A12 12 0 0 1 34 46V53A19 19 0 0 0 53 34Z" fill="#101012"/>
<path d="M29 22a5 5 0 0 0-2.25 9.47L25 38h8l-1.75-6.53A5 5 0 0 0 29 22Z" fill="#101012"/>
</svg>'''
UI_ICONS = {
    'resume': '<path d="M17 8h22l11 11v37H17z"/><path d="M39 8v12h11M25 31h17M25 40h17M25 49h10"/>',
    'contact': '<rect x="7" y="14" width="50" height="36" rx="5"/><path d="m9 18 23 18 23-18"/>',
}
LABELS = {'portfolio': 'Portfolio', 'resume': 'Résumé', 'linkedin': 'LinkedIn', 'contact': 'Contact'}

def linkedin_mark() -> str:
    # Exact PNG bytes supplied by LinkedIn, embedded rather than traced.
    nested = deepcopy(ET.parse(OUT / 'linkedin-official.svg').getroot())
    nested.attrib.update({'x': '28', 'y': '26.75', 'width': '50', 'height': '42.5', 'preserveAspectRatio': 'xMidYMid meet'})
    return '<rect x="19" y="16" width="68" height="64" rx="12" fill="#f7f5f1"/>' + ET.tostring(nested, encoding='unicode')

def validate(svg: str) -> None:
    root = ET.fromstring(svg)
    if root.attrib.get('viewBox') != '0 0 400 96':
        raise ValueError('Unexpected navigation dimensions')
    for node in root.iter():
        if node.tag.rsplit('}', 1)[-1] in {'script', 'foreignObject'}:
            raise ValueError('Unsafe SVG node')
        for key, value in node.attrib.items():
            local = key.rsplit('}', 1)[-1].lower()
            if local.startswith('on'):
                raise ValueError('SVG event handler')
            if local in {'href', 'src'} and not value.startswith('data:image/png;base64,'):
                raise ValueError('External SVG resource')

def main() -> None:
    for name, label in LABELS.items():
        if name == 'portfolio':
            icon = PORTFOLIO_MARK
        elif name == 'linkedin':
            icon = linkedin_mark()
        else:
            icon = f'<g transform="translate(25 22) scale(.8125)" stroke="#f7f5f1" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" fill="none">{UI_ICONS[name]}</g>'
        svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="400" height="96" viewBox="0 0 400 96" role="img" aria-labelledby="title">
<title id="title">Open {escape(label)}</title>
<rect x=".75" y=".75" width="398.5" height="94.5" rx="16" fill="#141416" stroke="#443b3c" stroke-width="1.5"/>
{icon}
<text x="112" y="59" fill="#f7f5f1" font-family="Arial,Helvetica,sans-serif" font-size="32" font-weight="500">{escape(label)}</text>
</svg>'''
        validate(svg)
        (OUT / f'link-{name}.svg').write_text(svg + '\n')
        print(f'link-{name}.svg: 400 x 96, validated')

if __name__ == '__main__':
    main()
