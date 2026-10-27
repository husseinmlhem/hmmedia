/* H.M Media — site behaviour */
(() => {
  'use strict';

  const WA_NUMBER = '971542882950';
  const FRAME_COUNT = 48;
  const FRAME_DIR = 'frames/';
  const DESIGNS_DIR = 'designs';
  const GITHUB_REPO = 'husseinmlhem/hmmedia';
  const IMAGE_RE = /\.(jpe?g|png|webp|gif)$/i;
  // Used when the GitHub API is unavailable (e.g. rate limited or running locally).
  const FALLBACK_DESIGNS = Array.from({ length: 23 }, (_, i) => `1 (${i + 1}).jpg`);
  const VIDEO_STEP = window.matchMedia('(max-width: 760px)').matches ? 4 : 6;
  const DESIGN_STEP = 8;

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));

  let lang = 'en';
  const t = (en, ar) => (lang === 'ar' ? ar : en);
  const waHref = (message) => `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(message)}`;

  /* ---------------- Language ---------------- */
  function applyLang(next) {
    lang = next === 'ar' ? 'ar' : 'en';
    const root = document.documentElement;
    root.lang = lang;
    root.dir = lang === 'ar' ? 'rtl' : 'ltr';

    $$('[data-en]').forEach((el) => {
      const text = el.dataset[lang];
      if (text != null) el.textContent = text;
    });
    $$('[data-ph-en]').forEach((el) => { el.placeholder = t(el.dataset.phEn, el.dataset.phAr); });
    $$('[data-aria-en]').forEach((el) => el.setAttribute('aria-label', t(el.dataset.ariaEn, el.dataset.ariaAr)));
    $$('.lang-btn').forEach((btn) => {
      const active = btn.dataset.lang === lang;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-pressed', String(active));
    });

    try { localStorage.setItem('hm-lang', lang); } catch (e) { /* storage unavailable */ }

    updateWhatsAppLinks();
    buildServiceOptions();
    updateIndustryCta();
    renderVideos();
    renderDesigns();
  }

  /* ---------------- WhatsApp links ---------------- */
  function requestMessage(title, price, source) {
    const priceText = price ? ` (${price})` : '';
    return lang === 'ar'
      ? `مرحباً حسين، أنا مهتم بـ: ${title}${priceText}.\nالاختيار: ${source}.\nأرجو إرسال الخطوة التالية وعرض سعر دقيق.`
      : `Hi Hussein, I'm interested in: ${title}${priceText}.\nSelected from: ${source}.\nPlease share the next step and an exact quote.`;
  }

  function updateWhatsAppLinks() {
    $$('[data-wa-en]').forEach((link) => {
      link.href = waHref(t(link.dataset.waEn, link.dataset.waAr));
    });

    $$('[data-request]').forEach((box) => {
      const link = $('.js-request', box);
      const titleEl = $('[data-request-title]', box);
      if (!link || !titleEl) return;
      const priceEl = $('[data-request-price]', box);
      const sourceBox = box.closest('[data-source-en]');
      const source = sourceBox ? t(sourceBox.dataset.sourceEn, sourceBox.dataset.sourceAr) : t('Website', 'الموقع');
      link.href = waHref(requestMessage(titleEl.textContent.trim(), priceEl ? priceEl.textContent.trim() : '', source));
    });
  }

  /* ---------------- Nav ---------------- */
  function initNav() {
    const nav = $('#nav');
    const burger = $('#burger');
    const onScroll = () => nav.classList.toggle('scrolled', window.scrollY > 24);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });

    const setOpen = (open) => {
      nav.classList.toggle('open', open);
      burger.setAttribute('aria-expanded', String(open));
    };
    burger.addEventListener('click', () => setOpen(!nav.classList.contains('open')));
    $$('#nav-links a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') setOpen(false); });

    $$('.lang-btn').forEach((btn) => btn.addEventListener('click', () => applyLang(btn.dataset.lang)));
  }

  /* ---------------- Service filters ---------------- */
  function setFilter(filter) {
    $$('.filter-btn').forEach((btn) => {
      const active = btn.dataset.filter === filter;
      btn.classList.toggle('active', active);
      btn.setAttribute('aria-selected', String(active));
    });
    $('#svc-grid').dataset.filter = filter;
    $$('.svc').forEach((card) => {
      const show = filter === 'all'
        || card.classList.contains('svc-custom')
        || card.dataset.cat === filter
        || (filter === 'new' && card.hasAttribute('data-new'));
      card.hidden = !show;
    });
  }

  function initFilters() {
    $$('.filter-btn').forEach((btn) => btn.addEventListener('click', () => setFilter(btn.dataset.filter)));
    $$('[data-filter-link]').forEach((link) => link.addEventListener('click', () => {
      setFilter(link.dataset.filterLink);
      if (link.dataset.filterLink === 'all') $('#svc-grid').classList.add('expanded');
    }));
    // On phones the full list starts collapsed to the first six services.
    $('#svc-more').addEventListener('click', () => $('#svc-grid').classList.add('expanded'));
  }

  /* ---------------- Contact form ---------------- */
  function buildServiceOptions() {
    const select = $('#cf-service');
    if (!select) return;
    const previous = select.selectedIndex;
    const titles = $$('.svc [data-request-title]').map((el) => el.textContent.trim());

    select.textContent = '';
    const placeholder = new Option(t('Select a service', 'اختر الخدمة'), '');
    placeholder.disabled = true;
    select.add(placeholder);
    titles.forEach((title) => select.add(new Option(title, title)));
    const other = t('Other / not sure', 'أخرى / غير متأكد');
    select.add(new Option(other, other));
    select.selectedIndex = previous > 0 ? previous : 0;
  }

  function initForm() {
    const form = $('#contact-form');
    if (!form) return;
    const name = $('#cf-name');
    const service = $('#cf-service');
    const details = $('#cf-details');
    const submit = $('#cf-submit');

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      let firstInvalid = null;
      [name, details].forEach((field) => {
        const invalid = !field.value.trim();
        field.setAttribute('aria-invalid', String(invalid));
        if (invalid && !firstInvalid) firstInvalid = field;
      });
      if (firstInvalid) { firstInvalid.focus(); return; }

      const chosen = service.value || t('Not selected', 'غير محددة');
      const message = lang === 'ar'
        ? `مرحباً حسين، أريد التواصل مع H.M Media بخصوص مشروع.\nالاختيار: نموذج التواصل في الموقع.\nالاسم: ${name.value.trim()}\nالخدمة: ${chosen}\nالتفاصيل: ${details.value.trim()}`
        : `Hi Hussein, I want to contact H.M Media about a project.\nSelected from: Website contact form.\nName: ${name.value.trim()}\nService: ${chosen}\nDetails: ${details.value.trim()}`;
      window.open(waHref(message), '_blank', 'noopener');

      const label = $('span', submit);
      label.textContent = t('WhatsApp opened ✓', 'تم فتح واتساب ✓');
      setTimeout(() => { label.textContent = t(label.dataset.en, label.dataset.ar); }, 2600);
    });

    [name, details].forEach((field) => field.addEventListener('input', () => field.removeAttribute('aria-invalid')));
  }

  /* ---------------- Industries ---------------- */
  let activeIndustry = 0;

  function updateIndustryCta() {
    const cta = $('#ind-cta');
    const btn = $$('.ind-btn')[activeIndustry];
    if (!cta || !btn) return;
    const name = btn.textContent.trim();
    cta.href = waHref(lang === 'ar'
      ? `مرحباً حسين، نوع عملي: ${name}.\nالاختيار: قسم حالات الاستخدام.\nأريد أفكاراً والخدمات المناسبة لعملي.`
      : `Hi Hussein, my business type: ${name}.\nSelected from: Use cases section.\nI'd like ideas and the right services for my business.`);
  }

  function initIndustries() {
    const buttons = $$('.ind-btn');
    const panels = $$('.ind-panel');
    buttons.forEach((btn, i) => btn.addEventListener('click', () => {
      activeIndustry = i;
      buttons.forEach((b, k) => {
        b.classList.toggle('active', k === i);
        b.setAttribute('aria-selected', String(k === i));
      });
      panels.forEach((p, k) => { p.hidden = k !== i; });
      updateIndustryCta();
    }));
  }

  /* ---------------- Process stepper ---------------- */
  function initStepper() {
    const rows = $$('.step-row');
    if (!rows.length || reduceMotion) return;
    let index = 0;
    let timer = null;
    const tick = () => {
      rows[index].classList.remove('active');
      index = (index + 1) % rows.length;
      rows[index].classList.add('active');
    };
    new IntersectionObserver(([entry]) => {
      clearInterval(timer);
      if (entry.isIntersecting) timer = setInterval(tick, 2400);
    }).observe(rows[0].parentElement);
  }

  /* ---------------- Reveal & card spotlight ---------------- */
  function initReveal() {
    const items = $$('.reveal');
    if (reduceMotion || !('IntersectionObserver' in window)) {
      items.forEach((el) => el.classList.add('in'));
      return;
    }
    const io = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add('in');
        io.unobserve(entry.target);
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
    items.forEach((el) => io.observe(el));
  }

  function initSpotlight() {
    if (!window.matchMedia('(hover: hover)').matches) return;
    document.addEventListener('pointermove', (e) => {
      const card = e.target.closest && e.target.closest('.card');
      if (!card) return;
      const r = card.getBoundingClientRect();
      card.style.setProperty('--mx', `${e.clientX - r.left}px`);
      card.style.setProperty('--my', `${e.clientY - r.top}px`);
    }, { passive: true });
  }

  function initMarquee() {
    const track = $('.marquee-track');
    if (!track) return;
    Array.from(track.children).forEach((item) => {
      const clone = item.cloneNode(true);
      clone.setAttribute('aria-hidden', 'true');
      track.appendChild(clone);
    });
  }

  /* ---------------- Showreel frame scrubber ---------------- */
  function initReel() {
    const reel = $('#reel');
    const canvas = $('#reel-canvas');
    const progressBar = $('#reel-progress');
    const ctx = canvas && canvas.getContext('2d');
    if (!reel || !ctx) return;

    const frames = [];
    const saveData = navigator.connection && navigator.connection.saveData;
    const wanted = [];
    for (let i = 1; i <= FRAME_COUNT; i += saveData ? 4 : 1) wanted.push(i);
    if (wanted[wanted.length - 1] !== FRAME_COUNT) wanted.push(FRAME_COUNT);
    let loaded = 0;
    let current = 1;
    let rafId = null;

    const frameSrc = (i) => `${FRAME_DIR}${String(i).padStart(4, '0')}.webp`;

    function sizeCanvas() {
      const dpr = Math.min(window.devicePixelRatio || 1, 2);
      const w = Math.round(canvas.clientWidth * dpr);
      const h = Math.round(canvas.clientHeight * dpr);
      if (canvas.width !== w || canvas.height !== h) {
        canvas.width = w;
        canvas.height = h;
      }
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      ctx.imageSmoothingQuality = 'high';
    }

    function nearest(i) {
      for (let d = 0; d < FRAME_COUNT; d++) {
        if (frames[i - d]) return frames[i - d];
        if (frames[i + d]) return frames[i + d];
      }
      return null;
    }

    function draw(i) {
      const img = nearest(i);
      if (!img) return;
      const cw = canvas.clientWidth;
      const ch = canvas.clientHeight;
      const scale = Math.max(cw / img.naturalWidth, ch / img.naturalHeight);
      const w = img.naturalWidth * scale;
      const h = img.naturalHeight * scale;
      ctx.clearRect(0, 0, cw, ch);
      ctx.drawImage(img, (cw - w) / 2, (ch - h) / 2, w, h);
    }

    // Frame 1 at the top of the page, last frame once the reel sits in the middle of the screen.
    function frameForScroll() {
      const rect = reel.getBoundingClientRect();
      const vh = window.innerHeight;
      const absTop = rect.top + window.scrollY;
      const endTop = Math.max(vh * 0.08, (vh - rect.height) / 2);
      const distance = Math.max(absTop - endTop, vh * 0.6);
      const progress = clamp(window.scrollY / distance, 0, 1);
      return Math.round(progress * (FRAME_COUNT - 1)) + 1;
    }

    function update() {
      rafId = null;
      const next = frameForScroll();
      if (next !== current) {
        current = next;
        draw(current);
      }
    }

    function load(i) {
      return new Promise((resolve) => {
        const img = new Image();
        img.decoding = 'async';
        img.onload = () => {
          frames[i] = img;
          loaded++;
          if (progressBar) progressBar.style.transform = `scaleX(${loaded / wanted.length})`;
          if (Math.abs(i - current) <= 1 || loaded === 1) draw(current);
          resolve();
        };
        img.onerror = () => { console.warn('Showreel frame failed to load:', frameSrc(i)); resolve(); };
        img.src = frameSrc(i);
      });
    }

    async function preload() {
      await load(wanted[0]);
      for (let k = 1; k < wanted.length; k += 6) {
        await Promise.all(wanted.slice(k, k + 6).map(load));
      }
      if (progressBar) progressBar.classList.add('done');
    }

    sizeCanvas();
    current = frameForScroll();
    if (document.readyState === 'complete') preload();
    else window.addEventListener('load', preload, { once: true });

    window.addEventListener('scroll', () => {
      if (!rafId) rafId = requestAnimationFrame(update);
    }, { passive: true });
    new ResizeObserver(() => { sizeCanvas(); draw(current); }).observe(canvas);
  }

  /* ---------------- Work: videos ---------------- */
  let videoIds = [];
  let videoShown = 0;
  let videoState = 'loading';

  function youTubeId(url) {
    try {
      const u = new URL(url);
      if (u.hostname.includes('youtu.be')) return u.pathname.split('/').filter(Boolean)[0] || null;
      if (u.searchParams.get('v')) return u.searchParams.get('v');
      const parts = u.pathname.split('/').filter(Boolean);
      const idx = parts.findIndex((p) => p === 'shorts' || p === 'embed');
      return idx !== -1 && parts[idx + 1] ? parts[idx + 1] : null;
    } catch (e) {
      return null;
    }
  }

  function renderVideos() {
    const grid = $('#video-grid');
    const more = $('#video-more');
    if (!grid || videoState === 'loading') return;

    if (videoState === 'error' || !videoIds.length) {
      grid.innerHTML = `<p class="work-msg">${videoState === 'error'
        ? t('Videos could not be loaded right now.', 'تعذر تحميل الفيديوهات حالياً.')
        : t('No videos yet.', 'لا توجد فيديوهات بعد.')}</p>`;
      more.hidden = true;
      return;
    }

    grid.textContent = '';
    videoIds.slice(0, videoShown).forEach((id, i) => {
      const card = document.createElement('button');
      card.type = 'button';
      card.className = 'video-card';
      card.setAttribute('aria-label', `${t('Play project', 'تشغيل العمل')} ${i + 1}`);
      card.innerHTML = `
        <img src="https://i.ytimg.com/vi/${id}/hqdefault.jpg" alt="" loading="lazy" decoding="async">
        <span class="corner" aria-hidden="true"><svg><use href="#i-out"/></svg></span>
        <span class="video-cap">
          <span class="play-sm" aria-hidden="true"><svg><use href="#i-play"/></svg></span>
          <span><b>${t('Project', 'عمل')} ${String(i + 1).padStart(2, '0')}</b><small>${t('Watch the work', 'شاهد العمل')}</small></span>
        </span>`;
      $('img', card).addEventListener('error', (e) => e.target.remove(), { once: true });
      card.addEventListener('click', () => openVideo(id));
      grid.appendChild(card);
    });
    more.hidden = videoShown >= videoIds.length;
  }

  async function loadVideos() {
    try {
      const res = await fetch('portfolio-videos.txt', { cache: 'no-cache' });
      if (!res.ok) throw new Error(`portfolio-videos.txt: HTTP ${res.status}`);
      const lines = (await res.text()).split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith('#'));
      videoIds = [...new Set(lines.map(youTubeId).filter(Boolean))];
      videoShown = Math.min(VIDEO_STEP, videoIds.length);
      videoState = 'ready';
    } catch (err) {
      console.error(err);
      videoState = 'error';
    }
    renderVideos();
  }

  /* ---------------- Work: designs ---------------- */
  let designUrls = [];
  let designShown = 0;
  let designState = 'idle';

  function renderDesigns() {
    const grid = $('#design-grid');
    const more = $('#design-more');
    if (!grid || designState !== 'ready') return;

    if (!designUrls.length) {
      grid.innerHTML = `<p class="work-msg">${t('No designs yet.', 'لا توجد تصاميم بعد.')}</p>`;
      more.hidden = true;
      return;
    }

    grid.textContent = '';
    designUrls.slice(0, designShown).forEach((src, i) => {
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'design-item';
      item.setAttribute('aria-label', `${t('Open design', 'عرض التصميم')} ${i + 1}`);
      item.innerHTML = `<img src="${src}" alt="" loading="lazy" decoding="async"><span class="corner" aria-hidden="true"><svg><use href="#i-out"/></svg></span>`;
      item.addEventListener('click', () => openLightbox(i));
      grid.appendChild(item);
    });
    more.hidden = designShown >= designUrls.length;
  }

  async function loadDesigns() {
    if (designState !== 'idle') return;
    designState = 'loading';
    let names;
    try {
      const res = await fetch(`https://api.github.com/repos/${GITHUB_REPO}/contents/${DESIGNS_DIR}`);
      if (!res.ok) throw new Error(`GitHub API: HTTP ${res.status}`);
      names = (await res.json()).filter((f) => f.type === 'file' && IMAGE_RE.test(f.name)).map((f) => f.name);
    } catch (err) {
      console.warn('Using the bundled design list instead of the GitHub API.', err);
      names = FALLBACK_DESIGNS;
    }
    names.sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));
    designUrls = names.map((n) => `${DESIGNS_DIR}/${encodeURIComponent(n)}`);
    designShown = Math.min(DESIGN_STEP, designUrls.length);
    designState = 'ready';
    renderDesigns();
  }

  function initWork() {
    const tabs = $$('.work-tab');
    tabs.forEach((tab) => tab.addEventListener('click', () => {
      tabs.forEach((x) => {
        const active = x === tab;
        x.classList.toggle('active', active);
        x.setAttribute('aria-selected', String(active));
        $(`#${x.getAttribute('aria-controls')}`).hidden = !active;
      });
      if (tab.dataset.workTab === 'designs') loadDesigns();
    }));

    $('#video-more').addEventListener('click', () => {
      videoShown = Math.min(videoShown + VIDEO_STEP, videoIds.length);
      renderVideos();
    });
    $('#design-more').addEventListener('click', () => {
      designShown = Math.min(designShown + DESIGN_STEP, designUrls.length);
      renderDesigns();
    });

    // Start fetching the video list only when the work section is close.
    const section = $('#work');
    new IntersectionObserver(([entry], obs) => {
      if (!entry.isIntersecting) return;
      obs.disconnect();
      loadVideos();
    }, { rootMargin: '600px 0px' }).observe(section);
  }

  /* ---------------- Modals ---------------- */
  let lastFocus = null;
  let lightboxIndex = 0;

  function openModal(modal) {
    lastFocus = document.activeElement;
    modal.hidden = false;
    document.body.style.overflow = 'hidden';
    $('.modal-close', modal).focus();
  }

  function closeModal(modal) {
    if (modal.hidden) return;
    modal.hidden = true;
    document.body.style.overflow = '';
    if (modal.id === 'video-modal') $('#video-frame').textContent = '';
    if (lastFocus) lastFocus.focus();
  }

  function openVideo(id) {
    $('#video-frame').innerHTML = `<iframe src="https://www.youtube-nocookie.com/embed/${id}?autoplay=1&rel=0" title="H.M Media video" allow="autoplay; encrypted-media; picture-in-picture; fullscreen" allowfullscreen></iframe>`;
    openModal($('#video-modal'));
  }

  function showLightbox(i) {
    lightboxIndex = (i + designUrls.length) % designUrls.length;
    $('#lb-img').src = designUrls[lightboxIndex];
    $('#lb-count').textContent = `${lightboxIndex + 1} / ${designUrls.length}`;
  }

  function openLightbox(i) {
    showLightbox(i);
    openModal($('#lightbox'));
  }

  function initModals() {
    $$('.modal').forEach((modal) => {
      modal.addEventListener('click', (e) => {
        if (e.target === modal || e.target.closest('[data-close]')) closeModal(modal);
      });
    });
    $('#lb-prev').addEventListener('click', () => showLightbox(lightboxIndex - 1));
    $('#lb-next').addEventListener('click', () => showLightbox(lightboxIndex + 1));

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') $$('.modal').forEach(closeModal);
      if ($('#lightbox').hidden) return;
      const forward = lang === 'ar' ? 'ArrowLeft' : 'ArrowRight';
      const back = lang === 'ar' ? 'ArrowRight' : 'ArrowLeft';
      if (e.key === forward) showLightbox(lightboxIndex + 1);
      if (e.key === back) showLightbox(lightboxIndex - 1);
    });
  }

  /* ---------------- Init ---------------- */
  function initialLang() {
    try {
      return new URLSearchParams(location.search).get('lang') || localStorage.getItem('hm-lang') || 'en';
    } catch (e) {
      return 'en';
    }
  }

  $$('[data-year]').forEach((el) => { el.textContent = new Date().getFullYear(); });
  initMarquee();
  initNav();
  initFilters();
  initForm();
  initIndustries();
  initWork();
  initModals();
  applyLang(initialLang());
  initReveal();
  initSpotlight();
  initStepper();
  initReel();
})();
