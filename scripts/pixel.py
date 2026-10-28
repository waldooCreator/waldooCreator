"""Shared pixel-art helpers: the Press Start 2P font rasterized to its native
8px grid, and runs of pixels written as compact SVG paths."""
from PIL import Image, ImageDraw, ImageFont

_FONTS = {}


def font(path):
    if path not in _FONTS:
        _FONTS[path] = ImageFont.truetype(path, 8)
    return _FONTS[path]


def text_pixels(font_path, text, scale=1):
    w = 8 * len(text)
    im = Image.new('1', (max(w, 1), 8), 0)
    dr = ImageDraw.Draw(im)
    dr.fontmode = '1'
    dr.text((0, 0), text, font=font(font_path), fill=1)
    pix = [(x * scale + sx, y * scale + sy) for y in range(8) for x in range(w) if im.getpixel((x, y))
           for sy in range(scale) for sx in range(scale)]
    return pix, w * scale


def path(pixels, color, px, ox=0, oy=0, cls=None, opacity=None):
    rows = {}
    for x, y in pixels:
        rows.setdefault(y, []).append(x)
    d = []
    for y, xs in sorted(rows.items()):
        xs = sorted(set(xs))
        start = prev = xs[0]
        for x in xs[1:] + [None]:
            if x is not None and x == prev + 1:
                prev = x
                continue
            w = prev - start + 1
            d.append(f'M{(ox + start) * px} {(oy + y) * px}h{w * px}v{px}h-{w * px}z')
            if x is not None:
                start = prev = x
    c = f' class="{cls}"' if cls else ''
    o = f' opacity="{opacity}"' if opacity is not None else ''
    return f'<path d="{"".join(d)}" fill="{color}"{c}{o}/>' if d else ''


def rect(x, y, w, h, color, px, extra=''):
    return f'<rect x="{x * px}" y="{y * px}" width="{w * px}" height="{h * px}" fill="{color}"{extra}/>'


def esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
