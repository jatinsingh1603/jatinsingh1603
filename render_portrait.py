#!/usr/bin/env python3
"""Wrap the approved portrait PNG in a self-contained animated profile SVG.

The source PNG stays unchanged. This script only builds an SVG frame around it.
"""
from base64 import b64encode
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def render_portrait(source: Path, destination: Path) -> None:
    encoded = b64encode(source.read_bytes()).decode('ascii')
    content = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="420" height="440" viewBox="0 0 420 440" role="img" aria-labelledby="portrait-title portrait-desc">
<title id="portrait-title">Jatin Kumar Singh — terminal portrait</title>
<desc id="portrait-desc">A grayscale ASCII-style portrait of Jatin, based on his profile photograph. A gentle vertical reveal repeats every six seconds. Reduced-motion settings show the complete still portrait.</desc>
<style>
.portrait {{ clip-path: inset(0); animation: terminal-reveal 6s ease-in-out infinite; }}
@keyframes terminal-reveal {{
  0% {{ clip-path: inset(0 0 97% 0); }}
  28%, 88% {{ clip-path: inset(0); }}
  100% {{ clip-path: inset(0 0 97% 0); }}
}}
@media (prefers-reduced-motion: reduce) {{
  .portrait {{ animation: none !important; clip-path: none !important; }}
}}
</style>
<rect x=".5" y=".5" width="419" height="439" rx="3" fill="#0d1117" stroke="#202832"/>
<circle cx="17" cy="15" r="2.5" fill="#f85149"/>
<circle cx="28" cy="15" r="2.5" fill="#d29922"/>
<circle cx="39" cy="15" r="2.5" fill="#26a641"/>
<g class="portrait">
  <image x="20" y="34" width="380" height="380" preserveAspectRatio="xMidYMid meet" xlink:href="data:image/png;base64,{encoded}"/>
</g>
<text x="17" y="431" font-family="'DejaVu Sans Mono', 'SFMono-Regular', Consolas, monospace" font-size="8" fill="#8b949e" letter-spacing=".45">JATIN KUMAR SINGH / CYBERSECURITY</text>
</svg>
'''
    destination.write_text(content, encoding='utf-8')


if __name__ == '__main__':
    render_portrait(ROOT / 'jatin-ascii.png', ROOT / 'portrait.svg')
