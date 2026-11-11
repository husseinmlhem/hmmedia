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

  // Portfolio: the "Looking for ...?" line cycles through the fields we work in.
  const word = document.getElementById('looking-word');
  if (!word || still) return;
  let words = [];
  try { words = JSON.parse(word.dataset.words); } catch (err) { return; }
  if (words.length < 2) return;
  let at = 0;
  setInterval(() => {
    word.classList.add('swap');
    setTimeout(() => {
      at = (at + 1) % words.length;
      word.textContent = words[at];
      word.classList.remove('swap');
    }, 320);
  }, 1900);
})();
