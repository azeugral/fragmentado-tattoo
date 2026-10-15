# Gera og.jpg (1200x630), favicon-64.png e apple-touch-icon.png com o logo fraturado.
# Uso: python -I tools/og.py  (rodar da pasta site/)
import os
from PIL import Image, ImageDraw, ImageFont, ImageChops

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(os.path.dirname(BASE), '_ref')
ANTON = os.path.join(REF, 'fontes', 'Anton.ttf')
PLEX = os.path.join(REF, 'fontes', 'Plex.ttf')
VERM = (211, 20, 31)


def prata(w, h):
    g = Image.new('RGB', (1, h))
    for y in range(h):
        t = y / max(1, h - 1)
        v = int(255 - t * 0.44 * 255) if t < 1 else 143
        g.putpixel((0, y), (v, v, min(255, v + 4)))
    return g.resize((w, h))


def palavra(txt, size, desloc=.045):
    f = ImageFont.truetype(ANTON, size)
    x0, y0, x1, y1 = f.getbbox(txt)
    w, h = x1 - x0 + int(size * .12), y1 - y0 + int(size * .12)
    m = Image.new('L', (w, h), 0)
    ImageDraw.Draw(m).text((-x0, -y0), txt, font=f, fill=255)
    # corte diagonal: de 63% da altura (esq.) a 40% (dir.)
    cima = Image.new('L', (w, h), 0); baixo = Image.new('L', (w, h), 0); fio = Image.new('L', (w, h), 0)
    ImageDraw.Draw(cima).polygon([(0, 0), (w, 0), (w, h * .40), (0, h * .63)], fill=255)
    ImageDraw.Draw(baixo).polygon([(0, h * .63), (w, h * .40), (w, h), (0, h)], fill=255)
    ImageDraw.Draw(fio).polygon([(0, h * .61), (w, h * .38), (w, h * .44), (0, h * .67)], fill=255)
    out = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    dx, dy = int(size * desloc), int(size * .04)
    tex = prata(w, h)
    fio_m = ImageChops.multiply(m, fio)
    out.paste(Image.new('RGB', (w, h), VERM), (int(size * .02), int(size * .02)), fio_m)
    out.paste(tex, (0, 0), ImageChops.multiply(m, cima))
    tb = ImageChops.multiply(m, baixo)
    out.paste(tex.transform(tex.size, Image.AFFINE, (1, 0, -dx, 0, 1, -dy)), (dx, dy), tb)
    return out


# og
fundo = Image.open(os.path.join(REF, 'fundo', 'd.png')).convert('RGB')
fw, fh = fundo.size
fundo = fundo.crop((0, (fh - int(fw * 630 / 1200)) // 2, fw, (fh + int(fw * 630 / 1200)) // 2)).resize((1200, 630), Image.LANCZOS)
og = fundo.copy()
lg = palavra('FRAGMENTADO', 170)
og.paste(lg, ((1200 - lg.width) // 2, 190), lg)
d = ImageDraw.Draw(og)
fs = ImageFont.truetype(PLEX, 22)
for txt, y, cor in (('T A T T O O   S T U D I O', 190 + lg.height + 18, (170, 170, 176)),
                    ('Santa Bárbara d\'Oeste · SP', 190 + lg.height + 70, (236, 236, 238))):
    w = d.textlength(txt, font=fs); d.text(((1200 - w) / 2, y), txt, font=fs, fill=cor)
og.save(os.path.join(BASE, 'og.jpg'), quality=86)

# ícones: um "F" fraturado
for nome, tam in (('favicon-64.png', 64), ('apple-touch-icon.png', 180)):
    ic = Image.new('RGB', (tam, tam), (7, 7, 8))
    f = palavra('F', int(tam * .9), .06)
    ic.paste(f, ((tam - f.width) // 2 + int(tam * .03), (tam - f.height) // 2), f)
    ic.save(os.path.join(BASE, nome))
print('ok')
