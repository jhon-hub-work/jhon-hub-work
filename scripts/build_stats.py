#!/usr/bin/env python3
"""Render a live Claude Code usage card from local transcripts.

Reads ~/.claude/projects/**/*.jsonl, computes usage stats, and writes
assets/claude-code-stats.svg. With --push, commits and pushes if it changed.
"""
import collections
import datetime
import glob
import io
import json
import os
import subprocess
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(REPO, "assets", "claude-code-stats.svg")
TRANSCRIPTS = os.path.expanduser("~/.claude/projects/*/*.jsonl")
HEATMAP_WEEKS = 17

MODEL_NAMES = {"opus": "Opus", "sonnet": "Sonnet", "haiku": "Haiku", "fable": "Fable"}


def pretty_model(mid):
    """claude-opus-5 -> Opus 5; claude-sonnet-4-6 -> Sonnet 4.6"""
    parts = mid.replace("claude-", "").split("-")
    family = MODEL_NAMES.get(parts[0], parts[0].title())
    ver = ".".join(p for p in parts[1:] if p.isdigit())
    return (family + " " + ver).strip()


def collect():
    sessions = set()
    messages = 0
    tokens = 0
    per_day = collections.Counter()
    per_hour = collections.Counter()
    models = collections.Counter()

    for path in glob.glob(TRANSCRIPTS):
        for line in io.open(path, encoding="utf-8", errors="ignore"):
            if '"timestamp"' not in line:
                continue
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") not in ("user", "assistant"):
                continue
            messages += 1
            if d.get("sessionId"):
                sessions.add(d["sessionId"])
            if d.get("type") == "assistant":
                m = d.get("message") or {}
                if m.get("model"):
                    models[m["model"]] += 1
                u = m.get("usage") or {}
                tokens += (u.get("input_tokens") or 0) + (u.get("output_tokens") or 0)
            ts = d.get("timestamp")
            if ts:
                dt = datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
                per_day[dt.date()] += 1
                per_hour[dt.hour] += 1

    return sessions, messages, tokens, per_day, per_hour, models


def streaks(days):
    """Longest run of consecutive active days, and the run ending today/yesterday."""
    if not days:
        return 0, 0
    ordered = sorted(days)
    longest = run = 1
    for prev, cur in zip(ordered, ordered[1:]):
        run = run + 1 if (cur - prev).days == 1 else 1
        longest = max(longest, run)

    today = datetime.date.today()
    current = 0
    if ordered[-1] >= today - datetime.timedelta(days=1):
        d = ordered[-1]
        active = set(days)
        while d in active:
            current += 1
            d -= datetime.timedelta(days=1)
    return current, longest


def human_tokens(n):
    if n >= 1000000000:
        return "%.1fB" % (n / 1e9)
    if n >= 1000000:
        return "%.1fM" % (n / 1e6)
    if n >= 1000:
        return "%.1fK" % (n / 1e3)
    return str(n)


def hour_label(h):
    return "%d %s" % (h % 12 or 12, "AM" if h < 12 else "PM")


def heatmap_cells(per_day, x0, y0, cell=13, gap=3):
    """GitHub-style grid: columns are weeks, rows are Mon..Sun."""
    today = datetime.date.today()
    end = today + datetime.timedelta(days=(6 - today.weekday()))
    start = end - datetime.timedelta(weeks=HEATMAP_WEEKS - 1, days=6)

    counts = [per_day.get(start + datetime.timedelta(days=i), 0)
              for i in range((end - start).days + 1)]
    busiest = max(counts) or 1
    shades = ["#1c2128", "#0e4429", "#006d32", "#26a641", "#39d353"]

    out = []
    for i, n in enumerate(counts):
        day = start + datetime.timedelta(days=i)
        if day > today:
            break
        level = 0 if n == 0 else min(4, 1 + int(3 * n / busiest))
        x = x0 + (i // 7) * (cell + gap)
        y = y0 + (i % 7) * (cell + gap)
        out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s">'
                   '<title>%s &#8212; %d messages</title></rect>'
                   % (x, y, cell, cell, shades[level], day.isoformat(), n))
    return "\n    ".join(out)


