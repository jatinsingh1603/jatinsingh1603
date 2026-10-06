# Profile maintenance

This public repository is named `jatinsingh1603`, so GitHub renders its root
`README.md` on the account profile.

## The case-file design

The README shares the portfolio's red (`#ed3025`), black (`#101012`) and ivory
palette. It uses native Markdown and HTML for readable text, links, tables and
expandable evidence. The cover is a small, self-contained SVG, with a separate
mobile composition selected by a `picture` element.

Regenerate the original cover artwork with Python's standard library:

```sh
python3 render_case_art.py
```

Commit both `profile-assets/case-header.svg` and
`profile-assets/case-header-mobile.svg` with generator changes. A single
six-second trace introduces the evidence folder and workflow; reduced-motion
preferences disable the animation. The complete illustration remains visible
when animation is unavailable. No remote fonts or scripts are needed.

GitHub controls the surrounding profile layout and typography. Source and image
links are relative to this repository, so the README also previews on a branch.

## Content and evidence

The October 2026 portfolio records in `jatinsingh1603/Portfolio/content` supply
the current career, findings, projects, awards and qualifications. The README
links each research entry to its public portfolio record.

- Two awards total $2,000: Blinkit $1,500 and Kraken $500.
- Reports and acknowledgements are not described as bounty awards.
- Google's Chrome DevTools MCP fix is described as submitted, not merged or
  released.
- NorthCap findings retain their authorised-testing context.
- Meesho has no stated bounty or vendor acknowledgement.
- The PenTest+ learning path is issued by TryHackMe; it is not described as a
  CompTIA certification.
- swiftPentest is the only featured project and Jatin's role is Contributor.

Review these sources before changing claims. Keep confidential reproduction
details out of this public profile. Organisation logo provenance is recorded
in `profile-assets/SOURCES.md`; preserve the supplied marks and their colours.

## Retired activity display

The contribution calendar, streak statistics and monthly contribution charts
are no longer embedded in the README. GitHub already supplies its native
contribution calendar below the profile content.

The old `activity.svg`, `stats.svg`, `stack.svg`, `activity.json` and their
Python generators are retained as historical assets. The old refresh workflow
is now manual-only, so it no longer commits unused activity snapshots every
day or on Python changes. Running it manually only updates those historical
cards; it does not rebuild or overwrite the new README or cover artwork.

The original `jatin-ascii.png` and `portrait.svg` are retained intact. The new
README does not repeat the portrait already displayed by GitHub's profile
sidebar.

## Maintenance reference

[GitHub's profile README documentation](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).
