#!/usr/bin/env python3
"""Build original, self-contained security and automation artwork for GitHub."""

from __future__ import annotations

import math
from pathlib import Path
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET


ASSETS = Path(__file__).resolve().parent / "profile-assets"
INK, RED, PAPER, MUTED = "#101012", "#ed3025", "#f7f5f1", "#bab6b2"


def rect(x, y, w, h, fill, radius=20, stroke="none", sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'


def text(x, y, label, size=28, fill=PAPER, weight=600, anchor="start"):
    return f'<text x="{x}" y="{y}" font-family="Arial, Helvetica, sans-serif" font-size="{size}" fill="{fill}" font-weight="{weight}" text-anchor="{anchor}">{escape(label)}</text>'


def line(d, color="#63504d", width=3, dash=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"' + (f' stroke-dasharray="{dash}"' if dash else "") + '/>'


def dot(x, y, r=5, fill=RED):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}"/>'


def defs():
    return """<defs>
      <radialGradient id="glow"><stop stop-color="#ed3025" stop-opacity=".07"/><stop offset="1" stop-color="#ed3025" stop-opacity="0"/></radialGradient>
    </defs>
    <style>
      /* The base illustration is complete. Only these decorative overlays move. */
      .flow-pulse { opacity: 0; stroke-dasharray: 9 191; stroke-dashoffset: 12;
        animation: data-flow 8s linear infinite; }
      .gate-confirm { opacity: 0; animation: gate-check 8s ease-in-out infinite; }
      @keyframes data-flow {
        0% { opacity: 0; stroke-dashoffset: 12; }
        2% { opacity: .62; stroke-dashoffset: 2; }
        14% { opacity: .62; stroke-dashoffset: -90; }
        16%, 100% { opacity: 0; stroke-dashoffset: -104; }
      }
      @keyframes gate-check {
        0%, 2% { opacity: 0; }
        6% { opacity: .65; }
        13%, 100% { opacity: 0; }
      }
      @media (prefers-reduced-motion: reduce) {
        .flow-pulse, .gate-confirm { animation: none !important; opacity: 0 !important; }
      }
    </style>"""


def flow(d, stage, delay=0, color="#6b6262", width=3):
    """Retain a static wire and animate one low-contrast packet over its path."""
    return line(d, color, width) + (
        f'<path class="flow-pulse" data-flow-stage="{stage}" d="{d}" '
        f'pathLength="100" fill="none" stroke="{PAPER}" stroke-width="{width + 1}" '
        f'stroke-linecap="round" stroke-linejoin="round" opacity="0" '
        f'style="animation-delay:{delay:g}s"/>'
    )


def shell(width, height, title):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="art-title art-description">',
            f'<title id="art-title">{escape(title)}</title>',
            '<desc id="art-description">Jatin contributes to swiftPentest: 12+ agents and 99 tools, control and test comparisons, a minimum 3/5 reproduction gate, and SARIF evidence output. The lower illustration shows an n8n due diligence, scoring and approval workflow.</desc>',
            defs(), rect(0, 0, width, height, INK, 32),
            rect(1, 1, width-2, height-2, "none", 32, "#353538", 2)]


def core(cx, cy, radius=175, mobile=False):
    result = [f'<circle cx="{cx}" cy="{cy}" r="{radius+75}" fill="url(#glow)"/>']
    result += [f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#514448" stroke-width="2"/>',
               f'<circle cx="{cx}" cy="{cy}" r="{radius-18}" fill="none" stroke="#333136" stroke-width="1" stroke-dasharray="3 12"/>']
    for index in range(12):
        angle = math.radians(index*30-90)
        x, y = cx+math.cos(angle)*radius, cy+math.sin(angle)*radius
        ex, ey = cx+math.cos(angle)*115, cy+math.sin(angle)*115
        result += [line(f"M{ex:.2f} {ey:.2f}L{x:.2f} {y:.2f}", "#534346", 2),
                   rect(round(x-18,2), round(y-18,2), 36, 36, "#1b1b1f", 10, "#706265", 1.5)]
        # Twelve individual agent modules, each with an internal chip mark.
        result += [rect(round(x-6,2), round(y-6,2), 12, 12, RED if index%3 else PAPER, 3)]
    face_radius=129 if mobile else 119
    result += [dot(cx,cy,face_radius+7,"#08080a"),
               f'<circle cx="{cx}" cy="{cy}" r="{face_radius}" fill="#1b1b1f" stroke="#ed3025" stroke-width="3"/>',
               f'<circle cx="{cx}" cy="{cy}" r="{face_radius-12}" fill="none" stroke="#665050" stroke-width="1"/>',
               line(f"M{cx-27} {cy-65}h54M{cx-38} {cy-53}h76", RED, 4),
               text(cx, cy+4, "swiftPentest", 36 if mobile else 35, PAPER, 700, "middle"),
               text(cx, cy+46, "CONTRIBUTOR", 32 if mobile else 28, MUTED, 500, "middle"),
               dot(cx-18,cy+79,4,RED),dot(cx,cy+79,4,RED),dot(cx+18,cy+79,4,PAPER)]
    return ''.join(result)


