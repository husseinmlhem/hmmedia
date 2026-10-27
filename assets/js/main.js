/* H.M Media — site behaviour */
(() => {
  'use strict';

  const WA_NUMBER = '971542882950';
  const PLAYLIST_ID = 'PLqqrYKCZFlioU3ZsRjw3uf1_qfNR9sRE5';
  const FRAME_COUNT = 48;
  const FRAME_DIR = 'frames/';
  const GALLERY_STEP = window.matchMedia('(max-width: 760px)').matches ? 8 : 12;

  // Example requests typed into the AI studio box, one per result panel.
  const DEMOS = [
    { key: 'images', en: 'Luxury product photos of my water bottle floating in the clouds', ar: 'صور فاخرة لزجاجة المياه الخاصة بي وهي تطفو بين الغيوم' },
    { key: 'video', en: 'A 15-second National Day video ad for my brand', ar: 'فيديو إعلاني مدته 15 ثانية لعلامتي بمناسبة اليوم الوطني' },
    { key: 'chat', en: 'A WhatsApp assistant that answers customers and books appointments', ar: 'مساعد واتساب يرد على العملاء ويحجز المواعيد' },
    { key: 'app', en: 'A web app that writes product descriptions in Arabic and English', ar: 'تطبيق ويب يكتب أوصاف المنتجات بالعربية والإنجليزية' },
    { key: 'flow', en: 'Send every new lead from Instagram to WhatsApp and my CRM', ar: 'أرسل كل عميل جديد من إنستغرام إلى واتساب ونظام إدارة العملاء' },
  ];

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (sel, root = document) => root.querySelector(sel);
  const $$ = (sel, root = document) => Array.from(root.querySelectorAll(sel));
  const clamp = (v, min, max) => Math.min(max, Math.max(min, v));
  const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  let lang = 'en';
  const t = (en, ar) => (lang === 'ar' ? ar : en);
  const waHref = (message) => `https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(message)}`;
  const openWhatsApp = (message) => window.open(waHref(message), '_blank', 'noopener');

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
    renderGallery();
    studio.restart();
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

  /* ---------------- AI studio (hero) ---------------- */
  const studio = (() => {
    const form = $('#prompt-form');
    const input = $('#prompt-input');
    const stage = $('#result-stage');
    const chips = $$('.pchip');
    const panels = $$('.result-panel');
    let run = 0;          // bumps to cancel a running demo loop
    let engaged = false;  // the visitor typed or picked an example
    let visible = true;

    function selectChip(key) {
      chips.forEach((chip) => {
        const active = chip.dataset.demo === key;
        chip.classList.toggle('active', active);
        chip.setAttribute('aria-selected', String(active));
      });
    }

    async function showPanel(key, token) {
      if (!reduceMotion) {
        stage.classList.add('loading');
        await wait(750);
        if (token !== run) return;
      }
      panels.forEach((p) => p.classList.toggle('active', p.dataset.panel === key));
      stage.classList.remove('loading');
    }

    async function typePlaceholder(text, token) {
      for (let i = 1; i <= text.length; i++) {
        if (token !== run) return false;
        input.placeholder = text.slice(0, i);
        await wait(32);
      }
      return token === run;
    }

    async function loop(token) {
      for (let i = 0; token === run; i = (i + 1) % DEMOS.length) {
        const demo = DEMOS[i];
        selectChip(demo.key);
        if (!(await typePlaceholder(demo[lang], token))) return;
        await showPanel(demo.key, token);
        await wait(3400);
        while (token === run && !visible) await wait(400);
      }
    }

    function restart() {
      run++;
      stage.classList.remove('loading');
      if (engaged || reduceMotion) {
        if (!engaged) input.placeholder = DEMOS[0][lang];
        return;
      }
      loop(run);
    }

    function stop() {
      engaged = true;
      run++;
      stage.classList.remove('loading');
      input.placeholder = t(input.dataset.phEn, input.dataset.phAr);
    }

    function autoGrow() {
      input.style.height = 'auto';
      input.style.height = `${Math.min(input.scrollHeight, 160)}px`;
    }

    chips.forEach((chip) => chip.addEventListener('click', () => {
      const demo = DEMOS.find((d) => d.key === chip.dataset.demo);
      stop();
      selectChip(demo.key);
      input.value = demo[lang];
      autoGrow();
      showPanel(demo.key, run);
    }));

    input.addEventListener('focus', stop);
    input.addEventListener('input', () => {
      autoGrow();
      input.closest('.prompt-box').classList.remove('invalid');
    });
    input.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); form.requestSubmit(); }
    });

    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (!text) {
        input.closest('.prompt-box').classList.add('invalid');
        input.focus();
        return;
      }
      openWhatsApp(lang === 'ar'
        ? `مرحباً حسين، أريد تنفيذ هذا بالذكاء الاصطناعي:\n${text}\nالاختيار: استوديو الذكاء الاصطناعي في الموقع.`
        : `Hi Hussein, I'd like to create this with AI:\n${text}\nSelected from: AI Studio on the website.`);
    });

    new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; }).observe(form.closest('.mock'));

    return { restart };
  })();

  /* ---------------- Contact form ---------------- */
  function buildServiceOptions() {
    const select = $('#cf-service');
    if (!select) return;
    const previous = select.selectedIndex;
    select.textContent = '';

    const placeholder = new Option(t('Select a service', 'اختر الخدمة'), '');
    placeholder.disabled = true;
    select.add(placeholder);

    [['ai', t('AI services', 'خدمات الذكاء الاصطناعي')], ['agency', t('Agency services', 'خدمات الوكالة')]].forEach(([id, label]) => {
      const group = document.createElement('optgroup');
      group.label = label;
      $$(`#${id} [data-service] [data-request-title]`).forEach((el) => {
        const title = el.textContent.trim();
        group.appendChild(new Option(title, title));
      });
      select.appendChild(group);
    });
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
      openWhatsApp(lang === 'ar'
        ? `مرحباً حسين، أريد التواصل مع H.M Media بخصوص مشروع.\nالاختيار: نموذج التواصل في الموقع.\nالاسم: ${name.value.trim()}\nالخدمة: ${chosen}\nالتفاصيل: ${details.value.trim()}`
        : `Hi Hussein, I want to contact H.M Media about a project.\nSelected from: Website contact form.\nName: ${name.value.trim()}\nService: ${chosen}\nDetails: ${details.value.trim()}`);

      const label = $('span', submit);
      label.textContent = t('WhatsApp opened ✓', 'تم فتح واتساب ✓');
      setTimeout(() => { label.textContent = t(label.dataset.en, label.dataset.ar); }, 2600);
    });

    [name, details].forEach((field) => field.addEventListener('input', () => field.removeAttribute('aria-invalid')));
  }

  /* ---------------- Reveal, spotlight, marquee ---------------- */
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

  /* ---------------- Video portfolio: showreel poster + playlist ---------------- */
  function initPlayer() {
    const player = $('#player');
    const canvas = $('#reel-canvas');
    const progressBar = $('#reel-progress');
    const ctx = canvas && canvas.getContext('2d');
    if (!player || !ctx) return;

    $('#player-start').addEventListener('click', () => {
      player.classList.add('playing');
      const iframe = document.createElement('iframe');
      iframe.src = `https://www.youtube-nocookie.com/embed/videoseries?list=${PLAYLIST_ID}&autoplay=1&rel=0`;
      iframe.title = 'H.M Media video portfolio';
      iframe.allow = 'autoplay; encrypted-media; picture-in-picture; fullscreen';
      iframe.allowFullscreen = true;
      player.appendChild(iframe);
    });

    // The poster is the H.M showreel: 48 frames scrubbed as the player scrolls into view.
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

    // First frame when the player enters at the bottom, last frame once it is centred.
    function frameForScroll() {
      const rect = player.getBoundingClientRect();
      const vh = window.innerHeight;
      const endTop = Math.max(vh * 0.08, (vh - rect.height) / 2);
      const progress = clamp((vh - rect.top) / Math.max(vh - endTop, 1), 0, 1);
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
      current = frameForScroll();
      await load(current);
      const rest = wanted.filter((i) => i !== current);
      for (let k = 0; k < rest.length; k += 6) {
        await Promise.all(rest.slice(k, k + 6).map(load));
      }
      if (progressBar) progressBar.classList.add('done');
    }

    sizeCanvas();
    // Only download the frames when the visitor gets close to the player.
    new IntersectionObserver(([entry], obs) => {
      if (!entry.isIntersecting) return;
      obs.disconnect();
      preload();
    }, { rootMargin: '800px 0px' }).observe(player);

    window.addEventListener('scroll', () => {
      if (!rafId) rafId = requestAnimationFrame(update);
    }, { passive: true });
    new ResizeObserver(() => { sizeCanvas(); draw(current); }).observe(canvas);
  }

  /* ---------------- Image portfolio (public Google Drive folder) ---------------- */
  let galleryItems = [];
  let galleryShown = 0;
  let galleryState = 'loading';
  let lightboxIndex = 0;

  // Drive serves resized copies of public files, so phones never download the full-size originals.
  const driveSrc = (id, width) => `https://lh3.googleusercontent.com/d/${id}=w${width}`;
  const driveFallback = (id, width) => `https://drive.google.com/thumbnail?id=${id}&sz=w${width}`;

  function loadDriveImage(img, item, width, onFail) {
    img.addEventListener('error', function retry() {
      img.removeEventListener('error', retry);
      img.addEventListener('error', onFail, { once: true });
      img.src = driveFallback(item.id, width);
    });
    img.src = driveSrc(item.id, width);
  }

  function renderGallery() {
    const grid = $('#gallery');
    const more = $('#gallery-more');
    if (!grid || galleryState === 'loading') return;

    if (galleryState === 'error' || !galleryItems.length) {
      grid.innerHTML = `<p class="work-msg">${t('The gallery could not be loaded here — open the full gallery instead.', 'تعذر تحميل المعرض هنا — افتح المعرض الكامل.')}</p>`;
      more.hidden = true;
      return;
    }

    grid.textContent = '';
    galleryItems.slice(0, galleryShown).forEach((item, i) => {
      if (item.failed) return;
      const btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'design-item';
      btn.setAttribute('aria-label', `${t('Open', 'عرض')}: ${item.title}`);
      const img = document.createElement('img');
      img.alt = item.title;
      img.loading = 'lazy';
      img.decoding = 'async';
      img.addEventListener('load', () => btn.classList.add('loaded'), { once: true });
      loadDriveImage(img, item, 800, () => {
        item.failed = true;
        btn.remove();
        if (!$('.design-item', grid)) {
          grid.innerHTML = `<p class="work-msg">${t('The gallery could not be loaded here — open the full gallery instead.', 'تعذر تحميل المعرض هنا — افتح المعرض الكامل.')}</p>`;
        }
      });
      const cap = document.createElement('span');
      cap.className = 'design-cap';
      cap.textContent = item.title;
      btn.append(img, cap);
      btn.addEventListener('click', () => openLightbox(i));
      grid.appendChild(btn);
    });
    more.hidden = galleryShown >= galleryItems.length;
  }

  async function loadGallery() {
    try {
      const res = await fetch('assets/data/gallery.json', { cache: 'no-cache' });
      if (!res.ok) throw new Error(`gallery.json: HTTP ${res.status}`);
      galleryItems = (await res.json()).images || [];
      galleryShown = Math.min(GALLERY_STEP, galleryItems.length);
      galleryState = 'ready';
    } catch (err) {
      console.error(err);
      galleryState = 'error';
    }
    renderGallery();
  }

  function initGallery() {
    $('#gallery-more').addEventListener('click', () => {
      galleryShown = Math.min(galleryShown + GALLERY_STEP, galleryItems.length);
      renderGallery();
    });
    new IntersectionObserver(([entry], obs) => {
      if (!entry.isIntersecting) return;
      obs.disconnect();
      loadGallery();
    }, { rootMargin: '800px 0px' }).observe($('#gallery'));
  }

  /* ---------------- Lightbox ---------------- */
  let lastFocus = null;

  function showLightbox(i, step = 1) {
    const total = galleryItems.length;
    for (let n = 0; n < total; n++) {
      const idx = ((i + n * step) % total + total) % total;
      if (!galleryItems[idx].failed) { lightboxIndex = idx; break; }
    }
    const item = galleryItems[lightboxIndex];
    const img = $('#lb-img');
    img.alt = item.title;
    loadDriveImage(img, item, 2000, () => {});
    $('#lb-cap').textContent = `${item.title} · ${lightboxIndex + 1} / ${total}`;
  }

  function openLightbox(i) {
    lastFocus = document.activeElement;
    showLightbox(i);
    const box = $('#lightbox');
    box.hidden = false;
    document.body.style.overflow = 'hidden';
    $('.modal-close', box).focus();
  }

  function closeLightbox() {
    const box = $('#lightbox');
    if (box.hidden) return;
    box.hidden = true;
    document.body.style.overflow = '';
    $('#lb-img').removeAttribute('src');
    if (lastFocus) lastFocus.focus();
  }

  function initLightbox() {
    const box = $('#lightbox');
    box.addEventListener('click', (e) => {
      if (e.target === box || e.target.closest('[data-close]')) closeLightbox();
    });
    $('#lb-prev').addEventListener('click', () => showLightbox(lightboxIndex - 1, -1));
    $('#lb-next').addEventListener('click', () => showLightbox(lightboxIndex + 1, 1));
    document.addEventListener('keydown', (e) => {
      if (box.hidden) return;
      if (e.key === 'Escape') closeLightbox();
      const forward = lang === 'ar' ? 'ArrowLeft' : 'ArrowRight';
      const back = lang === 'ar' ? 'ArrowRight' : 'ArrowLeft';
      if (e.key === forward) showLightbox(lightboxIndex + 1, 1);
      if (e.key === back) showLightbox(lightboxIndex - 1, -1);
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
  initForm();
  initGallery();
  initLightbox();
  applyLang(initialLang());
  initReveal();
  initSpotlight();
  initPlayer();
})();
