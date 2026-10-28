"""Animated pixel-art banner for the GitHub profile README.

Everything is drawn on a 400x100 pixel grid, each pixel a 3x3 rect, so the SVG
is crisp at any zoom. Text is the Press Start 2P font rasterized to its native
8px grid (exact bitmaps), so no font loads in the viewer's browser.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FONT_PATH, OUT = sys.argv[1], sys.argv[2]
FONT = ImageFont.truetype(FONT_PATH, 8)
GW, GH, PX = 400, 100, 3

# ---------------------------------------------------------------- palette
SKY = ['#0b0d1f', '#0f1230', '#141842', '#1a1d52', '#211f5e', '#2a2266']
STAR, STAR_DIM = '#fff4c2', '#8f8aa8'
MOON, MOON_SHADE = '#f4ecd2', '#d9cfae'
CITY_FAR, CITY_NEAR = '#1b1840', '#120f2c'
WIN_ON, WIN_WARM = '#ffd27a', '#f6a85b'
TITLE, TITLE_SHADOW = '#ffffff', '#d97757'
SUB, CURSOR = '#9fe8c9', '#9fe8c9'
ROOM, ROOM_DARK = '#3a2b45', '#2c2036'
LIGHT = '#ffcf8a'
HAIR, SKIN, SKIN_D = '#2b1d16', '#e8b48a', '#c99168'
HOOD, HOOD_D = '#3a7bd5', '#2c5ea8'
PHONES, PAD = '#1d1d24', '#d97757'
DESK, DESK_TOP, DESK_D = '#8a5a36', '#c8935a', '#5a3a22'
CHAIR, CHAIR_HI = '#2e3040', '#41445a'
MON, MON_D, SCREEN = '#c9c9d1', '#8d8d99', '#10131f'
CODE = ['#7aa2f7', '#9ece6a', '#e0af68', '#bb9af7', '#7dcfff', '#f7768e', '#c0caf5']
MUG, STEAM = '#e9e4da', '#d8d4ff'
PLANT, PLANT_D, POT = '#5fa35f', '#3f7a45', '#b5603f'

out = []
defs = []
css = []


def rect(x, y, w, h, color, cls=None, extra=''):
    c = f' class="{cls}"' if cls else ''
    out.append(f'<rect x="{x * PX}" y="{y * PX}" width="{w * PX}" height="{h * PX}" fill="{color}"{c}{extra}/>')


def runs(pixels, color, ox=0, oy=0, cls=None, target=None):
    """Draws a set of (x, y) pixels as horizontal runs."""
    sink = target if target is not None else out
    rows = {}
    for x, y in pixels:
        rows.setdefault(y, []).append(x)
    parts = []
    for y, xs in sorted(rows.items()):
        xs.sort()
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            parts.append(f'M{(ox + start) * PX} {(oy + y) * PX}h{(prev - start + 1) * PX}v{PX}h-{(prev - start + 1) * PX}z')
            if x is not None:
                start = prev = x
    c = f' class="{cls}"' if cls else ''
    sink.append(f'<path d="{"".join(parts)}" fill="{color}"{c}/>')


def text_pixels(text, scale=1):
    w = 8 * len(text)
    im = Image.new('1', (w, 8), 0)
    d = ImageDraw.Draw(im)
    d.fontmode = '1'
    d.text((0, 0), text, font=FONT, fill=1)
    pix = []
    for y in range(8):
        for x in range(w):
            if im.getpixel((x, y)):
                for sy in range(scale):
                    for sx in range(scale):
                        pix.append((x * scale + sx, y * scale + sy))
    return pix, w * scale


def sprite(rows, palette, ox, oy, cls=None):
    groups = {}
    for y, line in enumerate(rows):
        for x, ch in enumerate(line):
            if ch in palette:
                groups.setdefault(palette[ch], []).append((x, y))
    if cls:
        out.append(f'<g class="{cls}">')
    for color, pix in groups.items():
        runs(pix, color, ox, oy)
    if cls:
        out.append('</g>')


# ---------------------------------------------------------------- sky
band = GH // len(SKY)
for i, color in enumerate(SKY):
    rect(0, i * band, GW, band + 1, color)
    # dithered seam between bands
    if i > 0:
        runs([(x, i * band) for x in range(0, GW, 2)], SKY[i - 1])

# moon
moon = []
for y in range(-7, 8):
    for x in range(-7, 8):
        if x * x + y * y <= 49:
            moon.append((x + 7, y + 7))
runs(moon, MOON, 168, 6)
runs([(x + 7, y + 7) for x, y in [(p[0] - 7, p[1] - 7) for p in moon] if (x - 3) ** 2 + (y + 2) ** 2 <= 9], MOON_SHADE, 168, 6)
runs([(5, 9), (6, 9), (9, 4), (10, 11)], MOON_SHADE, 168, 6)

# stars: three twinkle groups
STARS = [(12, 6), (40, 14), (63, 4), (88, 20), (110, 9), (135, 17), (152, 3), (196, 22), (214, 8), (240, 15),
         (258, 5), (281, 24), (300, 11), (322, 4), (347, 18), (369, 8), (391, 21), (24, 30), (128, 33), (226, 31),
         (71, 38), (186, 40), (355, 34), (5, 44), (276, 41)]
for k in range(3):
    pix = [s for i, s in enumerate(STARS) if i % 3 == k]
    runs(pix, STAR, cls=f'tw tw{k}')
runs([(x + 1, y) for x, y in STARS[::4]] + [(x - 1, y) for x, y in STARS[::4]], STAR_DIM, cls='tw tw1')

# shooting star
out.append('<g class="shoot">')
runs([(i, i // 2) for i in range(10)], STAR_DIM)
runs([(10, 5), (11, 5)], STAR)
out.append('</g>')

# drifting clouds
CLOUD = ['....xxxx......', '..xxxxxxxx.xx.', '.xxxxxxxxxxxxx', 'xxxxxxxxxxxxxx']
out.append('<g class="cloud c1">')
sprite(CLOUD, {'x': '#22215c'}, 30, 3)
out.append('</g><g class="cloud c2">')
sprite(CLOUD, {'x': '#1d1c50'}, 230, 10)
out.append('</g>')

# ---------------------------------------------------------------- city
far = [(0, 70, 18), (18, 64, 14), (32, 74, 20), (52, 60, 12), (64, 68, 22), (86, 58, 16), (102, 72, 18),
       (120, 62, 14), (134, 70, 24), (158, 56, 12), (170, 66, 20), (190, 74, 16), (206, 62, 18), (224, 70, 20),
       (244, 60, 16), (260, 72, 14)]
for x, top, w in far:
    rect(x, top, w, GH - top, CITY_FAR)
near = [(0, 80, 26), (26, 76, 16), (42, 84, 22), (64, 74, 18), (82, 82, 24), (106, 78, 14), (120, 86, 20),
        (140, 76, 18), (158, 82, 22), (180, 78, 16), (196, 84, 20), (216, 80, 18), (234, 76, 24)]
for x, top, w in near:
    rect(x, top, w, GH - top, CITY_NEAR)
    rect(x + 2, top - 2, 2, 2, CITY_NEAR) if w > 18 else None
# lit windows, a few flicker
wins = []
for i, (x, top, w) in enumerate(far + near):
    for wy in range(top + 3, GH - 2, 4):
        for wx in range(x + 2, x + w - 2, 4):
            h = (wx * 7 + wy * 13 + i) % 11
            if h < 2:
                wins.append((wx, wy, h))
for k in range(3):
    pix = []
    for wx, wy, h in wins:
        if (wx + wy) % 3 == k:
            pix += [(wx, wy), (wx + 1, wy)]
    runs(pix, WIN_ON if k else WIN_WARM, cls=f'fl fl{k}')

# ---------------------------------------------------------------- the lit room (right)
RX, RY, RW, RH = 268, 8, 124, 74
rect(RX - 4, RY - 4, RW + 8, GH - RY + 4, '#17132f')  # building
rect(RX - 4, RY - 6, RW + 8, 2, '#221c45')  # roof edge
for wy in range(RY + 80, GH, 6):  # a few dark windows below
    for wx in range(RX + 4, RX + RW, 14):
        rect(wx, wy, 6, 3, '#221c45')
rect(RX - 2, RY - 2, RW + 4, RH + 4, '#5b4a7a')  # window frame
# The room's contents are drawn at double size on a 62x37 local grid.
out.append(f'<svg x="{RX * PX}" y="{RY * PX}" width="{RW * PX}" height="{RH * PX}" viewBox="0 0 {62 * PX} {37 * PX}" overflow="hidden">')
rect(0, 0, 62, 37, ROOM)
for i in range(16):  # warm light cone from the lamp
    rect(42 - i, 4 + i, 2 * i + 2, 1, '#45324f')
rect(0, 32, 62, 5, ROOM_DARK)
rect(0, 31, 62, 1, '#4a3757')
# shelf with books and a plant
rect(2, 11, 17, 1, DESK_D)
for i, c in enumerate(['#d97757', '#7aa2f7', '#9ece6a', '#e0af68', '#bb9af7']):
    rect(3 + i * 2, 6 + (i % 2), 2, 5 - (i % 2), c)
sprite(['.gg.', 'gGgg', 'gGGg', '.pp.', '.pp.'], {'g': PLANT, 'G': PLANT_D, 'p': POT}, 14, 6)
# poster
rect(22, 4, 9, 7, '#2a2040')
rect(23, 5, 7, 5, '#d97757')
runs([(24, 6), (25, 7), (26, 8), (27, 7), (28, 6), (26, 6)], '#ffe08a')
# hanging lamp
rect(42, 0, 1, 2, '#777')
sprite(['.LLL.', 'LLLLL'], {'L': '#e9b44c'}, 40, 2)
rect(41, 4, 3, 1, LIGHT)
# chair
sprite(['cc', 'cC', 'cC', 'cC', 'cC', 'cC', 'cC', 'cccccc', '..cc..', '..cc..', '.cccc.'], {'c': CHAIR, 'C': CHAIR_HI}, 7, 20)
# developer, side view facing the monitor
DEV = [
    '...hhhhh....',
    '..hhhhhhhh..',
    '.PhhhhhhSS..',
    '.PphhSSSSS..',
    '.PphSSSSeS..',
    '..PSSSSSSS..',
    '...SSSSSS...',
    '....dSSd....',
    '..DDDDDDDD..',
    '.DDDDDDDDDD.',
    '.DDDDDDDDDD.',
    '.DDDDDDDDD..',
    '.dddddddd...',
    '.nnnnnnnnnnn',
    '.......nn.nn',
    '.......nn.nn',
    '.......nn.nn',
    '......kkk.kkk',
]
pal = {'h': HAIR, 'S': SKIN, 'e': '#2b1d16', 'P': PHONES, 'p': PAD, 'D': HOOD, 'd': HOOD_D, 'n': '#2a2f45', 'k': '#111'}
sprite(DEV, pal, 8, 14)
# arms: two frames, typing
out.append('<g class="armA">')
runs([(16 + i, 23) for i in range(5)], HOOD)
runs([(21, 23), (22, 23)], SKIN)
out.append('</g><g class="armB">')
runs([(16 + i, 24) for i in range(4)] + [(20, 23)], HOOD)
runs([(21, 22), (22, 22)], SKIN)
out.append('</g>')
# desk
rect(19, 25, 41, 1, DESK_TOP)
rect(19, 26, 41, 2, DESK)
rect(21, 28, 2, 4, DESK_D)
rect(56, 28, 2, 4, DESK_D)
# keyboard
rect(20, 24, 8, 1, '#5d6280')
# mug with steam
sprite(['mmm.', 'mmmm', 'mmm.'], {'m': MUG}, 52, 22)
for k in range(3):
    out.append(f'<g class="steam s{k}">')
    runs([(52 + k, 20), (53, 19)], STEAM)
    out.append('</g>')
# monitor
MX, MY, MWID, MHEI = 31, 10, 18, 12
rect(MX, MY, MWID, MHEI, MON)
rect(MX + 1, MY + 1, MWID - 2, MHEI - 2, SCREEN)
rect(MX + 8, MY + MHEI, 2, 2, MON_D)
rect(MX + 6, MY + MHEI + 2, 6, 1, MON_D)
defs.append(f'<clipPath id="scr"><rect x="{(MX + 2) * PX}" y="{(MY + 2) * PX}" width="{(MWID - 4) * PX}" height="{(MHEI - 4) * PX}"/></clipPath>')
code = []
import random
rnd = random.Random(7)
for line in range(16):
    x = MX + 2 + rnd.choice([0, 0, 1, 2, 3])
    while x < MX + MWID - 3:
        ln = rnd.randint(1, 4)
        if x + ln > MX + MWID - 2:
            break
        code.append((x, MY + 2 + line * 2, ln, rnd.choice(CODE)))
        x += ln + 1
        if rnd.random() < 0.4:
            break
out.append('<g clip-path="url(#scr)"><g class="code">')
for rep in range(2):
    for x, y, ln, c in code:
        rect(x, y + rep * 32, ln, 1, c)
out.append('</g></g>')
rect(17, 18, 1, 1, '#9ec5ff')  # screen glow on the face
out.append('</svg>')
# window mullion over the room
rect(RX + RW // 2 - 1, RY, 2, RH, '#5b4a7a') if False else None

# ---------------------------------------------------------------- title and subtitle
title_pix, tw = text_pixels('WALTER VELASCO', 2)
runs(title_pix, TITLE_SHADOW, 18, 21)
runs(title_pix, TITLE, 16, 19)

PHRASES = [
    'Software Engineer',
    'Ingeniero de Software',
    '.NET  TypeScript  Python',
    'Building with AI agents',
]
HOLD, TYPE_STEP, ERASE = 2.2, 0.07, 0.5
slots = []
t = 0.0
for p in PHRASES:
    dur = len(p) * TYPE_STEP + HOLD + ERASE
    slots.append((t, dur))
    t += dur
TOTAL = t

prompt_pix, pw = text_pixels('>', 1)
runs(prompt_pix, TITLE_SHADOW, 16, 44)
SX, SY = 28, 44
for i, (p, (start, dur)) in enumerate(zip(PHRASES, slots)):
    pix, w = text_pixels(p, 1)
    n = len(p)
    # keyTimes over the whole cycle: hidden, typing char by char, hold, erase
    times, widths, curx = [0.0], [0], [SX]
    for k in range(n + 1):
        times.append((start + k * TYPE_STEP) / TOTAL)
        widths.append(k * 8)
        curx.append(SX + k * 8)
    times.append((start + n * TYPE_STEP + HOLD) / TOTAL)
    widths.append(n * 8)
    curx.append(SX + n * 8)
    times.append((start + dur - 0.001) / TOTAL)
    widths.append(0)
    curx.append(SX)
    times.append(1.0)
    widths.append(0)
    curx.append(SX)
    kt = ';'.join(f'{x:.4f}' for x in times)
    defs.append(
        f'<clipPath id="t{i}"><rect x="{SX * PX}" y="{SY * PX}" height="{8 * PX}" width="0">'
        f'<animate attributeName="width" dur="{TOTAL:.2f}s" repeatCount="indefinite" calcMode="discrete" '
        f'keyTimes="{kt}" values="{";".join(str(w * PX) for w in widths)}"/></rect></clipPath>'
    )
    out.append(f'<g clip-path="url(#t{i})">')
    runs(pix, SUB, SX, SY)
    out.append('</g>')
    # this phrase's cursor, shown only during its slot
    vis = ['0'] + ['1'] * (n + 1) + ['1', '0', '0']
    out.append(
        f'<rect y="{SY * PX}" width="{6 * PX}" height="{7 * PX}" fill="{CURSOR}" opacity="0" class="cur">'
        f'<animate attributeName="x" dur="{TOTAL:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{";".join(str(x * PX) for x in curx)}"/>'
        f'<animate attributeName="opacity" dur="{TOTAL:.2f}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt}" values="{";".join(vis)}"/>'
        f'</rect>'
    )

small, _ = text_pixels('@waldooCreator', 1)
runs(small, '#5d588f', 16, 60)

# ---------------------------------------------------------------- styles
css.append('''
.tw{animation:tw 3s steps(1) infinite}.tw1{animation-delay:-1s}.tw2{animation-delay:-2s}
@keyframes tw{0%,60%{opacity:1}61%,80%{opacity:.25}81%{opacity:1}}
.fl{animation:fl 7s steps(1) infinite}.fl1{animation-delay:-2.5s}.fl2{animation-delay:-5s}
@keyframes fl{0%,70%{opacity:1}71%,85%{opacity:0}86%{opacity:1}}
.shoot{opacity:0;animation:sh 9s linear infinite}
@keyframes sh{0%,82%{opacity:0;transform:translate(60px,20px)}83%{opacity:1}92%{opacity:1;transform:translate(330px,155px)}93%,100%{opacity:0;transform:translate(330px,155px)}}
.cloud{animation:cl 60s linear infinite}.c2{animation-duration:85s;animation-delay:-30s}
@keyframes cl{from{transform:translateX(-160px)}to{transform:translateX(860px)}}
.armA{animation:ta .5s steps(1) infinite}.armB{animation:ta .5s steps(1) infinite;animation-delay:-.25s}
@keyframes ta{0%,49%{opacity:1}50%,100%{opacity:0}}
.code{animation:sc 8s steps(32) infinite}
@keyframes sc{from{transform:translateY(0)}to{transform:translateY(-96px)}}
.steam{animation:st 2.4s steps(4) infinite;opacity:0}.s1{animation-delay:-.8s}.s2{animation-delay:-1.6s}
@keyframes st{0%{opacity:.9;transform:translateY(0)}100%{opacity:0;transform:translateY(-12px)}}
.cur{animation:bl 1s steps(1) infinite}
@keyframes bl{0%,50%{fill-opacity:1}51%,100%{fill-opacity:0}}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
''')

svg = (
    f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {GW * PX} {GH * PX}" width="{GW * PX}" height="{GH * PX}" '
    f'shape-rendering="crispEdges" role="img" aria-label="Walter Velasco — Software Engineer">'
    f'<title>Walter Velasco — Software Engineer</title>'
    f'<defs>{"".join(defs)}</defs><style>{"".join(css)}</style>'
    + ''.join(out)
    + '</svg>'
)
open(OUT, 'w').write(svg)
print(f'{OUT}: {len(svg) // 1024} KB, cycle {TOTAL:.1f}s')
