"""Pixel-art project cards for the profile README.

usage: gen_cards.py FONT.ttf OUT_DIR
"""
import sys
from pixel import esc, path, rect, text_pixels

FONT, OUT = sys.argv[1], sys.argv[2]
PX = 2
GW, GH = 300, 96

CARDS = [
    {'file': 'menu-flow', 'title': 'MENU FLOW', 'accent': '#e0af68', 'icon': 'food',
     'lines': ['Restaurant POS: QR menu, waiter app,', 'kitchen stations, cash shifts & sales.', '25 specs · 9 ADRs · tested'],
     'tags': ['Django', 'Vue 3', 'PostgreSQL']},
    {'file': 'conciencia', 'title': 'CONCIENCIA', 'accent': '#d4a017', 'icon': 'coin',
     'lines': ['Personal finance without friction:', 'Django REST + PWA, and an offline', 'Android app with SQLite.'],
     'tags': ['React Native', 'Django', 'Docker']},
    {'file': 'clc', 'title': 'CLC', 'accent': '#7cfc9a', 'icon': 'calc',
     'lines': ['Operations Research, step by step:', 'Revised Simplex, duality, assignment', 'and network flows. Arcade UI.'],
     'tags': ['JavaScript', 'Algorithms', 'OR']},
    {'file': 'oficina', 'title': 'OFICINA', 'accent': '#d97757', 'icon': 'office',
     'lines': ['Claude Code mod: your AI subagents', 'working in a pixel-art office,', 'live in the terminal.'],
     'tags': ['TypeScript', 'AI agents', 'Pixel art']},
    {'file': 'san-alejo', 'title': 'SAN ALEJO', 'accent': '#7dcfff', 'icon': 'box',
     'lines': ['Offline mobile inventory for storage', 'containers and their items.', ''],
     'tags': ['React Native', 'Expo', 'SQLite']},
    {'file': 'accesibilidad', 'title': 'A11Y SITE', 'accent': '#bb9af7', 'icon': 'ear',
     'lines': ['Accessible website for visually', 'impaired users: voice narration', 'and listening mode. WCAG 2.2 AA.'],
     'tags': ['JavaScript', 'Web Speech', 'a11y']},
]

ICONS = {
    'food': (['....ss....', '...s..s...', '..........', '.bbbbbbbb.', 'bbBbbBbbBb', 'bbbbbbbbbb', 'gggggggggg', 'rrrrrrrrrr', 'yyyyyyyyyy', '.bbbbbbbb.'],
             {'s': '#d8d4ff', 'b': '#e0a050', 'B': '#fff0c0', 'g': '#5fa35f', 'r': '#c0392b', 'y': '#f1c40f'}),
    'coin': (['...yyyy...', '..yYYYYy..', '.yYyyyyYy.', 'yYyyYYyyYy', 'yYyYyyyyYy', 'yYyyYYyyYy', 'yYyyyyYyYy', 'yYyyYYyyYy', '.yYyyyyYy.', '..yYYYYy..', '...yyyy...'],
             {'y': '#d4a017', 'Y': '#ffe08a'}),
    'calc': (['kkkkkkkkkk', 'kgggggggkk', 'kgGGGGGgkk', 'kgggggggkk', 'kkkkkkkkkk', 'kakbkakbkk', 'kkkkkkkkkk', 'kbkakbkakk', 'kkkkkkkkkk', 'kakbkakbkk', 'kkkkkkkkkk'],
             {'k': '#3b3f55', 'g': '#14351f', 'G': '#7cfc9a', 'a': '#e0af68', 'b': '#c9c9d1'}),
    'office': (['..oooooooooooo..', '..ooeooooooeoo..', 'oooooooooooooooo', '..oooooooooooo..', '...l.l....l.l...'],
               {'o': '#d97757', 'e': '#2a1a14', 'l': '#b5603f'}),
    'box': (['..bbbbbbbb..', '.bBBBBBBBBb.', 'bbbbbbbbbbbb', 'bBbbbttbbbBb', 'bBbbbttbbbBb', 'bBbbbbbbbbBb', 'bBbbbbbbbbBb', 'bbbbbbbbbbbb'],
            {'b': '#a8743f', 'B': '#c99158', 't': '#e9e4da'}),
    'ear': (['....s.......', '...ss...w...', 'ssssss...w..', 'ssssss.w..w.', 'ssssss.w..w.', 'ssssss...w..', '...ss...w...', '....s.......'],
            {'s': '#bb9af7', 'w': '#7dcfff'}),
}

for card in CARDS:
    a = card['accent']
    parts = [rect(0, 0, GW, GH, '#10132a', PX), rect(1, 1, GW - 2, GH - 2, '#151a3a', PX)]
    # pixel border with notched corners, in the accent color
    border = [(x, 0) for x in range(2, GW - 2)] + [(x, GH - 1) for x in range(2, GW - 2)] + \
             [(0, y) for y in range(2, GH - 2)] + [(GW - 1, y) for y in range(2, GH - 2)] + [(1, 1), (GW - 2, 1), (1, GH - 2), (GW - 2, GH - 2)]
    parts.append(path(border, a, PX))
    # icon, bobbing
    rows, pal = ICONS[card['icon']]
    s = 3
    groups = {}
    for y, line in enumerate(rows):
        for x, ch in enumerate(line):
            if ch in pal:
                for sy in range(s):
                    for sx in range(s):
                        groups.setdefault(pal[ch], []).append((x * s + sx, y * s + sy))
    parts.append('<g class="bob">' + ''.join(path(p, c, PX, GW - 14 - len(rows[0]) * s, 10) for c, p in groups.items()) + '</g>')
    # title
    tp, tw = text_pixels(FONT, card['title'], 2)
    parts.append(path(tp, '#000000', PX, 11, 11, opacity='.35'))
    parts.append(path(tp, '#ffffff', PX, 10, 10))
    parts.append(path([(x, 29) for x in range(10, 10 + tw)], a, PX))
    # description, in the reader's monospace font for legibility
    for i, line in enumerate(card['lines']):
        if line:
            parts.append(f'<text x="{10 * PX}" y="{(44 + i * 11) * PX}" fill="#c0caf5" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="{8 * PX}">{esc(line)}</text>')
    # tag chips
    x = 10
    for tag in card['tags']:
        w = len(tag) * 5 + 8
        parts.append(rect(x, 76, w, 12, '#0b0d1f', PX))
        parts.append(path([(i, 76) for i in range(x, x + w)] + [(i, 87) for i in range(x, x + w)] + [(x, j) for j in range(76, 88)] + [(x + w - 1, j) for j in range(76, 88)], a, PX, opacity='.8'))
        parts.append(f'<text x="{(x + 4) * PX}" y="{85 * PX}" fill="{a}" font-family="ui-monospace,SFMono-Regular,Menlo,Consolas,monospace" font-size="{7 * PX}">{esc(tag)}</text>')
        x += w + 4
    css = ('.bob{animation:bob 1.6s steps(2) infinite}@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}'
           '@media (prefers-reduced-motion:reduce){*{animation:none!important}}')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW * PX} {GH * PX}" width="{GW * PX}" height="{GH * PX}" '
           f'shape-rendering="crispEdges" role="img" aria-label="{esc(card["title"])}"><title>{esc(card["title"])}</title>'
           f'<style>{css}</style>{"".join(parts)}</svg>')
    open(f'{OUT}/{card["file"]}.svg', 'w').write(svg)
    print(card['file'], len(svg) // 1024, 'KB')
