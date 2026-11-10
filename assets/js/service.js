/* H.M Media: behaviour for the generated pages (navigation, reveal on scroll, auto-playing portfolio videos). */
(() => {
  'use strict';
  const nav = document.getElementById('nav');
  const burger = document.getElementById('burger');
  if (!nav) return;

  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  if (burger) {
    const setOpen = (open) => {
      nav.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
    };
    burger.addEventListener('click', () => setOpen(!nav.classList.contains('open')));
    document.querySelectorAll('#nav-links a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
  }

  if (!('IntersectionObserver' in window)) return;

  // Reveal on scroll.
  const revealed = document.querySelectorAll('.rv');
  if (revealed.length) {
    document.documentElement.classList.add('fx');
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.15 });
    revealed.forEach((el) => io.observe(el));
  }

  // Portfolio video cards: load a muted, looping YouTube player when the card scrolls into view.
  // The thumbnail stays visible until the player reports that it is really playing.
  const still = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const frames = new Map();
  window.addEventListener('message', (e) => {
    const card = frames.get(e.source);
    if (!card || typeof e.data !== 'string') return;
    try {
      const data = JSON.parse(e.data);
      if (data.info && data.info.playerState === 1) card.classList.add('playing');
    } catch (err) { /* not a player message */ }
  });
  const vio = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (!entry.isIntersecting) return;
      vio.unobserve(entry.target);
      if (document.querySelectorAll('.wall-video iframe').length >= 6) return; // keep the page light
      const id = entry.target.dataset.video;
      const frame = document.createElement('iframe');
      frame.title = '';
      frame.tabIndex = -1;
      frame.allow = 'autoplay; encrypted-media';
      frame.setAttribute('aria-hidden', 'true');
      frame.src = `https://www.youtube-nocookie.com/embed/${id}?autoplay=1&mute=1&loop=1&playlist=${id}&controls=0&playsinline=1&rel=0&enablejsapi=1`;
      frame.addEventListener('load', () => {
        frames.set(frame.contentWindow, entry.target);
        frame.contentWindow.postMessage(JSON.stringify({ event: 'listening', id, channel: 'widget' }), '*');
      });
      entry.target.appendChild(frame);
    });
  }, { rootMargin: '100px' });
  const watchVideos = (root) => { if (!still) root.querySelectorAll('.wall-video[data-video]').forEach((el) => vio.observe(el)); };
  watchVideos(document);

  // Portfolio filters: rebuild the moving rows from the cards of the chosen kind.
  const filters = document.getElementById('wall-filters');
  const wall = document.querySelector('.wall');
  const tracks = wall ? Array.from(wall.querySelectorAll('.wall-track')) : [];
  if (!filters || !tracks.length) return;
  const source = Array.from(wall.querySelectorAll('.wall-card:not([aria-hidden])')).map((card) => card.cloneNode(true));
  const original = tracks.map((track) => track.innerHTML);
  const fill = (kind) => {
    if (kind === 'all') {
      tracks.forEach((track, i) => { track.innerHTML = original[i]; });
    } else {
      const picked = source.filter((card) => card.dataset.cat === kind);
      tracks.forEach((track, r) => {
        // Start each row at a different card, and repeat the set until the row is wider than the screen.
        const row = picked.map((_, i) => picked[(i + r * Math.ceil(picked.length / 3)) % picked.length]);
        const half = document.createDocumentFragment();
        let width = 0;
        while (width < window.innerWidth * 1.4) {
          row.forEach((card) => {
            const copy = card.cloneNode(true);
            if (width > 0 && half.childElementCount >= row.length) copy.setAttribute('aria-hidden', 'true');
            half.appendChild(copy);
            width += (Number(copy.querySelector('img').getAttribute('width')) || 240) + 16;
          });
        }
        const twin = half.cloneNode(true);
        twin.querySelectorAll('.wall-card').forEach((card) => card.setAttribute('aria-hidden', 'true'));
        track.replaceChildren(half, twin);
      });
    }
    watchVideos(wall);
  };
  filters.hidden = false;
  filters.addEventListener('click', (e) => {
    const chip = e.target.closest('[data-filter]');
    if (!chip || chip.classList.contains('active')) return;
    filters.querySelectorAll('[data-filter]').forEach((el) => {
      el.classList.toggle('active', el === chip);
      el.setAttribute('aria-pressed', String(el === chip));
    });
    wall.classList.add('swap');
    setTimeout(() => { fill(chip.dataset.filter); wall.classList.remove('swap'); }, 350);
  });
})();
