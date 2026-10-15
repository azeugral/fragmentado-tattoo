# Fragmentado Tattoo Studio

Site de apresentação do estúdio [@fragmentadotattoo](https://www.instagram.com/fragmentadotattoo/), Santa Bárbara d'Oeste (SP).
Estático (HTML, CSS e JS puros), publicado no GitHub Pages: https://azeugral.github.io/fragmentado-tattoo/ (noindex enquanto for apresentação).

## Estrutura

- `index.html`: página única (hero, trabalhos, estilos, fechamento, flash, estúdio, agendamento, feedbacks, dúvidas, contato).
- `assets/site.css`, `assets/site.js`: estilo e interações (hero em fragmentos, filtro, lightbox, revelar ao rolar).
- `assets/img/`: imagens geradas por `tools/processar.py` a partir de `_ref/ig` (extração do Instagram, fora do repo).
- `tools/og.py`: gera `og.jpg`, `favicon-64.png` e `apple-touch-icon.png` com o logo fraturado.

## Identidade

- Paleta: preto `#070708`, carvão `#0e0e10`, prata `#dcdce0`, vermelho `#d3141f` (o vermelho dos posts do estúdio).
- Fontes: Anton (logo e títulos), IBM Plex Sans (texto), JetBrains Mono (etiquetas).
- Logo: "FRAGMENTADO" partido na diagonal, com a metade de baixo deslocada e um fio vermelho na fratura.
- Fundo: obsidiana estilhaçada com brilho vermelho nas fissuras, gerada por IA (versões desktop e mobile).
- Hero: a foto se monta a partir de 40 fragmentos (24 no celular) e troca a cada 6 s. Sem efeito de mouse. Com "reduzir movimento" ativo, vira um fade simples.

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
