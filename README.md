# Fragmentado Tattoo Studio

Site de apresentação do estúdio [@fragmentadotattoo](https://www.instagram.com/fragmentadotattoo/), Santa Bárbara d'Oeste (SP).
Estático (HTML, CSS e JS puros), publicado no GitHub Pages: https://azeugral.github.io/fragmentado-tattoo/ (noindex enquanto for apresentação).

## Estrutura

- `index.html`: página única (hero, trabalhos, estilos, fechamento, flash, estúdio, agendamento, feedbacks, dúvidas, contato).
- `assets/site.css`, `assets/site.js`: estilo e interações (hero em fragmentos, filtro, lightbox, revelar ao rolar).
- `assets/img/`: imagens geradas por `tools/processar.py` a partir de `_ref/ig` (extração do Instagram, fora do repo).
- `tools/og.py`: gera `og.jpg`, `favicon-64.png` e `apple-touch-icon.png` a partir da logo.

## Identidade

- Paleta: preto `#070708`, carvão `#0e0e10`, prata `#dcdce0`, vermelho `#d3141f` (o vermelho dos posts do estúdio).
- Fontes: Anton (títulos), Cinzel ("Tattoo Studio" sob a logo), IBM Plex Sans (texto), JetBrains Mono (etiquetas).
- Logo (v2): "FRAGMENTADO" em pincel seco, na linha do letreiro que o estúdio já usa. Gerada por IA em branco sobre preto e recortada em `assets/logo.png`/`.webp`. No site ela é aplicada como máscara com gradiente prata. O ícone é um "F" isolado no mesmo pincel (`_ref/logo/f.png`).
- Fundo (v2): minimalista, preto com um brilho vermelho suave em gradiente CSS. A obsidiana da v1 saiu.
- Hero: a foto se monta a partir de 40 fragmentos (24 no celular) e troca a cada 6 s. Sem efeito de mouse. Com "reduzir movimento" ativo, vira um fade simples.
- Intro (v3): a logo é pintada no centro, uma trinca vermelha a atravessa e a tela se parte em duas metades que abrem para a hero (cerca de 2,4 s). Depois, cada peça da hero entra em sequência.
- Fundo da hero (v3): cacos de vidro flutuando devagar (alguns vermelhos) e uma trinca vermelha fina que se desenha no fundo.
- Hero (v4): o texto virou um índice de estilos (Floral, Dark art, Blackwork, Lettering) ligado à foto. A linha ativa acende com a barra vermelha, tocar numa linha troca a foto, e no celular o índice vira uma faixa de 4 colunas sob a foto. Fotos em `HERO` do `processar.py`.
- Quebras em vermelho (v3): trincas entre seções, que se desenham ao rolar, e títulos partidos com fio vermelho (Estilos, Flash, Como agendar, contato).

## CONFIRMAR com o cliente

Dados tirados do Instagram e dos destaques. O que está marcado como genérico foi preenchido para a apresentação.

1. **Nome do tatuador**: não aparece no perfil. O site fala só em "Fragmentado".
2. **WhatsApp (19) 98958-7985**: tirado de um post de agosto. Confirmar se é o número de orçamento.
3. **Preços do flash** (até 10 cm: R$ 120; 3 por R$ 300): vieram de um post de promoção. Confirmar se valem fixos.
4. **Flash nº 01 a 08**: desenhos do destaque "Tattoo ideias". Confirmar se estão disponíveis e se são autorais.
5. **Feedbacks** (Camila R., Juliana S., Bruno M.): genéricos. Trocar por depoimentos reais (o destaque "Feedbacks" tem prints).
6. **Horário** ("seg a sáb, com hora marcada"): genérico.
7. **Tattoo a domicílio**: post de 07/10. Confirmar região atendida.
8. **Endereço**: estúdio privado; o site diz que o endereço é enviado após a confirmação.
9. **Idade mínima de 18 anos** e texto de cuidados: genéricos.
10. **Tattoo Rock 2026 (Araras)**: primeira convenção, post de 30/07.
11. **Parcelamento no cartão**: não informado.
12. **Domínio**: ainda não definido.
13. **"Agenda aberta"** no topo da hero: veio do post de agenda de outubro a dezembro. Trocar quando a agenda fechar.
