/* H.M Media: behaviour for the service pages (navigation only; the pages are static HTML). */
(() => {
  'use strict';
  const nav = document.getElementById('nav');
  const burger = document.getElementById('burger');
  if (!nav) return;

  const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 24);
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });

  if (!burger) return;
  const setOpen = (open) => {
    nav.classList.toggle('open', open);
    burger.setAttribute('aria-expanded', String(open));
  };
  burger.addEventListener('click', () => setOpen(!nav.classList.contains('open')));
  document.querySelectorAll('#nav-links a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });
})();
