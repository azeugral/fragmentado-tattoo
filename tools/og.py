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


# prévia de link (WhatsApp, Instagram, etc.): 1200x630.
# O WhatsApp muitas vezes mostra só o quadrado central (630x630), então logo e textos ficam
# dentro dele; as laterais levam duas fotos de tattoo que somem em direção ao centro.
og = brilho(1200, 630, 600, 315, 560, VERM, .18)
for arq, x0 in (('hero-1.webp', 0), ('hero-2.webp', 860)):
    ft = Image.open(os.path.join(BASE, 'assets', 'img', arq)).convert('RGB')
    ft = ft.resize((round(630 * ft.width / ft.height), 630), Image.LANCZOS)
    ft = ft.crop(((ft.width - 340) // 2, 0, (ft.width - 340) // 2 + 340, 630))
    m = Image.new('L', (340, 630), 0); dm = ImageDraw.Draw(m)
    for x in range(340):
        t = 1 - x / 339 if x0 == 0 else x / 339  # 1 na borda externa, 0 perto do centro
        dm.line([(x, 0), (x, 630)], fill=int(255 * .62 * t ** 1.3))
    og.paste(ft, (x0, 0), m)
lw = 560; lg = logo.resize((lw, round(lw * logo.height / logo.width)), Image.LANCZOS)
y = 190
og.paste(lg, ((1200 - lw) // 2, y), lg)
d = ImageDraw.Draw(og)
fs = ImageFont.truetype(PLEX, 21); fs2 = ImageFont.truetype(PLEX, 22)
yy = y + lg.height + 26
t1 = 'T A T T O O   S T U D I O'; w1 = d.textlength(t1, font=fs)
d.text(((1200 - w1) / 2, yy), t1, font=fs, fill=(214, 214, 218))
for cx in ((1200 - w1) / 2 - 22, (1200 + w1) / 2 + 22):  # losangos vermelhos, como no site
    d.polygon([(cx, yy + 6), (cx + 6, yy + 12), (cx, yy + 18), (cx - 6, yy + 12)], fill=VERM)
t2 = "Santa Bárbara d'Oeste · SP"; w2 = d.textlength(t2, font=fs2)
d.text(((1200 - w2) / 2, yy + 52), t2, font=fs2, fill=(160, 160, 167))
og.save(os.path.join(BASE, 'og.jpg'), quality=84, optimize=True, progressive=True)

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
