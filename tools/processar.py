# Gera as imagens do site a partir do material extraído do Instagram (_ref/ig).
# Uso: python -I tools/processar.py  (rodar da pasta site/)
import os, json
from PIL import Image, ImageOps, ImageEnhance

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REF = os.path.join(os.path.dirname(BASE), '_ref')
IG = os.path.join(REF, 'ig')
OUT = os.path.join(BASE, 'assets', 'img')

# (arquivo em _ref/ig/posts, categoria, legenda, foco vertical 0..1)
OBRAS = [
    ('13_DeNnoy9RTR2_1.jpg', 'floral', 'Fechamento floral, antebraço', .45),
    ('32_DcxNykERk_1_1.jpg', 'floral', 'Reforma e fechamento de braço', .45),
    ('61_DYdPAWyxdKP_1.jpg', 'dark', 'Anjos, dark art no antebraço', .5),
    ('54_DZn2mzuRHQm_1.jpg', 'dark', 'Olho, rosa e ornamento', .5),
    ('46_DbwhDIqx_MI_1.jpg', 'floral', 'Rosas e folhagem, braço inteiro', .45),
    ('56_DZd_EDfx_Ap_1.jpg', 'blackwork', 'Lobo em blackwork sólido', .5),
    ('18_Dd2AE7nPWXK_1.jpg', 'lettering', 'Loyalty, lettering no antebraço', .5),
    ('21_DdmVCLORKIA_1.jpg', 'floral', 'Fechamento floral finalizado', .45),
    ('71_DUi1xGkEbuP_1.jpg', 'dark', 'Guerreira alada na panturrilha', .5),
    ('22_DdWszAfxRcN_1.jpg', 'lettering', 'Frase na coluna com flor', .4),
    ('59_DYkmN_ZxGim_1.jpg', 'floral', 'Lírios com toque de vermelho', .5),
    ('50_DbEYN6gIfsr_1.jpg', 'dark', 'Floral sombrio na coxa', .5),
    ('36_Dcg14JGRZG3_1.jpg', 'floral', 'Fechamento, cliente de Piracicaba', .45),
    ('63_DX79ZRvRQ2H_1.jpg', 'lettering', 'Nome e pezinho, homenagem', .5),
    ('27_DdJ25bIxRex_1.jpg', 'floral', 'Flores e mandala no antebraço', .45),
    ('52_DaibNYPIsyW_1.jpg', 'blackwork', 'Flash de escorpião', .45),
    ('24_DdRvbZSx-5X_1.jpg', 'floral', 'Lírio no ombro e braço', .45),
    ('69_DVEdBfeEWdG_1.jpg', 'lettering', 'Resiliência, traço fino', .5),
    ('65_DW6tLLLESdl_1.jpg', 'floral', 'Borboleta e girassol', .5),
    ('48_DbmHZv7ROP2_1.jpg', 'blackwork', 'Cruz e símbolo, autoral', .45),
    ('44_Db_cIZqRGER_1.jpg', 'floral', 'Água-viva e flores', .45),
    ('66_DWBpr3-kU49_1.jpg', 'floral', 'Rosa nas costas', .5),
    ('70_DVAIlRWETHt_1.jpg', 'floral', 'Lírios em preto e cinza', .5),
    ('55_DZd_czWxpFH_1.jpg', 'blackwork', 'Gato boxeador, old school', .45),
]
HERO = ['13_DeNnoy9RTR2_1.jpg', '61_DYdPAWyxdKP_1.jpg', '32_DcxNykERk_1_1.jpg', '54_DZn2mzuRHQm_1.jpg']
ESTILOS = {
    'floral': '46_DbwhDIqx_MI_1.jpg', 'blackwork': '56_DZd_EDfx_Ap_1.jpg',
    'dark': '71_DUi1xGkEbuP_1.jpg', 'lettering': '18_Dd2AE7nPWXK_1.jpg',
}
FLASH = ['ideias_02.jpg', 'ideias_03.jpg', 'ideias_16.jpg', 'ideias_13.jpg',
         'ideias_20.jpg', 'ideias_24.jpg', 'ideias_14.jpg', 'ideias_21.jpg']


def crop(im, ratio, fy=.5):
    w, h = im.size
    if w / h > ratio:
        nw = int(h * ratio); x = (w - nw) // 2
        return im.crop((x, 0, x + nw, h))
    nh = int(w / ratio); y = int((h - nh) * fy)
    return im.crop((0, y, w, y + nh))


def save(im, name, w, q=80):
    im = im.copy(); h = round(w * im.height / im.width)
    im.resize((w, h), Image.LANCZOS).save(os.path.join(OUT, name), 'WEBP', quality=q, method=6)


def abre(path):
    return ImageOps.exif_transpose(Image.open(path)).convert('RGB')


os.makedirs(OUT, exist_ok=True)
meta = []
for i, (f, cat, leg, fy) in enumerate(OBRAS, 1):
    im = crop(abre(os.path.join(IG, 'posts', f)), 4 / 5, fy)
    n = f'obra-{i:02d}'
    save(im, n + '.webp', min(1080, im.width))
    save(im, n + '-p.webp', 540, 76)
    meta.append({'n': n, 'cat': cat, 'leg': leg})

for i, f in enumerate(HERO, 1):
    im = crop(abre(os.path.join(IG, 'posts', f)), 4 / 5, .45)
    save(im, f'hero-{i}.webp', min(1000, im.width), 82)

for k, f in ESTILOS.items():
    im = crop(abre(os.path.join(IG, 'posts', f)), 3 / 4, .5)
    save(im, f'estilo-{k}.webp', 720)

for i, f in enumerate(FLASH, 1):
    im = abre(os.path.join(IG, 'hl', f))
    w, h = im.size
    x0 = int(w * .07); cw = w - 2 * x0; y0 = int(h * .16)
    im = im.crop((x0, y0, x0 + cw, y0 + int(cw * 1.25)))
    im = ImageEnhance.Contrast(im).enhance(1.06)
    save(im, f'flash-{i}.webp', 600, 78)

save(crop(abre(os.path.join(IG, 'perfil.jpg')), 4 / 5, .3), 'artista.webp', 800)
save(crop(abre(os.path.join(IG, 'posts', '17_Dd2SgBnTSBF_1.jpg')), 4 / 5, .5), 'artista-2.webp', 800)
save(crop(abre(os.path.join(IG, 'posts', '49_DbbqZzCkaS3_3.jpg')), 4 / 3, .5), 'convencao.webp', 900)

with open(os.path.join(BASE, 'tools', 'obras.json'), 'w', encoding='utf-8') as fh:
    json.dump(meta, fh, ensure_ascii=False, indent=1)
print('ok', len(meta))
