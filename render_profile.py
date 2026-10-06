"""Render a terminal-style profile using real public GitHub calendar data."""
from datetime import date, timedelta
from html import escape
from pathlib import Path
import json

BG = '#0d1117'
PANEL = '#10151b'
LINE = '#202832'
TEXT = '#e6edf3'
MUTED = '#8b949e'
GREEN = '#26a641'
PALETTE = ['#161b22', '#0e4429', '#006d32', '#26a641', '#39d353']


def text(x, y, value, size=14, color=TEXT, extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" {extra}>{escape(str(value))}</text>'


def rect(x, y, w, h, color, radius=0, extra=''):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{color}" {extra}/>'


def svg(width, height, title, content, desc=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
<title id="title">{escape(title)}</title><desc id="desc">{escape(desc or title)}</desc>
<style>
text {{ font-family: 'DejaVu Sans Mono', 'SFMono-Regular', Consolas, monospace; }}
.cell {{ animation: reveal 1.1s ease-out both; }}
@keyframes reveal {{ from {{ opacity: .18; }} to {{ opacity: 1; }} }}
@media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important; }} }}
</style>
{content}
</svg>\n'''


def make_activity(data):
    days = data['days']
    first = date.fromisoformat(days[0]['date'])
    origin = first - timedelta(days=(first.weekday() + 1) % 7)
    cols = ((date.fromisoformat(days[-1]['date']) - origin).days // 7) + 1
    pitch = min(15, 810 / cols)
    size = pitch - 2.5
    s = rect(0, 0, 860, 168, BG)
    month = None
    for day in days:
        dt = date.fromisoformat(day['date'])
        col = (dt - origin).days // 7
        row = (dt.weekday() + 1) % 7
        if dt.strftime('%Y-%m') != month and (dt.day == 1 or month is None):
            if col < cols - 1:
                s += text(round(43 + col * pitch, 2), 15, dt.strftime('%b'), 10, MUTED)
            month = dt.strftime('%Y-%m')
        color = PALETTE[int(day['level'])]
        s += f'<rect x="{43 + col * pitch:.2f}" y="{28 + row * 15}" width="{size:.2f}" height="12.5" rx="1.4" fill="{color}" class="cell" style="animation-delay:{col * .012:.3f}s"><title>{escape(day["date"])}: {int(day["count"])} contributions</title></rect>'
    for row, label in [(1, 'Mon'), (3, 'Wed'), (5, 'Fri')]:
        s += text(3, 38 + row * 15, label, 10, MUTED)
    s += text(43, 155, f'{data["total"]:,} contributions in the last year', 12, TEXT)
    s += text(691, 155, 'Less', 10, MUTED)
    for i, color in enumerate(PALETTE):
        s += rect(724 + i * 16, 145, 12, 12, color, 1.4)
    s += text(809, 155, 'More', 10, MUTED)
    return svg(860, 168, 'GitHub contribution calendar', s,
               f'{data["total"]} contributions from {data["range_start"]} to {data["range_end"]}. Real public profile calendar data.')


def make_stats(data):
    s = rect(.5, .5, 419, 439, BG, 3, f'stroke="{LINE}"')
    metrics = [
        ('current streak', str(data['current_streak']), 'days'),
        ('longest streak', str(data['longest_streak']), 'days · rolling year'),
        ('contributions', f'{data["total"]:,}', 'rolling year'),
        ('active days', str(data['active_days']), 'rolling year'),
        ('best day', f'{data["best_day"]:,}', 'contributions'),
        ('daily average', f'{data["average_active_day"]:.1f}', 'per active day'),
    ]
    for i, (label, value, unit) in enumerate(metrics):
        x = 17 + (i % 2) * 198
        y = 18 + (i // 2) * 85
        s += rect(x, y, 187, 76, PANEL, 2, f'stroke="{LINE}" stroke-width=".7"')
        s += text(x + 12, y + 18, label, 10, MUTED)
        s += text(x + 12, y + 46, value, 27, GREEN if i == 0 else TEXT, 'font-weight="700"')
        s += text(x + 12, y + 65, unit, 9, MUTED)
    s += text(19, 287, 'CONTRIBUTIONS / MONTH', 9, MUTED, 'letter-spacing="1.1"')
    months = data['months']
    peak = max((month['count'] for month in months), default=1) or 1
    pitch = 382 / len(months)
    for i, month in enumerate(months):
        height = month['count'] / peak * 94
        x = 19 + i * pitch
        width = max(6, pitch - 9)
        if month['count']:
            s += f'<rect x="{x:.2f}" y="{394 - height:.2f}" width="{width:.2f}" height="{height:.2f}" rx=".8" fill="{GREEN}" class="cell" style="animation-delay:{i * .06:.2f}s"><title>{escape(month["month"])}: {month["count"]} contributions</title></rect>'
        else:
            s += rect(round(x, 2), 392.5, round(width, 2), 1.5, LINE)
        label = date.fromisoformat(month['month'] + '-01').strftime('%b')[0]
        s += text(round(x + width / 2, 2), 410, label, 9, MUTED, 'text-anchor="middle"')
    s += text(19, 431, 'Updated ' + data['fetched_at'][:10] + ' UTC', 8, MUTED)
    return svg(420, 440, 'Daily GitHub activity statistics for Jatin', s,
               f'Current streak {data["current_streak"]} days. Longest streak {data["longest_streak"]} days in the displayed calendar window. {data["total"]} contributions over {data["active_days"]} active days. Best day {data["best_day"]} contributions. Average {data["average_active_day"]:.1f} per active day. Real public data from {data["range_start"]} to {data["range_end"]}.')


def make_stack():
    s = rect(0, 0, 860, 69, BG)
    rows = [
        [('VAPT', '#41464e'), ('WEB & API SECURITY', '#365667'),
         ('SOURCE CODE REVIEW', '#4e4266'), ('AI AUTOMATION', '#32635d')],
        [('PYTHON', '#725f34'), ('n8n', '#74404c'), ('AI WORKFLOWS', '#41516c'),
         ('LINUX', '#57524b'), ('GIT', '#754936'), ('JAVA', '#495d75'), ('SQL', '#3b6067')],
    ]
    for row, pills in enumerate(rows):
        widths = [round(len(label) * 6.4 + 25) for label, _ in pills]
        x = (860 - sum(widths) - (len(pills) - 1) * 7) / 2
        y = 4 + row * 30
        for (label, color), width in zip(pills, widths):
            s += rect(round(x, 2), y, width, 23, color, 2)
            s += text(round(x + width / 2, 2), y + 15.5, label, 10, TEXT,
                      'text-anchor="middle" font-weight="700"')
            x += width + 7
    return svg(860, 69, 'Security and automation toolkit', s,
               'VAPT, web and API security, source code review, AI automation, Python, n8n, AI workflows, Linux, Git, Java and SQL.')


def render(data, output_dir):
    """Keep the daily workflow contract: regenerate only data-driven cards."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    for name, value in [('activity.svg', make_activity(data)), ('stats.svg', make_stats(data))]:
        (output_dir / name).write_text(value, encoding='utf-8')


if __name__ == '__main__':
    root = Path(__file__).resolve().parent
    render(json.loads((root / 'activity.json').read_text()), root)
    (root / 'stack.svg').write_text(make_stack(), encoding='utf-8')