def input_panel(x, y, w, h, label, mobile=False):
    return ''.join([rect(x+2,y+4,w,h,"#0b0b0d",18),rect(x,y,w,h,"#1b1b1f",18,"#51484d",1.5),
                    rect(x+16,y+16,7,h-32,RED,3),text(x+38,y+44,label,32 if mobile else 28),
                    line(f"M{x+38} {y+h-23}h{w-64}","#6e6262",3),dot(x+w-24,y+24,4,PAPER)])


def tools(x, y, w, h, mobile=False):
    result=[rect(x+2,y+4,w,h,"#0b0b0d",18),rect(x,y,w,h,"#1b1b1f",18,"#51484d",1.5),
            text(x+22,y+43,"99 TOOLS",36 if mobile else 32)]
    for row in range(2):
        for column in range(6):
            slotw=(w-56)/6
            sx=x+20+column*(slotw+3)
            sy=y+65+row*27
            result += [rect(sx,sy,slotw,17,"#292325",5,"#564340"),dot(sx+slotw/2,sy+8,2.5,RED if (row+column)%3 else PAPER)]
    result += [line(f"M{x+22} {y+h-19}h{w-44}","#4e4242",2)]
    return ''.join(result)


def evidence(x, y, w, h, mobile=False):
    stamp_y=110 if mobile else 138
    result=[rect(x+14,y+20,w-14,h-20,"#0a080b",18),
            rect(x+4,y+22,w-20,h-32,"#32252a",15,"#6f433f",2),
            rect(x+19,y+7,w-40,h-36,"#bdb4aa",12),
            rect(x+9,y,w-40,h-36,PAPER,12),
            text(x+30,y+54,"SARIF",38 if mobile else 32,INK),
            line(f"M{x+31} {y+78}h{w-107}M{x+31} {y+96}h{w-89}" + ("" if mobile else f"M{x+31} {y+114}h{w-120}"),"#a39a95",4),
            rect(x+30,y+stamp_y,w-64,38,"none",7,RED,2),
            text(x+42,y+stamp_y+28,"EVIDENCE",32 if mobile else 28,RED),
            rect(x,y+h-58,w,58,"#272023",13,"#6d4944",2),
            line(f"M{x+21} {y+h-42}h{w-42}","#a95047",2),
            dot(x+26,y+h-20,4,RED),dot(x+42,y+h-20,4,PAPER)]
    return ''.join(result)


def gate(x, y, w, h, mobile=False):
    # The threshold is always three filled cells of five. The moving highlights
    # are decorative confirmation cues; they never change the threshold.
    result=[rect(x,y,w,h,"#19181c",18,RED,2),
            text(x+w/2,y+43,"3/5 REPRODUCTION GATE",32 if mobile else 28,PAPER,600,"middle")]
    cellw=28 if mobile else 24
    start=x+w/2-(cellw*5+8*4)/2
    for index in range(5):
        cellx=start+index*(cellw+8)
        result.append(rect(cellx,y+h-20,cellw,6,RED if index<3 else "#4a4144",3))
        if index<3:
            result.append(
                f'<rect class="gate-confirm" data-gate-check="{index+1}" '
                f'x="{cellx}" y="{y+h-21}" width="{cellw}" height="8" '
                f'rx="4" fill="none" stroke="{PAPER}" stroke-width="2" '
                f'opacity="0" style="animation-delay:{3.3+index*.45:.2f}s"/>'
            )
    return ''.join(result)


def workflow(x, y, w, mobile=False):
    h=174 if mobile else 136
    result=[text(x,y-27,"n8n WORKFLOW",32 if mobile else 28,MUTED,500)]
    gap=24 if mobile else 68
    cellw=(w-2*gap)/3
    labels=[("DUE", "DILIGENCE"),("RISK", "SCORING"),("HUMAN", "APPROVAL")]
    for i,(top,bottom) in enumerate(labels):
        sx=x+i*(cellw+gap)
        if i<2:
            result += [flow(f"M{sx+cellw} {y+h/2}H{sx+cellw+gap}", f"workflow-{i+1}", 5.9+i*.7, RED, 3),dot(sx+cellw+gap/2,y+h/2,4,PAPER)]
        result += [rect(sx+2,y+4,cellw,h,"#0b0b0d",18),rect(sx,y,cellw,h,"#1b1b1f",18,"#51484d",1.5)]
        cx=sx+cellw/2
        if i==0:
            result += [rect(cx-15,y+20,30,36,"none",5,RED,3),line(f"M{cx-7} {y+29}h14M{cx-7} {y+38}h14M{cx-7} {y+47}h9",PAPER,2)]
        elif i==1:
            result += [rect(cx-21,y+43,10,15,RED,2),rect(cx-5,y+31,10,27,PAPER,2),rect(cx+11,y+20,10,38,RED,2)]
        else:
            result += [f'<circle cx="{cx}" cy="{y+39}" r="21" fill="none" stroke="{RED}" stroke-width="3"/>',
                       line(f"M{cx-10} {y+39}l7 8 14-16",PAPER,3)]
        result += [text(cx,y+(102 if mobile else 92),top,32 if mobile else 28,PAPER,600,"middle"),
                   text(cx,y+(144 if mobile else 124),bottom,32 if mobile else 28,PAPER,600,"middle")]
    return ''.join(result)


