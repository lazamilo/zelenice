(function () {
  const reduce = document.documentElement.classList.contains('reduce');
  const hasG = window.gsap && window.ScrollTrigger;
  if (hasG) gsap.registerPlugin(ScrollTrigger);
  const $ = (s, c = document) => c.querySelector(s);
  const $$ = (s, c = document) => [...c.querySelectorAll(s)];
  const isDesk = () => matchMedia('(min-width: 901px)').matches;

  /* smooth scroll */
  let lenis = null;
  if (!reduce && window.Lenis) {
    lenis = new Lenis({ duration: 1.15, smoothWheel: true }); window.__lenis = lenis;
    if (hasG) { lenis.on('scroll', ScrollTrigger.update); gsap.ticker.add(t => lenis.raf(t * 1000)); gsap.ticker.lagSmoothing(0); }
    else { const raf = t => { lenis.raf(t); requestAnimationFrame(raf); }; requestAnimationFrame(raf); }
  }
  $$('a[href^="#"]').forEach(a => a.addEventListener('click', e => {
    const id = a.getAttribute('href'); if (id.length < 2) return;
    const t = document.querySelector(id); if (!t) return;
    e.preventDefault(); lenis ? lenis.scrollTo(t, { offset: -100 }) : t.scrollIntoView({ behavior: 'smooth' });
  }));

  /* header */
  const hdr = $('#hdr'); const body = document.body;
  const startLight = hdr.classList.contains('light');
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    hdr.classList.toggle('solid', y > 40);
    if (!startLight) hdr.classList.toggle('light', false);
    const hide = y > lastY && y > 400 && !body.classList.contains('mega-open') && !body.classList.contains('menu-open');
    hdr.classList.toggle('hide', hide);
    lastY = y;
  };
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* mega menu */
  const megaBtn = $('#megaBtn'), mega = $('#mega'), scrim = $('#scrim');
  const closeMega = () => { body.classList.remove('mega-open'); megaBtn && megaBtn.setAttribute('aria-expanded', 'false'); };
  if (megaBtn) {
    megaBtn.addEventListener('click', () => { const o = body.classList.toggle('mega-open'); megaBtn.setAttribute('aria-expanded', o); });
    scrim.addEventListener('click', closeMega);
    addEventListener('keydown', e => { if (e.key === 'Escape') closeMega(); });
    $$('.mega li a').forEach(a => a.addEventListener('mouseenter', () => {
      $$('.mega-media img').forEach(i => i.classList.toggle('on', i.dataset.k === a.dataset.img));
    }));
    $$('.mega li a').forEach(a => a.addEventListener('click', closeMega));
  }
  const burger = $('#burger');
  burger && burger.addEventListener('click', () => { body.classList.toggle('menu-open'); lenis && (body.classList.contains('menu-open') ? lenis.stop() : lenis.start()); });
  $$('.mnav a').forEach(a => a.addEventListener('click', () => { body.classList.remove('menu-open'); lenis && lenis.start(); }));

  /* loader + hero */
  const loader = $('#loader');
  const heroIn = () => {
    if (!hasG || reduce) return;
    gsap.from('.hero h1 .l > span', { yPercent: 110, duration: 1.3, ease: 'expo.out', stagger: .12 });
    gsap.from('.hero-sub, .hero-card', { y: 30, opacity: 0, duration: 1.2, ease: 'expo.out', delay: .35, stagger: .1 });
  };
  if (loader) {
    if (hasG && !reduce && !sessionStorage.getItem('zl')) {
      try { sessionStorage.setItem('zl', 1); } catch (e) {}
      const tl = gsap.timeline();
      tl.from('.loader .lg svg', { yPercent: 105, duration: 1, ease: 'expo.out' })
        .to('.loader .bar i', { width: '100%', duration: .9, ease: 'power2.inOut' }, '-=.4')
        .to(loader, { clipPath: 'inset(0 0 100% 0)', duration: 1, ease: 'expo.inOut' }, '+=.1')
        .add(heroIn, '-=.55')
        .set(loader, { display: 'none' });
    } else { loader.style.display = 'none'; heroIn(); }
  }

  /* hero video sequence: assets/video/hero-1.mp4 ... hero-7.mp4, ~3.2s each, crossfaded.
     If the first clip can't load, the photo slideshow below stays as the fallback. */
  const hv = $('#heroVideo');
  if (hv && !reduce) {
    const CLIPS = [1, 2, 3, 4, 5, 6, 7].map(n => 'assets/video/hero-' + n + '.mp4');
    const vids = $$('video', hv); let k = 0, cur = 0, started = false;
    const load = (v, src) => { v.src = src; v.load(); };
    const show = () => {
      const v = vids[cur], other = vids[1 - cur];
      other.classList.remove('prev');
      vids.forEach(x => x.classList.remove('on'));
      other.classList.add('prev'); v.classList.add('on');
      v.currentTime = 0; const p = v.play(); p && p.catch(() => {});
      k = (k + 1) % CLIPS.length; load(other, CLIPS[k]);
      setTimeout(() => { cur = 1 - cur; show(); }, 3200);
    };
    vids[0].addEventListener('canplay', function first() {
      vids[0].removeEventListener('canplay', first);
      if (started) return; started = true;
      hv.classList.add('ready'); $('.hero-dots') && ($('.hero-dots').style.display = 'none');
      show();
    });
    vids[0].addEventListener('error', () => hv.remove(), { once: true });
    load(vids[0], CLIPS[0]);
  }

  /* hero slideshow */
  const slides = $$('.hero-media img'), dots = $$('.hero-dots i');
  if (slides.length) {
    let i = 0; slides[0].classList.add('on');
    if (!reduce) setInterval(() => {
      slides.forEach(s => s.classList.remove('prev'));
      slides[i].classList.remove('on'); slides[i].classList.add('prev'); dots[i] && dots[i].classList.remove('on');
      i = (i + 1) % slides.length;
      slides[i].classList.add('on'); dots[i] && dots[i].classList.add('on');
    }, 6000);
  }
  /* winter progress (15 Nov to 15 Mar) */
  const wb = $('#winterBar');
  if (wb) {
    const now = new Date(); let y = now.getFullYear(); if (now.getMonth() < 6) y -= 1;
    const s = new Date(y, 10, 15), e = new Date(y + 1, 2, 15);
    const p = Math.max(0, Math.min(1, (now - s) / (e - s)));
    setTimeout(() => { wb.style.transition = 'width 1.6s cubic-bezier(.22,1,.36,1)'; wb.style.width = Math.max(p * 100, 3) + '%'; }, 1800);
  }

  /* statement word reveal */
  const st = $('[data-words]');
  if (st) {
    const walk = n => { [...n.childNodes].forEach(c => {
      if (c.nodeType === 3) { const f = document.createDocumentFragment(); c.textContent.split(/(\s+)/).forEach(w => { if (!w.trim()) f.appendChild(document.createTextNode(w)); else { const s = document.createElement('span'); s.className = 'w'; s.textContent = w; f.appendChild(s); } }); c.replaceWith(f); }
    }); };
    walk(st);
    const ws = $$('.w', st);
    if (hasG && !reduce) {
      ScrollTrigger.create({ trigger: st, start: 'top 80%', end: 'bottom 45%', scrub: true,
        onUpdate: self => { const n = Math.round(self.progress * ws.length); ws.forEach((w, k) => w.classList.toggle('on', k < n)); } });
      gsap.from($$('.chip', st), { scale: 0, duration: 1, ease: 'back.out(1.6)', stagger: .15, scrollTrigger: { trigger: st, start: 'top 75%' } });
    } else ws.forEach(w => w.classList.add('on'));
  }

  /* reveals */
  if (hasG && !reduce) {
    $$('.rv').forEach(el => gsap.to(el, { opacity: 1, y: 0, duration: 1.2, ease: 'expo.out', scrollTrigger: { trigger: el, start: 'top 90%' } }));
    $$('[data-par] img, .bigcta > img').forEach(im => {
      gsap.fromTo(im, { yPercent: -6 }, { yPercent: 6, ease: 'none', scrollTrigger: { trigger: im.parentElement, start: 'top bottom', end: 'bottom top', scrub: true } });
    });
    /* counters */
    $$('[data-count]').forEach(b => {
      const to = +b.dataset.count; const o = { v: to > 1000 ? to - 40 : 0 };
      ScrollTrigger.create({ trigger: b, start: 'top 88%', once: true, onEnter: () => gsap.to(o, { v: to, duration: 1.8, ease: 'expo.out', onUpdate: () => b.textContent = Math.round(o.v) }) });
    });
  } else $$('.rv').forEach(el => { el.style.opacity = 1; el.style.transform = 'none'; });

  /* activities list */
  const acts = $$('.act'), aImgs = $$('#actsMedia img');
  const setAct = a => { acts.forEach(x => x.classList.toggle('on', x === a)); aImgs.forEach(i => i.classList.toggle('on', i.dataset.k === a.dataset.img)); };
  acts.forEach(a => {
    a.addEventListener('mouseenter', () => isDesk() && setAct(a));
    if (hasG) ScrollTrigger.create({ trigger: a, start: 'top 55%', end: 'bottom 55%', onEnter: () => isDesk() && setAct(a), onEnterBack: () => isDesk() && setAct(a) });
  });

  /* seasons horizontal */
  const track = $('#sTrack');
  if (track && hasG && !reduce) {
    const mm = gsap.matchMedia();
    mm.add('(min-width: 901px)', () => {
      const labels = $$('.s-progress span');
      const dist = () => track.scrollWidth - innerWidth;
      const tw = gsap.to(track, { x: () => -dist(), ease: 'none', scrollTrigger: {
        trigger: '#seasons', pin: '.seasons-pin', start: 'top top', end: () => '+=' + dist(), scrub: 1, invalidateOnRefresh: true,
        onUpdate: s => { const k = Math.min(3, Math.floor(s.progress * 4 * .999)); labels.forEach((l, j) => l.classList.toggle('on', j === k)); } } });
      $$('.s-panel .img img').forEach(im => gsap.fromTo(im, { scale: 1.15 }, { scale: 1, ease: 'none', scrollTrigger: { trigger: im, containerAnimation: tw, start: 'left right', end: 'right left', scrub: true } }));
    });
  }

  /* dejavnosti side nav */
  const djl = $$('#djNav a');
  if (djl.length && hasG) djl.forEach(l => {
    const s = document.querySelector(l.getAttribute('href'));
    ScrollTrigger.create({ trigger: s, start: 'top 50%', end: 'bottom 50%', onToggle: e => e.isActive && djl.forEach(x => x.classList.toggle('on', x === l)) });
  });

  /* accordions */
  $$('.acc button').forEach(b => b.addEventListener('click', () => { b.parentElement.classList.toggle('on'); setTimeout(() => hasG && ScrollTrigger.refresh(), 650); }));

  /* project modal */
  const modal = $('#modal');
  if (modal && window.PROJ) {
    const open = i => { const p = PROJ[i]; $('#mImg').src = 'assets/img/' + p.img + '.jpg'; $('#mImg').alt = p.t; $('#mDate').textContent = p.date; $('#mTitle').textContent = p.t; $('#mText').textContent = p.txt; modal.classList.add('on'); lenis && lenis.stop(); };
    const close = () => { modal.classList.remove('on'); lenis && lenis.start(); };
    $$('#pgrid .pc').forEach(c => c.addEventListener('click', e => { e.preventDefault(); open(+c.dataset.i); }));
    $('#modalX').addEventListener('click', close); modal.addEventListener('click', e => e.target === modal && close());
    addEventListener('keydown', e => e.key === 'Escape' && close());
    const m = location.hash.match(/^#p(\d+)/); if (m) setTimeout(() => open(+m[1]), 400);
  }

  addEventListener('load', () => hasG && ScrollTrigger.refresh());
})();
