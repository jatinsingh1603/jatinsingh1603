# Profile maintenance

## Display this README on the profile

GitHub displays the root README of a public repository whose name exactly matches the owner's username.
For this account, that repository name is `jatinsingh1603`.

If this repository is still named `Readme`, rename it to `jatinsingh1603` under **Settings → General → Repository name**.
Keep its visibility public. The images use relative paths and will continue working after the rename.

## Refreshing activity

The **Refresh profile cards** workflow runs daily at 02:17 UTC (07:47 India time).
Run it manually from the Actions tab when needed. GitHub can delay scheduled runs and can disable scheduled workflows after 60 days without repository activity.

To run locally with Python 3.12:

```sh
python update_profile.py
```

No personal access token, Python package installation, paid widget or external statistics service is required.
The workflow uses its built-in repository token only to commit the updated cards.

The updater reads the public GitHub contribution calendar and public user endpoint.
Counts represent GitHub contribution events, not lines of code, coding hours or independently verified project outcomes.
The longest streak, best day, total and monthly bars cover only the date range saved in `activity.json`.
Average per active day excludes zero-contribution days.
The current streak includes yesterday when today has no contributions yet; the calculation uses UTC.

The initial and final calendar months can be partial months.
The JSON snapshot includes fetch time and every date/count pair for inspection.
Malformed, stale or incomplete responses fail before replacing the saved cards.
The displayed numbers remain authentic; the design does not add decorative contributions.

## Editing the appearance

Edit `render_profile.py`, then run:

```sh
python render_profile.py
```

This regenerates `activity.svg`, `stats.svg` and `stack.svg` from the saved data snapshot.
Commit changes to the script and assets together. Edit `README.md` for the terminal prompts, links and projects.
The daily workflow only refreshes the two activity cards and their data snapshot.

## Maintaining the portrait

`jatin-ascii.png` is the approved AI-generated grayscale ASCII-style portrait based on Jatin's GitHub profile photograph.
The PNG is stored intact. It is a raster illustration with a character-art appearance, not live ASCII text.

`render_portrait.py` embeds that PNG inside a self-contained `portrait.svg`.
The SVG adds a dark terminal frame, three small status dots, a caption and a six-second repeating reveal.
It does not alter the source image or fetch external content.

To change the frame, caption or timing, edit that script and run:

```sh
python render_portrait.py
```

To use a different portrait, replace `jatin-ascii.png`, rerun the script and commit both files.
The portrait is independent of the daily activity refresh.
Reduced-motion preferences disable the reveal and display the complete portrait.
SVG viewers without animation support also show the complete portrait.

## Design reference

The terminal layout takes visual inspiration from [AVIVASHISHTA29's profile](https://github.com/AVIVASHISHTA29/AVIVASHISHTA29).
The implementation is original. The portrait, links, projects and activity data belong to Jatin's version.
All graphics include accessible descriptions. The statistics and badges use system monospace fonts.
GitHub's image cache can take time to display a fresh version.

GitHub reference: [Managing your profile README](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme).
