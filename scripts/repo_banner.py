"""Pixel-art header for a project README, in the profile banner's style.

usage: repo_banner.py FONT.ttf OUT.svg "TITLE" "subtitle" "#accent" [icon]
icon: one of calc, food, coin, none
"""
import sys
from PIL import Image, ImageDraw, ImageFont

font_path, out_path, title, subtitle, accent = sys.argv[1:6]
icon = sys.argv[6] if len(sys.argv) > 6 else 'none'
FONT = ImageFont.truetype(font_path, 8)
GW, GH, PX = 400, 64, 3
SKY = ['#0b0d1f', '#0f1230', '#141842', '#1a1d52']
parts, css = [], []


def runs(pixels, color, ox=0, oy=0, cls=None):
    rows = {}
    for x, y in pixels:
        rows.setdefault(y, []).append(x)
    d = []
    for y, xs in sorted(rows.items()):
        xs.sort()
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            w = prev - start + 1
            d.append(f'M{(ox + start) * PX} {(oy + y) * PX}h{w * PX}v{PX}h-{w * PX}z')
            if x is not None:
                start = prev = x
    c = f' class="{cls}"' if cls else ''
    parts.append(f'<path d="{"".join(d)}" fill="{color}"{c}/>')


def text_pixels(text, scale=1):
    w = 8 * len(text)
    im = Image.new('1', (w, 8), 0)
    dr = ImageDraw.Draw(im)
    dr.fontmode = '1'
    dr.text((0, 0), text, font=FONT, fill=1)
    return [(x * scale + sx, y * scale + sy) for y in range(8) for x in range(w) if im.getpixel((x, y))
            for sy in range(scale) for sx in range(scale)], w * scale


band = GH // len(SKY)
for i, c in enumerate(SKY):
    parts.append(f'<rect x="0" y="{i * band * PX}" width="{GW * PX}" height="{(band + 1) * PX}" fill="{c}"/>')
    if i:
        runs([(x, i * band) for x in range(0, GW, 2)], SKY[i - 1])

stars = [(14, 6), (52, 12), (95, 4), (140, 9), (188, 5), (233, 13), (262, 6), (305, 10), (352, 4), (388, 12), (70, 54), (330, 56)]
for k in range(3):
    runs([s for i, s in enumerate(stars) if i % 3 == k], '#fff4c2', cls=f'tw tw{k}')

# ground line in the accent color
runs([(x, GH - 3) for x in range(GW)] + [(x, GH - 2) for x in range(0, GW, 2)], accent)

scale = 3 if len(title) * 24 <= 300 else 2
tp, tw = text_pixels(title, scale)
tx = 20
ty = 12 if scale == 3 else 16
runs(tp, accent, tx + 2, ty + 2)
runs(tp, '#ffffff', tx, ty)
sp, sw = text_pixels(subtitle, 1)
runs(sp, '#c0caf5', tx, ty + 8 * scale + 8)

ICONS = {
    'calc': (['kkkkkkkkkk', 'kgggggggkk', 'kgGGGGGgkk', 'kgggggggkk', 'kkkkkkkkkk', 'kakbkakbkk', 'kkkkkkkkkk', 'kbkakbkakk', 'kkkkkkkkkk', 'kakbkakbkk', 'kkkkkkkkkk'],
             {'k': '#3b3f55', 'g': '#14351f', 'G': '#7cfc9a', 'a': '#e0af68', 'b': '#c9c9d1'}),
    'food': (['....ss....', '...s..s...', '..........', '.bbbbbbbb.', 'bbBbbBbbBb', 'bbbbbbbbbb', 'gggggggggg', 'rrrrrrrrrr', 'yyyyyyyyyy', '.bbbbbbbb.'],
             {'s': '#d8d4ff', 'b': '#e0a050', 'B': '#fff0c0', 'g': '#5fa35f', 'r': '#c0392b', 'y': '#f1c40f'}),
    'coin': (['...yyyy...', '..yYYYYy..', '.yYyyyyYy.', 'yYyyYYyyYy', 'yYyYyyyyYy', 'yYyyYYyyYy', 'yYyyyyYyYy', 'yYyyYYyyYy', '.yYyyyyYy.', '..yYYYYy..', '...yyyy...'],
             {'y': '#d4a017', 'Y': '#ffe08a'}),
}
if icon in ICONS:
    rows, pal = ICONS[icon]
    ix, iy, s = GW - 70, 14, 4
    groups = {}
    for y, line in enumerate(rows):
        for x, ch in enumerate(line):
            if ch in pal:
                for sy in range(s):
                    for sx in range(s):
                        groups.setdefault(pal[ch], []).append((x * s + sx, y * s + sy))
    parts.append('<g class="bob">')
    for c, px in groups.items():
        runs(px, c, ix, iy)
    parts.append('</g>')

css.append('.tw{animation:tw 3s steps(1) infinite}.tw1{animation-delay:-1s}.tw2{animation-delay:-2s}'
           '@keyframes tw{0%,60%{opacity:1}61%,80%{opacity:.25}81%{opacity:1}}'
           '.bob{animation:bob 1.6s steps(2) infinite}@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}'
           '@media (prefers-reduced-motion:reduce){*{animation:none!important}}')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW * PX} {GH * PX}" width="{GW * PX}" height="{GH * PX}" '
       f'shape-rendering="crispEdges" role="img" aria-label="{title} — {subtitle}"><title>{title}</title>'
       f'<style>{"".join(css)}</style>{"".join(parts)}</svg>')
open(out_path, 'w').write(svg)
print(out_path, len(svg) // 1024, 'KB')
