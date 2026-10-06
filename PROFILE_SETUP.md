# Visual profile maintenance

The root README renders on the GitHub account profile. It is a graphic-first
casebook: a cinematic cover, illustrated research folders, a security and
automation machine, recognition objects and four graphic navigation buttons.
Only one short instruction is native prose. Every large panel is a link.

## Artwork

The palette matches the portfolio: red `#ed3025`, black `#101012`, ivory
`#f7f5f1`. Self-contained SVG panels have separate mobile compositions selected
below 600px. Alt text conveys the same facts without images. Full factual
records and links live in `CASEBOOK.md`.

Regenerate code-native artwork with Python's standard library:

```sh
python3 render_evidence_art.py
python3 render_system_art.py
python3 render_awards_art.py
python3 render_link_art.py
```

Commit each generator and its corresponding files in `profile-assets` together.
No remote fonts, JavaScript, third-party image widgets or live statistics APIs
are required. Artwork uses complete static frames; motion is optional.

`profile-assets/cinematic-cover.jpg` is project artwork created with the built-in
image generation tool and exported as a 1536 × 1024 progressive JPEG. Generation
brief: a premium cinematic black detective folder with an ivory fingerprint
sheet, red glass magnifier, brushed-metal combination lock, red glass shield
and connected chrome automation nodes, black/red/ivory palette and typography
reading “JATIN KUMAR SINGH / SECURITY / + AUTOMATION”. No portrait, invented
company mark or fake evidence appears in the illustration.

Organisation marks retain their original colours and proportions. Their
provenance is recorded in `profile-assets/SOURCES.md`. The illustrated trophies,
seal and diploma are original visual summaries, not official credential badges.

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

The former cover, portrait, calendar, streak cards, monthly charts and generators
remain as historical source files. None is embedded in the new README. GitHub
already displays the native contribution calendar and sidebar portrait.
The old refresh workflow stays manual-only and cannot overwrite this layout.