def desktop():
    a=shell(1280,850,"Systems and automation: swiftPentest contribution and n8n workflow")
    a += [text(48,66,"SYSTEMS & AUTOMATION",36,PAPER,600),
          line("M48 97H1232","#353538",2),text(644,125,"12+ AGENTS",30,MUTED,500,"middle")]
    # Inputs enter the core. Its output passes through validation before SARIF.
    a += [flow("M293 240H370Q394 240 394 264V329H524","control",0,RED),
          flow("M293 350H352Q378 350 378 333V329H524","test",.35),
          flow("M295 492H409Q433 492 433 464V329H524","tools",.7),
          flow("M644 454V545","core-to-gate",2,RED),
          flow("M870 583H925Q949 583 949 557V480Q949 460 969 460H986","gate-to-evidence",4.7,RED),
          dot(394,329,4,PAPER),dot(433,329,4,PAPER)]
    a += [input_panel(48,195,245,89,"CONTROL"),input_panel(48,307,245,89,"TEST"),
          tools(48,421,247,143),core(644,329,173),evidence(986,213,244,308),
          gate(418,545,452,76)]
    a += [line("M48 641H1232","#353538",2),workflow(48,691,1184),"</svg>"]
    return ''.join(a)


def mobile():
    a=shell(760,1420,"Systems and automation: swiftPentest contribution and n8n workflow")
    a += [text(40,66,"SYSTEMS &",40,PAPER,600),text(40,119,"AUTOMATION",40,PAPER,600),
          line("M40 148H720","#353538",2),text(380,183,"12+ AGENTS",34,MUTED,500,"middle")]
    a += [flow("M194 608V581Q194 566 212 566H356Q368 566 368 550V503","control",0,RED),
          flow("M566 608V581Q566 566 548 566H404Q392 566 392 550V503","test",.35),
          flow("M195 741V721H352Q364 721 364 703V534Q364 514 368 503","tools",.7),
          flow("M380 503V1008","core-to-gate",2,RED),
          flow("M565 1008V948","gate-to-evidence",4.7,RED)]
    a += [core(380,378,163,True),input_panel(40,607,312,97,"CONTROL",True),
          input_panel(408,607,312,97,"TEST",True),tools(40,741,312,205,True),
          evidence(418,735,290,213,True),gate(40,1008,680,85,True),
          line("M40 1123H720","#353538",2),workflow(40,1200,680,True),"</svg>"]
    return ''.join(a)


def validate(svg: str, minimum_font: int):
    root=ET.fromstring(svg)
    for element in root.iter():
        local=element.tag.rsplit('}',1)[-1]
        if local in {"script","foreignObject","image"}:
            raise ValueError(f"Unsupported node: {local}")
        if "font-size" in element.attrib and int(element.attrib["font-size"])<minimum_font:
            raise ValueError("Text below minimum size")
        for key,value in element.attrib.items():
            if key.lower().startswith("on") or key.rsplit('}',1)[-1] in {"href","src"}:
                raise ValueError("External resource or script handler")
    for label in ["swiftPentest","CONTRIBUTOR","12+ AGENTS","99 TOOLS","3/5 REPRODUCTION GATE"]:
        if label not in svg:raise ValueError(f"Missing essential label: {label}")
    pulses=[node for node in root.iter() if node.attrib.get("class")=="flow-pulse"]
    confirmations=[node for node in root.iter() if node.attrib.get("class")=="gate-confirm"]
    if len(pulses)!=7 or len(confirmations)!=3:
        raise ValueError("Expected seven connected flow pulses and three gate cues")
    if any(node.tag.rsplit("}",1)[-1]!="path" for node in pulses):
        raise ValueError("Flow animation may only decorate connector paths")
    for node in root.iter():
        if node.tag.rsplit("}",1)[-1]=="text" and ("class" in node.attrib or "style" in node.attrib):
            raise ValueError("Meaningful text must remain static")
    if "8s linear infinite" not in svg or "prefers-reduced-motion: reduce" not in svg:
        raise ValueError("Missing running animation or reduced-motion fallback")


def main():
    for filename,svg,minimum in [("system-board.svg",desktop(),28),("system-board-mobile.svg",mobile(),32)]:
        validate(svg,minimum)
        path=ASSETS/filename
        path.write_text(svg+'\n')
        print(f"{filename}: {len(svg):,} bytes, validated")


if __name__=="__main__":
    main()
