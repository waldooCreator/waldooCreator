"""Pixel-art GitHub stats panel, refreshed by a scheduled GitHub Action.

usage: GITHUB_TOKEN=... stats.py FONT.ttf OUT.svg LOGIN
Reads public data only: contributions this year, public repos, stars, and the
languages of the user's own public, non-fork repos.
"""
import json
import os
import sys
import urllib.request

from pixel import esc, path, rect, text_pixels

FONT, OUT, LOGIN = sys.argv[1], sys.argv[2], sys.argv[3]
PX, GW, GH = 2, 300, 110

QUERY = '''query($login: String!) {
  user(login: $login) {
    contributionsCollection { contributionCalendar { totalContributions } totalCommitContributions }
    repositories(ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false, first: 100) {
      totalCount
      nodes { stargazerCount isArchived languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
  }
}'''


def fetch():
    req = urllib.request.Request(
        'https://api.github.com/graphql',
        data=json.dumps({'query': QUERY, 'variables': {'login': LOGIN}}).encode(),
        headers={'Authorization': f'bearer {os.environ["GITHUB_TOKEN"]}', 'Content-Type': 'application/json'},
    )
    with urllib.request.urlopen(req, timeout=30) as res:
        body = json.load(res)
    if 'errors' in body:
        raise SystemExit(f'GraphQL errors: {body["errors"]}')
    return body['data']['user']


user = fetch()
repos = user['repositories']['nodes']
stars = sum(r['stargazerCount'] for r in repos)
contrib = user['contributionsCollection']['contributionCalendar']['totalContributions']
langs = {}
colors = {}
for r in repos:
    for e in r['languages']['edges']:
        n = e['node']['name']
        langs[n] = langs.get(n, 0) + e['size']
        colors[n] = e['node']['color'] or '#8b949e'
total = sum(langs.values()) or 1
top = sorted(langs.items(), key=lambda kv: -kv[1])[:6]

parts = [rect(0, 0, GW, GH, '#10132a', PX), rect(1, 1, GW - 2, GH - 2, '#151a3a', PX)]
border = [(x, 0) for x in range(2, GW - 2)] + [(x, GH - 1) for x in range(2, GW - 2)] + \
         [(0, y) for y in range(2, GH - 2)] + [(GW - 1, y) for y in range(2, GH - 2)] + [(1, 1), (GW - 2, 1), (1, GH - 2), (GW - 2, GH - 2)]
parts.append(path(border, '#5b4a7a', PX))

# left: three counters
commits = user['contributionsCollection']['totalCommitContributions']
stats = [('CONTRIBUTIONS', contrib, '#7cfc9a'), ('COMMITS', commits, '#e0af68'), ('PUBLIC REPOS', user['repositories']['totalCount'], '#7dcfff')]
for i, (label, value, color) in enumerate(stats):
    y = 12 + i * 32
    vp, _ = text_pixels(FONT, str(value), 2)
    parts.append(path(vp, color, PX, 12, y))
    lp, _ = text_pixels(FONT, label, 1)
    parts.append(path(lp, '#8f8aa8', PX, 12, y + 19))

# right: languages as a pixel bar plus a legend
x0, y0, bw = 128, 14, 160
title, _ = text_pixels(FONT, 'TOP LANGUAGES', 1)
parts.append(path(title, '#c0caf5', PX, x0, y0))
x = x0
for i, (name, size) in enumerate(top):
    w = max(2, round(bw * size / total)) if i < len(top) - 1 else max(2, x0 + bw - x)
    parts.append(rect(x, y0 + 14, w, 6, colors[name], PX))
    x += w
for i, (name, size) in enumerate(top):
    cx, cy = x0 + (i % 2) * 82, y0 + 30 + (i // 2) * 16
    parts.append(rect(cx, cy, 6, 6, colors[name], PX))
    parts.append(f'<text x="{(cx + 10) * PX}" y="{(cy + 6) * PX}" fill="#c0caf5" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="{7 * PX}">'
                 f'{esc(name)} <tspan fill="#8f8aa8">{100 * size / total:.1f}%</tspan></text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW * PX} {GH * PX}" width="{GW * PX}" height="{GH * PX}" '
       f'shape-rendering="crispEdges" role="img" aria-label="GitHub stats for {esc(LOGIN)}"><title>GitHub stats</title>{"".join(parts)}</svg>')
open(OUT, 'w').write(svg)
print(OUT, f'{contrib} contributions, {stars} stars, {commits} commits, top: {[n for n, _ in top]}')
