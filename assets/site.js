(() => {
  const d = document, root = d.documentElement;
  const calmo = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const EASE = 'cubic-bezier(.16,.84,.32,1)';

  /* ---------- header e barra mobile ---------- */
  const top = d.querySelector('.top'), barra = d.querySelector('.barra-mob');
  const aoRolar = () => {
    const y = scrollY;
    top.classList.toggle('solid', y > 24);
    if (barra) barra.classList.toggle('on', y > innerHeight * .5 && menu.hidden);
  };

  /* ---------- menu ---------- */
  const burger = d.querySelector('.burger'), menu = d.getElementById('menu');
  const fecharMenu = () => { menu.hidden = true; burger.setAttribute('aria-expanded', 'false'); root.classList.remove('lock'); };
  burger.addEventListener('click', () => {
    const abrir = menu.hidden;
    menu.hidden = !abrir; burger.setAttribute('aria-expanded', String(abrir));
    root.classList.toggle('lock', abrir);
  });
  menu.addEventListener('click', e => { if (e.target.closest('a')) fecharMenu(); });
  addEventListener('resize', () => { if (innerWidth > 1024 && !menu.hidden) fecharMenu(); });
  addEventListener('scroll', aoRolar, { passive: true }); aoRolar();

  /* ---------- revelar ao rolar ---------- */
  const io = new IntersectionObserver(es => es.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('vis'); io.unobserve(e.target); }
  }), { rootMargin: '0px 0px -8% 0px' });
  d.querySelectorAll('.rv').forEach(el => io.observe(el));

  /* ---------- hero: foto que se monta em fragmentos ---------- */
  const hx = d.querySelector('.hx');
  if (hx) {
    const frame = hx.querySelector('.hx-frame'), full = hx.querySelector('.hx-full');
    const slides = JSON.parse(hx.dataset.slides);
    const num = hx.querySelector('.hx-num'), leg = hx.querySelector('.hx-leg'), bar = hx.querySelector('.hx-bar i');
    const HOLD = 6000;
    let atual = 0, timer = 0, visivel = true, ocupado = false;

    // triângulos sobre uma malha com pontos deslocados (semente fixa: sempre o mesmo corte)
    let s = 7;
    const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
    const malha = (cols, rows) => {
      const P = [];
      for (let r = 0; r <= rows; r++) {
        P.push([]);
        for (let c = 0; c <= cols; c++) {
          const borda = c === 0 || r === 0 || c === cols || r === rows;
          const jx = borda && (c === 0 || c === cols) ? 0 : (rnd() - .5) * 70 / cols;
          const jy = borda && (r === 0 || r === rows) ? 0 : (rnd() - .5) * 70 / rows;
          P[r].push([c / cols * 100 + jx, r / rows * 100 + jy]);
        }
      }
      const T = [];
      for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
        const a = P[r][c], b = P[r][c + 1], e = P[r + 1][c + 1], f = P[r + 1][c];
        if ((r + c) % 2) T.push([a, b, e], [a, e, f]); else T.push([a, b, f], [b, e, f]);
      }
      return T;
    };
    const tris = innerWidth < 640 ? malha(3, 4) : malha(4, 5);

    const montarSet = src => {
      const g = d.createElement('div'); g.className = 'hx-set';
      g.innerHTML = tris.map(t => {
        const cx = (t[0][0] + t[1][0] + t[2][0]) / 3, cy = (t[0][1] + t[1][1] + t[2][1]) / 3;
        // 0.6% de sobra em volta de cada peça esconde a costura entre triângulos
        const pts = t.map(([x, y]) => `${(x + (x - cx) * .02).toFixed(2)}% ${(y + (y - cy) * .02).toFixed(2)}%`).join(',');
        return `<i data-c="${cx.toFixed(1)},${cy.toFixed(1)}" style="clip-path:polygon(${pts});transform-origin:${cx.toFixed(1)}% ${cy.toFixed(1)}%;background-image:url(${src})"></i>`;
      }).join('');
      frame.appendChild(g);
      return g;
    };

    const anima = (g, entrada) => Promise.all([...g.children].map(el => {
      const [cx, cy] = el.dataset.c.split(',').map(Number);
      const vx = cx - 50, vy = cy - 50, dist = Math.hypot(vx, vy);
      const k = entrada ? .9 : 1.3;
      const fora = `translate(${(vx * k + (rnd() - .5) * 20).toFixed(1)}%,${(vy * k + (rnd() - .5) * 20).toFixed(1)}%) rotate(${((rnd() - .5) * 50).toFixed(1)}deg) scale(.84)`;
      const kf = [{ transform: fora, opacity: 0 }, { transform: 'none', opacity: 1 }];
      return el.animate(entrada ? kf : kf.reverse(), {
        duration: entrada ? 1100 : 750,
        delay: entrada ? 250 + (70 - dist) * 6 + rnd() * 160 : dist * 3 + rnd() * 120,
        easing: entrada ? EASE : 'cubic-bezier(.5,0,.75,0)',
        fill: 'both'
      }).finished;
    }));

    const legenda = i => {
      num.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(slides.length).padStart(2, '0');
      leg.textContent = slides[i].leg;
      bar.classList.remove('run'); void bar.offsetWidth; bar.style.setProperty('--t', HOLD + 'ms'); bar.classList.add('run');
    };
    const carrega = src => new Promise(res => { const im = new Image(); im.onload = im.onerror = () => (im.decode ? im.decode().catch(() => {}).then(res) : res()); im.src = src; });
    const agenda = () => { clearTimeout(timer); if (visivel && !d.hidden) timer = setTimeout(proxima, HOLD); };

    async function proxima() {
      if (ocupado) return; ocupado = true;
      const prox = (atual + 1) % slides.length;
      await carrega(slides[prox].src);
      if (calmo) {
        full.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 300, fill: 'forwards' }).finished.then(() => {
          full.src = slides[prox].src; full.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, fill: 'forwards' });
        });
      } else {
        const sai = montarSet(slides[atual].src), entra = montarSet(slides[prox].src);
        full.style.visibility = 'hidden';
        await Promise.all([anima(sai, false), anima(entra, true)]);
        full.src = slides[prox].src; await carrega(slides[prox].src);
        full.style.visibility = ''; sai.remove(); entra.remove();
      }
      atual = prox; legenda(atual); ocupado = false; agenda();
    }

    // primeira montagem
    legenda(0);
    if (!calmo) {
      full.style.visibility = 'hidden';
      carrega(slides[0].src).then(() => {
        const g = montarSet(slides[0].src);
        anima(g, true).then(() => { full.style.visibility = ''; g.remove(); agenda(); });
      });
    } else agenda();

    // pausa fora da tela ou com a aba escondida
    new IntersectionObserver(([e]) => { visivel = e.isIntersecting; visivel ? agenda() : clearTimeout(timer); }).observe(hx);
    d.addEventListener('visibilitychange', () => d.hidden ? clearTimeout(timer) : agenda());
  }

  /* ---------- trabalhos: filtro e "ver mais" ---------- */
  const grade = d.querySelector('.grade');
  if (grade) {
    const obras = [...grade.children], btnMais = d.querySelector('.mais button');
    const LIM = innerWidth < 640 ? 8 : 12;
    let filtro = 'todos', aberto = false;
    const aplica = () => {
      let n = 0;
      obras.forEach(o => {
        const ok = filtro === 'todos' || o.dataset.cat === filtro;
        const mostra = ok && (aberto || filtro !== 'todos' || n < LIM);
        if (ok) n++;
        const antes = !o.classList.contains('sai');
        o.classList.toggle('sai', !mostra);
        if (mostra && !antes) { o.classList.remove('entra'); void o.offsetWidth; o.classList.add('entra'); }
      });
      btnMais.parentElement.hidden = aberto || filtro !== 'todos';
    };
    d.querySelectorAll('.filtros button').forEach(b => b.addEventListener('click', () => {
      d.querySelectorAll('.filtros button').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
      filtro = b.dataset.f; obras.forEach(o => o.classList.remove('entra')); aplica();
    }));
    btnMais.addEventListener('click', () => { aberto = true; aplica(); });
    aplica();

    /* ---------- lightbox ---------- */
    const lb = d.getElementById('lb'), lbImg = lb.querySelector('img'), lbCap = lb.querySelector('figcaption');
    let idx = 0, lista = [];
    const mostra = (i, troca) => {
      idx = (i + lista.length) % lista.length;
      const o = lista[idx];
      const set = () => { lbImg.src = o.dataset.full; lbImg.alt = o.querySelector('img').alt; lbCap.textContent = o.querySelector('.cap').textContent.trim().replace(/^(\d+)/,'$1 · '); };
      if (troca) { lbImg.classList.add('troca'); setTimeout(() => { set(); lbImg.onload = () => lbImg.classList.remove('troca'); }, 180); }
      else set();
    };
    const abrir = o => {
      lista = obras.filter(x => !x.classList.contains('sai'));
      mostra(lista.indexOf(o)); lb.hidden = false; root.classList.add('lock');
      requestAnimationFrame(() => lb.classList.add('on')); lb.querySelector('.lb-x').focus();
    };
    const fechar = () => { lb.classList.remove('on'); root.classList.remove('lock'); setTimeout(() => { lb.hidden = true; }, 300); };
    obras.forEach(o => o.addEventListener('click', () => abrir(o)));
    lb.querySelector('.lb-x').addEventListener('click', fechar);
    lb.querySelector('.lb-p').addEventListener('click', () => mostra(idx - 1, true));
    lb.querySelector('.lb-n').addEventListener('click', () => mostra(idx + 1, true));
    lb.addEventListener('click', e => { if (e.target === lb) fechar(); });
    d.addEventListener('keydown', e => {
      if (lb.hidden) return;
      if (e.key === 'Escape') fechar();
      if (e.key === 'ArrowLeft') mostra(idx - 1, true);
      if (e.key === 'ArrowRight') mostra(idx + 1, true);
    });
    let x0 = null, y0 = 0;
    lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
    lb.addEventListener('touchend', e => {
      if (x0 === null) return;
      const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) mostra(idx + (dx < 0 ? 1 : -1), true);
      x0 = null;
    });
  }

  /* ---------- ano no rodapé ---------- */
  const ano = d.getElementById('ano'); if (ano) ano.textContent = new Date().getFullYear();
})();