def tile(x, y, label, value):
    return ('<rect class="tile" x="%.1f" y="%.1f" width="196" height="76" rx="8"/>\n'
            '    <text class="lbl" x="%d" y="%d">%s</text>\n'
            '    <text class="val" x="%d" y="%d">%s</text>'
            % (x + 0.5, y + 0.5, x + 18, y + 26, label, x + 18, y + 58, value))


TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="880" height="382" viewBox="0 0 880 382" role="img" aria-label="Claude Code usage: {sessions} sessions, {messages} messages, {tokens} tokens, {days} active days, {cur} day current streak, top model {model}">
  <style>
    .bg   {{ fill:#161b22; stroke:#30363d; stroke-width:1; }}
    .tile {{ fill:#1c2128; stroke:#30363d; stroke-width:1; }}
    .lbl  {{ font:500 13px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; fill:#8b949e; }}
    .val  {{ font:700 24px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; fill:#e6edf3; }}
    .ttl  {{ font:600 15px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; fill:#e6edf3; }}
    .sub  {{ font:400 12px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; fill:#6e7681; }}
    .pill {{ fill:#1f6feb; }}
    .pillt{{ font:600 12px -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif; fill:#ffffff; }}
  </style>

  <rect class="bg" x="0.5" y="0.5" width="879" height="381" rx="12"/>

  <text class="ttl" x="24" y="38">Claude Code &#183; lifetime usage</text>
  <rect class="pill" x="778" y="22" width="78" height="22" rx="11"/>
  <text class="pillt" x="817" y="37" text-anchor="middle">All time</text>

  <g>
    {tiles}
  </g>

  <g>
    {heat}
  </g>

  <text class="sub" x="24" y="366">Last {weeks} weeks of activity &#183; regenerated from local transcripts &#183; updated {updated}</text>
</svg>
'''


def render():
    sessions, messages, tokens, per_day, per_hour, models = collect()
    current, longest = streaks(set(per_day))
    top_model = pretty_model(models.most_common(1)[0][0]) if models else "-"
    peak = hour_label(per_hour.most_common(1)[0][0]) if per_hour else "-"

    tiles = "\n    ".join([
        tile(24, 62, "Sessions", "{:,}".format(len(sessions))),
        tile(236, 62, "Messages", "{:,}".format(messages)),
        tile(448, 62, "Tokens (in + out)", human_tokens(tokens)),
        tile(660, 62, "Active days", str(len(per_day))),
        tile(24, 154, "Current streak", "%dd" % current),
        tile(236, 154, "Longest streak", "%dd" % longest),
        tile(448, 154, "Peak hour", peak),
        tile(660, 154, "Top model", top_model),
    ])

    svg = TEMPLATE.format(
        sessions=len(sessions), messages=messages, tokens=human_tokens(tokens),
        days=len(per_day), cur=current, model=top_model, tiles=tiles,
        heat=heatmap_cells(per_day, 24, 250), weeks=HEATMAP_WEEKS,
        updated=datetime.datetime.now().strftime("%d %b %Y, %H:%M"))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(svg)
    return len(sessions), messages, tokens, len(per_day), current, top_model


def git(*args):
    return subprocess.run(("git",) + args, cwd=REPO, capture_output=True, text=True)


def push():
    if git("diff", "--quiet", "--", OUT).returncode == 0:
        return "no change"
    git("add", "--", OUT)
    r = git("-c", "user.name=Jhon Mycho Buerano",
            "-c", "user.email=bueranojhon@gmail.com",
            "commit", "-m", "chore: refresh Claude Code usage card")
    if r.returncode:
        return "commit failed: " + (r.stderr or r.stdout).strip()
    r = git("push", "origin", "HEAD")
    return "pushed" if r.returncode == 0 else "push failed: " + r.stderr.strip()


if __name__ == "__main__":
    print("sessions=%d messages=%d tokens=%d days=%d streak=%d model=%s" % render())
    if "--push" in sys.argv:
        print(push())
