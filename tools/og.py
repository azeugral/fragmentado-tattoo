# Gera og.jpg (1200x630), favicon-64.png e apple-touch-icon.png a partir de assets/logo.png.
# Uso: python -I tools/og.py  (rodar da pasta site/)
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(os.path.dirname(BASE), '_ref')
PLEX = os.path.join(REF, 'fontes', 'Plex.ttf')
PRETO, VERM = (7, 7, 8), (211, 20, 31)
logo = Image.open(os.path.join(BASE, 'assets', 'logo.png')).convert('RGBA')


def brilho(w, h, cx, cy, r, cor, forca):
    # mancha radial suave sobre o preto (o mesmo brilho vermelho do site)
    g = Image.new('L', (w, h), 0); d = ImageDraw.Draw(g)
    for k in range(60, 0, -1):
        v = int(255 * forca * (1 - k / 60) ** 2)
        d.ellipse((cx - r * k / 60, cy - r * k / 60 * .7, cx + r * k / 60, cy + r * k / 60 * .7), fill=v)
    base = Image.new('RGB', (w, h), PRETO)
    base.paste(Image.new('RGB', (w, h), cor), (0, 0), g)
    return base


og = brilho(1200, 630, 600, 300, 620, VERM, .16)
lw = 900; lg = logo.resize((lw, round(lw * logo.height / logo.width)), Image.LANCZOS)
y = 150
og.paste(lg, ((1200 - lw) // 2, y), lg)
d = ImageDraw.Draw(og)
fs = ImageFont.truetype(PLEX, 24)
for txt, yy, cor in (('T A T T O O   S T U D I O', y + lg.height + 28, (210, 210, 214)),
                     ('Santa Bárbara d\'Oeste · SP', y + lg.height + 84, (157, 157, 164))):
    w = d.textlength(txt, font=fs); d.text(((1200 - w) / 2, yy), txt, font=fs, fill=cor)
og.save(os.path.join(BASE, 'og.jpg'), quality=86)

# ícone: "F" isolado no mesmo pincel (_ref/logo/f.png, gerado por IA em branco sobre preto)
g = Image.open(os.path.join(REF, 'logo', 'f.png')).convert('L')
g = g.point(lambda v: 0 if v < 30 else 255 if v > 200 else int((v - 30) * 255 / 170))
f = Image.new('RGBA', g.size, (255, 255, 255, 0)); f.putalpha(g); f = f.crop(g.getbbox())
for nome, tam in (('favicon-64.png', 64), ('apple-touch-icon.png', 180)):
    ic = Image.new('RGB', (tam, tam), PRETO)
    s = tam * .82 / max(f.size); ff = f.resize((round(f.width * s), round(f.height * s)), Image.LANCZOS)
    ic.paste(ff, ((tam - ff.width) // 2, (tam - ff.height) // 2), ff)
    ic.save(os.path.join(BASE, nome))
print('ok')
