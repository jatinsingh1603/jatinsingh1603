# Visual profile maintenance

The root README renders on the GitHub account profile. Its opening now shares
the portfolio's physical suitcase and rolling combination lock. The native
page's palette, formal Arial typography, rounded case, ivory wheels, fixed
seam and dark wheel shading carry through to the GitHub artwork.

## Artwork and motion

The palette is red `#ed3025`, black `#101012`, ivory `#f7f5f1`. Every large
panel links to details. Full factual records and links live in `CASEBOOK.md`.
The opening and illustrated panels have separate mobile compositions selected
below 600px. Alt text preserves the content when images are unavailable.

Regenerate the code-native artwork:

```sh
python3 render_suitcase_art.py
python3 render_system_art.py
python3 render_link_art.py
python3 render_evidence_art.py
python3 render_awards_art.py
```

The suitcase wheels continuously cycle through Security, Automation, Bug Bounty,
Red Teaming, Web & API, Mobile VAPT, Log Analysis, AI Agents and GRC. The wheels
pause for reading and stagger their smooth transitions. The system illustration
uses a quiet signal travelling through its existing workflow connections.
Numbers and research outcomes remain fixed; motion never simulates live results.

Both animations use self-contained SVG/CSS, with no runtime JavaScript, external
fonts, external image service or recurring workflow. Reduced-motion preferences
stop animation and preserve a complete static composition. Check actual playback
in the GitHub README after changing animation code; a successful image load alone
does not verify animation. The repository's standalone image viewer may differ
from the README renderer.

LinkedIn's navigation mark comes from its official brand download. The CRTP
panel uses the official Altered Security mark in place of the illustrated seal. The portfolio
link reuses the portfolio's original BrandMark geometry. Organisation marks
retain their colours and proportions; provenance lives in
`profile-assets/SOURCES.md`. The illustration generators and their SVG outputs
must be committed together.

## Sound link

The "Enter with sound" artwork beneath the suitcase links to the portfolio
homepage. It is a website link, not an embedded GitHub audio player. The site
uses its existing looping soundtrack and mute control. Browser autoplay rules
may require a tap, and the site respects a previous session mute. Regenerate
the button with `python3 render_link_art.py`.

## Content sources

The October 2026 records in `jatinsingh1603/Portfolio/content` supply the current
career, findings, project, awards and qualifications. Before changing facts,
review those sources and the current résumé.

- Exactly two awarded bounties total $2,000: Blinkit $1,500 and Kraken $500.
- Reports and acknowledgements are not bounty awards.
- Google's Chrome DevTools MCP fix is submitted, not claimed merged or released.
- NorthCap findings retain authorised-testing context.
- Meesho has no stated bounty or vendor acknowledgement.
- The PenTest+ learning path is from TryHackMe, not a CompTIA certification.
- swiftPentest is the only featured project; Jatin's role is Contributor.
- NorthCap graduation is expected in 2027, not completed.

Do not put private endpoints or exploit reproduction details in this public repo.

## Historical assets

The former photographic cover, portrait, calendar, streak cards, monthly charts and generators
remain as historical source files. None is embedded in the new README. GitHub
already displays the native contribution calendar and sidebar portrait.
The old refresh workflow stays manual-only and cannot overwrite this layout.
