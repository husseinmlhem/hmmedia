"""Renders the per-service landing pages (English at /services/<slug>/, Arabic at /ar/services/<slug>/).

Called by tools/build.py. Each page is plain, static, single-language HTML so search engines and AI
crawlers read it without running JavaScript. Copy comes from tools/service_content.py; names, prices
and shared FAQ answers come from index.html (passed in through `ctx`).
"""
from __future__ import annotations

import hashlib
import html
import json
import pathlib
import urllib.parse

import service_content as sc

LANG_PREFIX = {"en": "", "ar": "/ar"}
ROOT = pathlib.Path(__file__).resolve().parent.parent


def asset_version(relative: str) -> str:
    """'assets/css/style.css' -> 'assets/css/style.css?v=<content hash>', so an updated file is never served from cache."""
    digest = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()[:10]
    return f"{relative}?v={digest}"


def esc(text: str) -> str:
    return html.escape(text, quote=False)


def qa(text: str) -> str:
    return html.escape(text, quote=True)


def path(lang: str, slug: str) -> str:
    return f"{LANG_PREFIX[lang]}/services/{slug}/"


def home_path(lang: str, anchor: str = "") -> str:
    return f"{LANG_PREFIX[lang]}/{anchor}"


def wa_link(ctx: dict, message: str) -> str:
    # Same encoding as encodeURIComponent() in assets/js/main.js.
    return f"{ctx['WHATSAPP']}?text={urllib.parse.quote(message, safe=chr(45) + '_.!~*()' + chr(39))}"


# ------------------------------------------------------------------------------------ page model
def resolve_pages(ctx: dict) -> list[dict]:
    """Joins the hand-written copy with the services parsed from index.html."""
    page = ctx["page"]
    resolved = []
    for definition in sc.AI_PAGES:
        service = next((s for s in page.services if s["title"] and s["price"] and s["title"]["en"] == definition["match"]), None)
        if not service:
            raise SystemExit(f"service_content: no service titled {definition['match']!r} on the home page")
        resolved.append({**definition, "kind": "ai", "service": service, "label": service["title"]})
    for definition in sc.GROUP_PAGES:
        items = [s for s in page.services if s["group"] and s["group"]["en"] == definition["match"] and s["title"] and s["price"]]
        if not items:
            raise SystemExit(f"service_content: no agency group titled {definition['match']!r} on the home page")
        resolved.append({**definition, "kind": "group", "items": items})
    return resolved


def find_faq(ctx: dict, english_question: str):
    return next((f for f in ctx["page"].faqs if f["q"] and f["a"] and f["q"]["en"] == english_question), None)


def price_of(p: dict, lang: str) -> str:
    if p["kind"] == "ai":
        return p["service"]["price"][lang]
    cheapest = min(p["items"], key=lambda s: ctx_price_value(s))
    return cheapest["price"][lang]


_PRICE_PARSER = None


def ctx_price_value(service: dict) -> int:
    amount, _unit = _PRICE_PARSER(service["price"]["en"])
    return amount if amount is not None else 10**9


def faq_list(ctx: dict, p: dict, lang: str) -> list[dict]:
    """Page-specific questions first, then the shared answers from the home page."""
    start = price_of(p, lang)
    if p["kind"] == "ai":
        cost_q = {"en": f"How much does {p['label']['en']} cost?", "ar": f"كم تبلغ تكلفة {p['label']['ar']}؟"}
    else:
        cost_q = {"en": f"How much do {p['label']['en']} services cost?", "ar": f"كم تبلغ تكلفة خدمات {p['label']['ar']}؟"}
    cost_a = {
        "en": f"Prices start from {start}. They are approximate starting points: tell us your budget and goal, and you get an exact quote before any work starts.",
        "ar": f"تبدأ الأسعار من {start}. هي أسعار بداية تقريبية: أخبرنا بميزانيتك وهدفك وتحصل على عرض سعر دقيق قبل بدء أي عمل.",
    }
    items = [{"q": cost_q, "a": cost_a}]
    items += p.get("faq", [])
    for question in p.get("faq_extra", []) + sc.SHARED_FAQ:
        shared = find_faq(ctx, question)
        if shared and all(shared["q"]["en"] != i["q"]["en"] for i in items):
            items.append({"q": shared["q"], "a": shared["a"]})
    return items


# ------------------------------------------------------------------------------------ shared blocks
def link_label(p: dict, lang: str) -> str:
    return p["label"][lang]


HOME_WALL_STILLS = 10  # assets/home/wall-01.webp ... : stills from video and motion work for other clients


def home_wall_block(ctx: dict) -> str:
    """Decorative moving wall of work for the home page (two rows; the full, filterable wall is on /work/).
    Video stills and designs alternate, so no single client fills the wall."""
    still_width = round(WALL_ROW_HEIGHT * 16 / 9)
    stills = [(f"/assets/home/wall-{n:02d}.webp", still_width) for n in range(1, HOME_WALL_STILLS + 1)]
    designs = [(d["thumb"], round(WALL_ROW_HEIGHT * d["w"] / d["h"])) for d in ctx["designs"]]
    designs = designs[13:] + designs[:13]  # start with the property, retail and social work
    mixed = []
    for i in range(max(len(stills), len(designs))):
        mixed += stills[i:i + 1] + designs[i:i + 1]
    rows = []
    for r in range(2):
        cards = "".join(
            f'<div class="wall-card"><img src="{src}" width="{width}" height="{WALL_ROW_HEIGHT}" loading="lazy" alt=""></div>'
            for src, width in mixed[r::2]
        )
        rows.append(f'    <div class="wall-row{" wall-row--rev" if r else ""}"><div class="wall-track" style="--t:{90 + r * 18}s">{cards}{cards}</div></div>')
    return "\n".join([
        "<!-- build:home-wall (generated by tools/build.py) -->",
        '<div class="wall wall--home" aria-hidden="true">',
        '  <div class="wall-plane">',
        *rows,
        "  </div>",
        "</div>",
        "<!-- /build:home-wall -->",
    ])


def service_links_block(ctx: dict, pages: list[dict]) -> str:
    """Footer link list shown on the home page, written once with both languages (build.py swaps it for /ar/)."""
    lines = [
        '<!-- build:service-links (generated by tools/build.py) -->',
        '<nav class="footer-services" aria-label="Services">',
        '  <h3 class="footer-h" data-en="Services" data-ar="الخدمات">Services</h3>',
        "  <ul>",
    ]
    for p in pages:
        lines.append(
            f'    <li><a href="{path("en", p["slug"])}" data-href-ar="{path("ar", p["slug"])}" '
            f'data-en="{qa(link_label(p, "en"))}" data-ar="{qa(link_label(p, "ar"))}">{esc(link_label(p, "en"))}</a></li>'
        )
    lines += ["  </ul>", "</nav>", "<!-- /build:service-links -->"]
    return "\n".join(lines)


def header_html(ctx: dict, lang: str, slug: str, alt_paths: dict | None = None) -> str:
    ui = sc.UI[lang]
    paths = alt_paths or {"en": path("en", slug), "ar": path("ar", slug)}
    links = "\n".join(
        f'        <li class="nav-one"><a href="{home_path(lang, anchor)}" aria-label="H.M One"><img src="/assets/img/hm-one-logo.svg" width="1014" height="614" alt="H.M One"></a></li>'
        if anchor == "one/" else f'        <li><a href="{home_path(lang, anchor)}">{esc(label)}</a></li>'
        for anchor, label in ui["nav"]
    )
    message = ui["wa_talk"].format(source=("زر ابدأ مشروعك" if lang == "ar" else "Start Project button"))
    en_current = ' class="lang-btn active" aria-current="true"' if lang == "en" else ' class="lang-btn"'
    ar_current = ' class="lang-btn active" aria-current="true"' if lang == "ar" else ' class="lang-btn"'
    cta = f'<a class="btn btn-accent btn-sm nav-cta" href="{qa(wa_link(ctx, message))}" target="_blank" rel="noopener"><span>{esc(ui["start"])}</span> <span class="arr" aria-hidden="true">→</span></a>'
    return f"""<header class="nav" id="nav">
  <div class="container nav-inner">
    <a href="{home_path(lang)}" class="brand" aria-label="H.M Media">
      <svg class="brand-mark"><use href="#i-logo"/></svg>
      <span>H.M Media</span>
    </a>
    <nav aria-label="Main">
      <ul class="nav-links" id="nav-links">
{links}
      </ul>
    </nav>
    <div class="nav-actions">
      <div class="lang-switch" role="group" aria-label="{qa(ui['language'])}">
        <a{en_current} href="{paths['en']}" hreflang="en" lang="en">EN</a>
        <a{ar_current} href="{paths['ar']}" hreflang="ar" lang="ar" aria-label="العربية">ع</a>
      </div>
      {cta}
      <button class="burger" type="button" id="burger" aria-controls="nav-links" aria-expanded="false" aria-label="{qa(ui['menu'])}"><span></span><span></span><span></span></button>
    </div>
  </div>
</header>"""


def footer_html(ctx: dict, lang: str, pages: list[dict]) -> str:
    ui = sc.UI[lang]
    links = "\n".join(f'      <li><a href="{path(lang, p["slug"])}">{esc(link_label(p, lang))}</a></li>' for p in pages)
    tag_a, tag_b = ui["footer_tag"]
    login_link = f'\n          <li><a href="{sc.ONE_APP_URL}">{esc(sc.ONE[lang]["footer_login"])}</a></li>' if sc.ONE_APP_URL else ""
    social = "\n".join(f'          <li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in ctx["SOCIAL_LINKS"])
    return f"""<footer class="footer">
  <div class="container">
    <div class="footer-grid">
      <div>
        <a href="{home_path(lang)}" class="brand" aria-label="H.M Media"><svg class="brand-mark"><use href="#i-logo"/></svg><span>H.M Media</span></a>
        <p class="footer-tag">{esc(tag_a)} <span class="grad">{esc(tag_b)}</span></p>
        <p class="footer-loc">{esc(ui['footer_loc'])}</p>
      </div>
      <div>
        <h3 class="footer-h">{esc(ui['footer_explore'])}</h3>
        <ul>
          <li><a href="{LANG_PREFIX[lang]}/work/">{esc(sc.WORK[lang]['nav'])}</a></li>
          <li><a href="{LANG_PREFIX[lang]}/one/">H.M One</a></li>
          <li><a href="{LANG_PREFIX[lang]}/about/">{esc(sc.ABOUT[lang]['nav'])}</a></li>
          <li><a href="{home_path(lang, '#faq')}">{esc(ui['footer_faq'])}</a></li>
        </ul>
      </div>
      <div>
        <h3 class="footer-h">{esc(ui['footer_follow'])}</h3>
        <ul>
{social}
        </ul>
      </div>
      <div>
        <h3 class="footer-h">{esc(ui['footer_contact'])}</h3>
        <ul>
          <li><a href="{qa(wa_link(ctx, ui['wa_talk'].format(source='Footer' if lang == 'en' else 'أسفل الموقع')))}" target="_blank" rel="noopener">{esc(ui['whatsapp'])}</a></li>
          <li><a href="mailto:{ctx['EMAIL']}">{esc(ui['email'])}</a></li>{login_link}
        </ul>
      </div>
    </div>
    <nav class="footer-services" aria-label="{qa(ui['footer_services'])}">
      <h3 class="footer-h">{esc(ui['footer_services'])}</h3>
      <ul>
{links}
      </ul>
    </nav>
    <div class="footer-bottom">
      <p>© {ctx['year']} {esc(ui['rights'])} · <a class="footer-credit" href="{ctx['FOUNDER']['url']}" target="_blank" rel="noopener">{esc(ui['founder'])}</a></p>
      <a href="#top">{esc(ui['back_top'])}</a>
    </div>
  </div>
</footer>"""


def talk_html(ctx: dict, lang: str, source: str) -> str:
    ui = sc.UI[lang]
    a, b = ui["talk_h"]
    return f"""<section class="section talk-section" id="talk">
  <div class="container">
    <div class="talk-band talk-band--static">
      <div class="talk-band-copy">
        <h2 class="h2">{esc(a)} <span class="grad">{esc(b)}</span></h2>
        <p class="lead">{esc(ui['talk_lead'])}</p>
        <div class="talk">
          <a class="talk-btn" href="{qa(wa_link(ctx, ui['wa_talk'].format(source=source)))}" target="_blank" rel="noopener">
            <span class="talk-ic" aria-hidden="true"><svg><use href="#i-wa"/></svg></span>
            <span class="talk-text"><b>{esc(ui['talk_btn'])}</b><small>{esc(ui['talk_small'])}</small></span>
            <span class="arr" aria-hidden="true">→</span>
          </a>
        </div>
      </div>
    </div>
  </div>
</section>"""


# ------------------------------------------------------------------------------------ head + structured data
def head_common(ctx: dict, lang: str, *, title: str, description: str, en_path: str, ar_path: str, graph: list) -> str:
    """Shared <head> for the generated pages: meta, canonical, hreflang, Open Graph, icons and JSON-LD."""
    SITE = ctx["SITE"]
    url = SITE + (en_path if lang == "en" else ar_path)
    other = "ar" if lang == "en" else "en"
    other_url = SITE + (ar_path if lang == "en" else en_path)
    og_image = f"{SITE}/assets/img/og-{lang}.jpg"
    data = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=2).replace("</", "<\\/")
    lines = [
        '<meta charset="UTF-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">',
        f"<title>{esc(title)}</title>",
        f'<meta name="description" content="{qa(description)}">',
        '<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">',
        '<meta name="theme-color" content="#060706">',
        f'<link rel="canonical" href="{url}">',
        f'<link rel="alternate" hreflang="{lang}" href="{url}">',
        f'<link rel="alternate" hreflang="{other}" href="{other_url}">',
        f'<link rel="alternate" hreflang="x-default" href="{SITE + en_path}">',
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{ctx["BRAND"]}">',
        f'<meta property="og:title" content="{qa(title)}">',
        f'<meta property="og:description" content="{qa(description)}">',
        f'<meta property="og:url" content="{url}">',
        f'<meta property="og:locale" content="{ctx["OG_LOCALE"][lang]}">',
        f'<meta property="og:locale:alternate" content="{ctx["OG_LOCALE"][other]}">',
        f'<meta property="og:image" content="{og_image}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        '<meta name="twitter:card" content="summary_large_image">',
        f'<meta name="twitter:title" content="{qa(title)}">',
        f'<meta name="twitter:description" content="{qa(description)}">',
        f'<meta name="twitter:image" content="{og_image}">',
        '<link rel="icon" href="/favicon.svg" type="image/svg+xml">',
        '<link rel="icon" href="/favicon-96.png" type="image/png" sizes="96x96">',
        '<link rel="apple-touch-icon" href="/apple-touch-icon.png">',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        f'<link href="{ctx["FONTS_URL"]}" rel="stylesheet">',
        f'<link rel="stylesheet" href="/{asset_version("assets/css/style.css")}">',
        '<script type="application/ld+json">',
        data,
        "</script>",
        f'<script src="/{asset_version("assets/js/service.js")}" defer></script>',
    ]
    return "\n".join(lines)


def head_html(ctx: dict, lang: str, p: dict, faqs: list[dict]) -> str:
    SITE = ctx["SITE"]
    ui = sc.UI[lang]
    url = SITE + path(lang, p["slug"])
    title = f"{p['title'][lang]} | {ctx['BRAND']}"
    description = p["description"][lang]
    other = "ar" if lang == "en" else "en"
    og_image = f"{SITE}/assets/img/og-{lang}.jpg"
    org_ref = {"@id": ctx["ORG_ID"]}
    crumb_group = ui["crumb_ai"] if p["kind"] == "ai" else ui["crumb_agency"]
    crumb_anchor = "#ai" if p["kind"] == "ai" else "#agency"

    if p["kind"] == "ai":
        amount, unit = _PRICE_PARSER(p["service"]["price"]["en"])
        offers = [{"@type": "Offer", "url": url, "priceCurrency": "AED", **({"priceSpecification": {"@type": "UnitPriceSpecification", "priceCurrency": "AED", "minPrice": amount, **({"unitCode": unit} if unit else {})}} if amount is not None else {})}]
        service_node = {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": p["label"][lang],
            "description": p["intro"][lang],
            "serviceType": ui["crumb_ai"],
            "provider": org_ref,
            "areaServed": ctx["AREA_SERVED"],
            "url": url,
            "offers": offers[0],
        }
    else:
        offer_items = []
        for s in p["items"]:
            amount, unit = _PRICE_PARSER(s["price"]["en"])
            offer = {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["title"][lang], "provider": org_ref}, "priceCurrency": "AED"}
            if amount is not None:
                offer["priceSpecification"] = {"@type": "UnitPriceSpecification", "priceCurrency": "AED", "minPrice": amount, **({"unitCode": unit} if unit else {})}
            offer_items.append(offer)
        service_node = {
            "@type": "Service",
            "@id": f"{url}#service",
            "name": p["title"][lang],
            "description": p["intro"][lang],
            "serviceType": ui["crumb_agency"],
            "provider": org_ref,
            "areaServed": ctx["AREA_SERVED"],
            "url": url,
            "hasOfferCatalog": {"@type": "OfferCatalog", "name": p["label"][lang], "itemListElement": offer_items},
        }

    graph = [
        {"@type": ["Organization", "ProfessionalService"], "@id": ctx["ORG_ID"], "name": ctx["BRAND"], "url": SITE + "/"},
        service_node,
        {
            "@type": "WebPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": title,
            "description": description,
            "inLanguage": lang,
            "isPartOf": {"@id": ctx["WEBSITE_ID"]},
            "about": {"@id": f"{url}#service"},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": ctx["BRAND"], "item": SITE + home_path(lang)},
                {"@type": "ListItem", "position": 2, "name": crumb_group, "item": SITE + home_path(lang, crumb_anchor)},
                {"@type": "ListItem", "position": 3, "name": p["label"][lang], "item": url},
            ],
        },
        {
            "@type": "FAQPage",
            "@id": f"{url}#faq",
            "inLanguage": lang,
            "mainEntity": [{"@type": "Question", "name": f["q"][lang], "acceptedAnswer": {"@type": "Answer", "text": f["a"][lang]}} for f in faqs],
        },
    ]
    return head_common(ctx, lang, title=title, description=description, en_path=path("en", p["slug"]), ar_path=path("ar", p["slug"]), graph=graph)


# ------------------------------------------------------------------------------------ page body
def tick_list(items: list[str]) -> str:
    return "<ul class=\"tick-list\">" + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"


def card_text(p: dict, lang: str) -> str:
    """One short line for a service card: the home-page blurb, or the first sentence of a category intro."""
    if p["kind"] == "ai" and p["service"]["desc"]:
        return p["service"]["desc"][lang]
    intro = p["intro"][lang]
    cut = intro.find(". ") if lang == "en" else intro.find(" لكل خدمة")
    return intro[: cut + 1].strip() if cut > 0 and lang == "en" else (intro[:cut].strip() if cut > 0 else intro)


def related_html(ctx: dict, lang: str, p: dict, by_slug: dict) -> str:
    ui = sc.UI[lang]
    cards = []
    for slug in p.get("related", []):
        other = by_slug.get(slug)
        if not other:
            continue
        cards.append(
            f'<a class="card rel-card" href="{path(lang, slug)}"><h3>{esc(other["label"][lang])}</h3>'
            f'<p>{esc(card_text(other, lang))}</p><span class="more" aria-hidden="true">→</span></a>'
        )
    if not cards:
        return ""
    return f"""<section class="section section--tight" aria-labelledby="related-h">
  <div class="container">
    <h2 class="svc-h2" id="related-h">{esc(ui['related'])}</h2>
    <div class="rel-grid">{''.join(cards)}</div>
  </div>
</section>"""


def body_html(ctx: dict, lang: str, p: dict, faqs: list[dict], by_slug: dict) -> str:
    ui = sc.UI[lang]
    a, b = p["h1"][lang]
    crumb_group = ui["crumb_ai"] if p["kind"] == "ai" else ui["crumb_agency"]
    crumb_anchor = "#ai" if p["kind"] == "ai" else "#agency"
    eyebrow = ui["eyebrow_ai"] if p["kind"] == "ai" else ui["eyebrow_agency"]
    source = f"{p['label'][lang]} {ui['page_word']}"
    start = price_of(p, lang)

    if p["kind"] == "ai":
        message = ui["wa_msg"].format(title=p["label"][lang], price=f" ({start})", source=source)
        hero_cta = f"""<div class="svc-hero-cta">
      <div class="price-chip"><small>{esc(ui['starting_from'])}</small><strong>{esc(start)}</strong></div>
      <a class="btn btn-accent" href="{qa(wa_link(ctx, message))}" target="_blank" rel="noopener"><svg class="ic"><use href="#i-wa"/></svg> <span>{esc(ui['request'])}</span></a>
    </div>"""
        details = f"""<section class="section section--tight">
  <div class="container svc-cols">
    <div class="card svc-col"><h2>{esc(ui['gets'])}</h2>{tick_list(p['gets'][lang])}</div>
    <div class="card svc-col"><h2>{esc(ui['good_for'])}</h2>{tick_list(p['good_for'][lang])}</div>
  </div>
</section>"""
    else:
        rows = []
        for s in p["items"]:
            message = ui["wa_msg"].format(title=s["title"][lang], price=f" ({s['price'][lang]})", source=source)
            rows.append(
                f'<li><a class="svc-row" href="{qa(wa_link(ctx, message))}" target="_blank" rel="noopener">'
                f'<span>{esc(s["title"][lang])}</span><span class="svc-row-price">{esc(s["price"][lang])}</span></a></li>'
            )
        message = ui["wa_msg_group"].format(title=p["label"][lang], source=source)
        hero_cta = f"""<div class="svc-hero-cta">
      <div class="price-chip"><small>{esc(ui['starting_from'])}</small><strong>{esc(start)}</strong></div>
      <a class="btn btn-accent" href="{qa(wa_link(ctx, message))}" target="_blank" rel="noopener"><svg class="ic"><use href="#i-wa"/></svg> <span>{esc(ui['request'])}</span></a>
    </div>"""
        details = f"""<section class="section section--tight">
  <div class="container">
    <div class="card svc-col svc-col--wide"><h2>{esc(ui['included'])}</h2><ul class="svc-list">{''.join(rows)}</ul></div>
  </div>
</section>"""

    steps = "".join(
        f'<li class="card step"><span class="step-num">0{i}</span><h3 class="step-title">{esc(t)}</h3><p class="step-text">{esc(d)}</p></li>'
        for i, (t, d) in enumerate(ui["steps"], 1)
    )
    how_a, how_b = ui["how_h"]
    faq_a, faq_b = ui["faq_h"]
    faq_items = "".join(
        f'<details class="faq-item"><summary><span>{esc(f["q"][lang])}</span><span class="faq-plus" aria-hidden="true"></span></summary><p class="faq-a">{esc(f["a"][lang])}</p></details>'
        for f in faqs
    )
    return f"""<main id="top">
<section class="svc-hero">
  <div class="container">
    <nav class="crumbs" aria-label="{qa(ui['breadcrumb'])}">
      <ol>
        <li><a href="{home_path(lang)}">{ctx['BRAND']}</a></li>
        <li><a href="{home_path(lang, crumb_anchor)}">{esc(crumb_group)}</a></li>
        <li aria-current="page">{esc(p['label'][lang])}</li>
      </ol>
    </nav>
    <span class="eyebrow">{esc(eyebrow)}</span>
    <h1 class="svc-h1">{esc(a)} <span class="grad">{esc(b)}</span></h1>
    <p class="svc-intro">{esc(p['intro'][lang])}</p>
    {hero_cta}
  </div>
</section>

{details}

<section class="section section--tight" id="process">
  <div class="container">
    <h2 class="svc-h2">{esc(how_a)} <span class="grad">{esc(how_b)}</span></h2>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="section section--tight" id="faq">
  <div class="container">
    <h2 class="svc-h2">{esc(faq_a)} <span class="grad">{esc(faq_b)}</span></h2>
    <div class="faq-list svc-faq">{faq_items}</div>
  </div>
</section>

{related_html(ctx, lang, p, by_slug)}

{talk_html(ctx, lang, source)}
</main>"""


def render_page(ctx: dict, lang: str, p: dict, pages: list[dict]) -> str:
    ui = sc.UI[lang]
    by_slug = {x["slug"]: x for x in pages}
    faqs = faq_list(ctx, p, lang)
    # faq_list returns bilingual items; head_html/body_html pick the language they need.
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{ui['dir']}">
<head>
{head_html(ctx, lang, p, faqs)}
</head>
<body>

{ctx['sprite']}

{header_html(ctx, lang, p['slug'])}

{body_html(ctx, lang, p, faqs, by_slug)}

{footer_html(ctx, lang, pages)}

</body>
</html>
"""


def about_path(lang: str) -> str:
    return f"{LANG_PREFIX[lang]}/about/"


def render_about(ctx: dict, lang: str, pages: list[dict]) -> str:
    ui = sc.UI[lang]
    a = sc.ABOUT[lang]
    SITE = ctx["SITE"]
    url = SITE + about_path(lang)
    founder = ctx["FOUNDER"]
    h1_a, h1_b = a["h1"]
    how_a, how_b = ui["how_h"]

    def link_list(kind: str) -> str:
        items = "".join(f'<li><a href="{path(lang, p["slug"])}">{esc(p["label"][lang])}</a></li>' for p in pages if p["kind"] == kind)
        return f'<ul class="link-list">{items}</ul>'

    steps = "".join(
        f'<li class="card step"><span class="step-num">0{i}</span><h3 class="step-title">{esc(t)}</h3><p class="step-text">{esc(d)}</p></li>'
        for i, (t, d) in enumerate(ui["steps"], 1)
    )
    wa = qa(wa_link(ctx, ui["wa_talk"].format(source=a["source"])))
    contact = (
        f'<li><a href="{wa}" target="_blank" rel="noopener">{esc(a["phone"])}: <bdi dir="ltr">{esc(ctx["PHONE_DISPLAY"])}</bdi></a></li>'
        f'<li><a href="mailto:{ctx["EMAIL"]}">{esc(a["email"])}: <bdi dir="ltr">{ctx["EMAIL"]}</bdi></a></li>'
        + "".join(f'<li><a href="{u}" target="_blank" rel="noopener">{esc(n)}</a></li>' for n, u in ctx["SOCIAL_LINKS"])
    )

    graph = [
        {"@type": ["Organization", "ProfessionalService"], "@id": ctx["ORG_ID"], "name": ctx["BRAND"], "url": SITE + "/", "founder": {"@id": founder["id"]}},
        {"@type": "Person", "@id": founder["id"], "name": founder["name"], "alternateName": founder["name_ar"], "url": founder["url"], "jobTitle": "Multimedia Lead & Creative Technologist"},
        {
            "@type": "AboutPage",
            "@id": f"{url}#webpage",
            "url": url,
            "name": a["title"],
            "description": a["description"],
            "inLanguage": lang,
            "isPartOf": {"@id": ctx["WEBSITE_ID"]},
            "about": {"@id": ctx["ORG_ID"]},
            "breadcrumb": {"@id": f"{url}#breadcrumb"},
        },
        {
            "@type": "BreadcrumbList",
            "@id": f"{url}#breadcrumb",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": ctx["BRAND"], "item": SITE + home_path(lang)},
                {"@type": "ListItem", "position": 2, "name": a["label"], "item": url},
            ],
        },
    ]
    head = head_common(ctx, lang, title=a["title"], description=a["description"], en_path=about_path("en"), ar_path=about_path("ar"), graph=graph)
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{ui['dir']}">
<head>
{head}
</head>
<body>

{ctx['sprite']}

{header_html(ctx, lang, "about", alt_paths={"en": about_path("en"), "ar": about_path("ar")})}

<main id="top">
<section class="svc-hero">
  <div class="container">
    <nav class="crumbs" aria-label="{qa(ui['breadcrumb'])}">
      <ol>
        <li><a href="{home_path(lang)}">{ctx['BRAND']}</a></li>
        <li aria-current="page">{esc(a['label'])}</li>
      </ol>
    </nav>
    <span class="eyebrow">{esc(a['label'])}</span>
    <h1 class="svc-h1">{esc(h1_a)} <span class="grad">{esc(h1_b)}</span></h1>
    <p class="svc-intro">{esc(a['intro'])}</p>
    <div class="svc-hero-cta">
      <a class="btn btn-accent" href="{wa}" target="_blank" rel="noopener"><svg class="ic"><use href="#i-wa"/></svg> <span>{esc(ui['talk_btn'])}</span></a>
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container svc-cols">
    <div class="card svc-col"><h2>{esc(a['ai_h'])}</h2>{link_list('ai')}</div>
    <div class="card svc-col"><h2>{esc(a['agency_h'])}</h2>{link_list('group')}</div>
  </div>
</section>

<section class="section section--tight" id="process">
  <div class="container">
    <h2 class="svc-h2">{esc(how_a)} <span class="grad">{esc(how_b)}</span></h2>
    <ol class="steps">{steps}</ol>
  </div>
</section>

<section class="section section--tight">
  <div class="container svc-cols">
    <div class="card svc-col"><h2>{esc(a['where_h'])}</h2><p class="svc-text">{esc(a['where'])}</p></div>
    <div class="card svc-col" id="founder"><h2>{esc(a['founder_h'])}</h2><p class="svc-text">{esc(a['founder'])}</p><p class="svc-text"><a class="text-link" href="{founder['url']}" target="_blank" rel="noopener">{esc(a['founder_link'])} →</a></p></div>
  </div>
</section>

<section class="section section--tight" id="contact">
  <div class="container">
    <div class="card svc-col svc-col--wide"><h2>{esc(a['contact_h'])}</h2><ul class="link-list">{contact}</ul><p class="svc-text">{esc(a['reply'])}</p></div>
  </div>
</section>

{talk_html(ctx, lang, a['source'])}
</main>

{footer_html(ctx, lang, pages)}

</body>
</html>
"""


def page_shell(ctx: dict, lang: str, head: str, slug: str, main: str, pages: list[dict]) -> str:
    ui = sc.UI[lang]
    alt = {"en": f"/{slug}/", "ar": f"/ar/{slug}/"}
    return f"""<!DOCTYPE html>
<html lang="{lang}" dir="{ui['dir']}">
<head>
{head}
</head>
<body>

{ctx['sprite']}

{header_html(ctx, lang, slug, alt_paths=alt)}

{main}

{footer_html(ctx, lang, pages)}

</body>
</html>
"""


def crumbs_html(ctx: dict, lang: str, label: str) -> str:
    ui = sc.UI[lang]
    return f"""<nav class="crumbs" aria-label="{qa(ui['breadcrumb'])}">
      <ol>
        <li><a href="{home_path(lang)}">{ctx['BRAND']}</a></li>
        <li aria-current="page">{esc(label)}</li>
      </ol>
    </nav>"""


def breadcrumb_node(ctx: dict, lang: str, url: str, label: str) -> dict:
    return {
        "@type": "BreadcrumbList",
        "@id": f"{url}#breadcrumb",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ctx["BRAND"], "item": ctx["SITE"] + home_path(lang)},
            {"@type": "ListItem", "position": 2, "name": label, "item": url},
        ],
    }


# Line icons (24x24, stroke) for the H.M One page. Every path carries pathLength="1" so the stroke can be drawn in with CSS.
ONE_ICONS = {
    "hr": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6"/><circle cx="17.5" cy="9" r="2.3"/><path d="M16.5 14.2c2.6.3 4.5 2.5 4.5 5.3"/>',
    "attendance": '<rect x="3.5" y="5" width="17" height="15.5" rx="3"/><path d="M8 3v4M16 3v4M3.5 10h17"/><path d="M8.5 15l2.4 2.4 4.6-4.6"/>',
    "payroll": '<rect x="2.5" y="6" width="19" height="12" rx="2.5"/><circle cx="12" cy="12" r="2.6"/><path d="M6 9.5v5M18 9.5v5"/>',
    "facility": '<path d="M4 21V5.5A1.5 1.5 0 0 1 5.500 4h7A1.5 1.5 0 0 1 14 5.5V21"/><path d="M14 10h4.5A1.5 1.5 0 0 1 20 11.5V21M2.5 21h19"/><path d="M7.5 8h3M7.5 12h3M7.5 16h3"/>',
    "assets": '<path d="M3 12.200V5a2 2 0 0 1 2-2h7.200a2 2 0 0 1 1.400.600l7 7a2 2 0 0 1 0 2.800l-7.200 7.200a2 2 0 0 1-2.800 0l-7-7A2 2 0 0 1 3 12.200z"/><circle cx="8" cy="8" r="1.500"/>',
    "maintenance": '<path d="M14.500 6.200a4.200 4.200 0 0 0 5.300 5.300l-9.600 9.600a2.300 2.300 0 0 1-3.300-3.300z"/><path d="M14.500 6.200L17.300 3.400a4.200 4.200 0 0 0-5.600 5.600"/><path d="M19.800 11.500a4.200 4.200 0 0 0 .800-4.800L18 9.300"/>',
    "procurement": '<path d="M2.500 4h2.700l2.300 11h10.300l2-8H6.300"/><circle cx="9" cy="19" r="1.500"/><circle cx="17" cy="19" r="1.500"/>',
    "inventory": '<path d="M12 3l8 4.200v9.600L12 21l-8-4.200V7.200z"/><path d="M4 7.200l8 4.200 8-4.200M12 11.400V21"/><path d="M8 5.100l8 4.200"/>',
    "finance": '<path d="M4 20V4M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/><path d="M7 7.500l4-3 3 2 5-3.500"/>',
    "lock": '<rect x="4.500" y="10.500" width="15" height="10" rx="2.500"/><path d="M8 10.500V7.500a4 4 0 0 1 8 0v3"/>',
    "puzzle": '<path d="M9 4h3a2 2 0 1 1 4 0h3a1 1 0 0 1 1 1v4a2 2 0 1 0 0 4v6a1 1 0 0 1-1 1h-5a2 2 0 1 0-4 0H5a1 1 0 0 1-1-1v-5a2 2 0 1 0 0-4V5a1 1 0 0 1 1-1z"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.800 2.500 2.800 15.500 0 18M12 3c-2.800 2.500-2.800 15.500 0 18"/>',
    "shield": '<path d="M12 3l7.500 2.800v5.700c0 4.500-3.100 8-7.500 9.500-4.400-1.500-7.500-5-7.500-9.500V5.800z"/><path d="M8.800 12l2.300 2.300 4.200-4.300"/>',
}


def one_icon(name: str) -> str:
    body = ONE_ICONS[name].replace("<path ", '<path pathLength="1" ').replace("<circle ", '<circle pathLength="1" ').replace("<rect ", '<rect pathLength="1" ')
    return f'<svg class="one-ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>'


# Every Solution and every function it performs, extracted from the platform's code (see tools/one_features.json).
# "limits" in that file (partial or setup-required work) are deliberately not published as features.
ONE_FEATURES = json.loads((ROOT / "tools" / "one_features.json").read_text(encoding="utf-8"))["solutions"]
ONE_SOLUTION_ICON = {"platform": "shield"}


def solution_icon(sol: dict) -> str:
    return one_icon(ONE_SOLUTION_ICON.get(sol["slug"], sol["slug"]))


def solution_count(sol: dict) -> int:
    return sum(len(g["items"]) for g in sol["groups"])


def solution_path(lang: str, sol: dict) -> str:
    return f"{LANG_PREFIX[lang]}/one/{sol['slug']}/"


LOGIN_ICON = ('<svg class="ic" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
              '<path d="M14 4h4a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2h-4"/><path d="M10 16l4-4-4-4M14 12H4"/></svg>')
# Real screens of the platform (taken from a demo workspace with sample data): file name, English name, Arabic name.
ONE_SCREENS = [
    ("workspace", "Company workspace", "مساحة عمل الشركة"),
    ("hr", "People map", "خريطة الموظفين"),
    ("reports", "Executive reports", "التقارير التنفيذية"),
    ("finance", "Finance and billing", "المالية والفوترة"),
    ("operations-work-orders", "Work orders", "أوامر العمل"),
]

ONE_LOGO = '<img src="/assets/img/hm-one-logo.svg" width="1014" height="614" alt="H.M One">'


def portal_html(lang: str) -> str:
    """The customer entrance to the platform: shown only on the H.M One page, once the platform has an address."""
    if not sc.ONE_APP_URL:
        return ""
    o = sc.ONE[lang]
    a, b = o["portal_h"]
    return f"""<section class="section section--tight" id="login">
  <div class="container">
    <div class="portal rv">
      <div class="portal-in">
        <div class="portal-gate" aria-hidden="true"><i></i><i></i><i></i><span>{LOGIN_ICON}</span></div>
        <div class="portal-copy">
          <span class="eyebrow">{esc(o['portal_eyebrow'])}</span>
          <h2 class="svc-h2">{esc(a)} <span class="grad">{esc(b)}</span></h2>
        </div>
        <a class="btn btn-accent btn-lg portal-btn" href="{sc.ONE_APP_URL}">{LOGIN_ICON} <span>{esc(o['cta_login'])}</span> <span class="arr" aria-hidden="true">→</span></a>
      </div>
    </div>
  </div>
</section>"""


def render_one(ctx: dict, lang: str, pages: list[dict]) -> str:
    ui = sc.UI[lang]
    o = sc.ONE[lang]
    SITE = ctx["SITE"]
    url = f"{SITE}{LANG_PREFIX[lang]}/one/"
    h1_a, h1_b = o["h1"]
    sol_a, sol_b = o["solutions_h"]
    cus_a, cus_b = o["custom_short_h"]
    faq_a, faq_b = ui["faq_h"]
    wa_ready = qa(wa_link(ctx, o["wa_ready"]))
    wa_custom = qa(wa_link(ctx, o["wa_custom"]))
    buttons = f"""<div class="svc-hero-cta">
      <a class="btn btn-accent btn-lg" href="{wa_ready}" target="_blank" rel="noopener"><svg class="ic"><use href="#i-wa"/></svg> <span>{esc(o['cta_ready'])}</span></a>
      <a class="btn btn-ghost btn-lg" href="{wa_custom}" target="_blank" rel="noopener">{esc(o['cta_custom'])}</a>
    </div>"""
    portal = portal_html(lang)
    name_at = 1 if lang == "en" else 2
    screens = "".join(
        f'<figure class="screen"><img src="/assets/one/{shot[0]}.webp" width="1600" height="1000" loading="lazy" alt="{qa(o["screen_alt"].format(name=shot[name_at]))}">'
        f'<figcaption>{esc(shot[name_at])}</figcaption></figure>'
        for shot in ONE_SCREENS
    )
    scr_a, scr_b = o["screens_h"]
    cards = "".join(
        f'<article class="card sol rv" style="--d:{i % 3}">'
        f'<span class="sol-ic">{solution_icon(sol)}</span><h3>{esc(sol["name"][lang])}</h3>'
        f'<ul class="sol-list">{"".join(f"<li>{esc(h[lang])}</li>" for h in sol["highlights"])}</ul>'
        f'<a class="sol-more" href="{solution_path(lang, sol)}"><span>{esc(o["all_functions"].format(n=solution_count(sol)))}</span> <span class="arr" aria-hidden="true">→</span></a>'
        f'</article>'
        for i, sol in enumerate(ONE_FEATURES)
    )
    pills = "".join(f'<li class="pill rv" style="--d:{i}">{one_icon(icon)}<span>{esc(label)}</span></li>' for i, (icon, label) in enumerate(o["pills"]))
    faq_items = "".join(
        f'<details class="faq-item"><summary><span>{esc(q)}</span><span class="faq-plus" aria-hidden="true"></span></summary><p class="faq-a">{esc(a)}</p></details>'
        for q, a in o["faq"]
    )
    app = {
        "@type": "SoftwareApplication",
        "@id": f"{SITE}/one/#software",
        "name": "H.M One",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "Web",
        "description": o["description"],
        "image": f"{SITE}/assets/img/hm-one-logo.png",
        "inLanguage": ["en", "ar"],
        "provider": {"@id": ctx["ORG_ID"]},
        "publisher": {"@id": ctx["ORG_ID"]},
        "featureList": [f"{sol['name'][lang]}: {sol['summary'][lang]}" for sol in ONE_FEATURES],
        "url": url,
    }
    graph = [
        {"@type": ["Organization", "ProfessionalService"], "@id": ctx["ORG_ID"], "name": ctx["BRAND"], "url": SITE + "/"},
        app,
        {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": o["title"], "description": o["description"], "inLanguage": lang,
         "isPartOf": {"@id": ctx["WEBSITE_ID"]}, "about": {"@id": app["@id"]}, "breadcrumb": {"@id": f"{url}#breadcrumb"}},
        breadcrumb_node(ctx, lang, url, o["label"]),
        {"@type": "FAQPage", "@id": f"{url}#faq", "inLanguage": lang,
         "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in o["faq"]]},
    ]
    head = head_common(ctx, lang, title=o["title"], description=o["description"], en_path="/one/", ar_path="/ar/one/", graph=graph)
    main = f"""<main id="top">
<section class="svc-hero one-hero">
  <div class="container one-hero-copy">
    {crumbs_html(ctx, lang, o['label'])}
    <div class="one-hero-logo">{ONE_LOGO}</div>
    <h1 class="svc-h1"><span class="sr-only">H.M One: </span>{esc(h1_a)} <span class="grad">{esc(h1_b)}</span></h1>
    <p class="svc-intro">{esc(o['tagline'])}</p>
    {buttons}
  </div>
  <div class="container">
    <div class="mockup" aria-hidden="true">
      <div class="mockup-bar"><i></i><i></i><i></i><span>one.h-m.agency</span></div>
      <img src="/assets/one/operations.webp" width="1600" height="1000" alt="" fetchpriority="high">
    </div>
  </div>
</section>

<section class="section section--tight">
  <div class="container"><ul class="pills">{pills}</ul></div>
</section>

<section class="section section--tight" id="screens">
  <div class="container"><h2 class="svc-h2">{esc(scr_a)} <span class="grad">{esc(scr_b)}</span></h2></div>
  <div class="screens" role="group" aria-label="{qa(o['screens_label'])}" tabindex="0">{screens}</div>
</section>

<section class="section section--tight" id="solutions">
  <div class="container">
    <h2 class="svc-h2">{esc(sol_a)} <span class="grad">{esc(sol_b)}</span></h2>
    <p class="svc-lead">{esc(o['solutions_hint'])}</p>
    <div class="sol-grid">{cards}</div>
  </div>
</section>

<section class="section section--tight" id="custom">
  <div class="container">
    <div class="card custom-band rv">
      <div><h2 class="svc-h2">{esc(cus_a)} <span class="grad">{esc(cus_b)}</span></h2><p class="svc-lead">{esc(o['custom_short'])}</p></div>
      <a class="btn btn-accent" href="{wa_custom}" target="_blank" rel="noopener"><span>{esc(o['cta_custom'])}</span> <span class="arr" aria-hidden="true">→</span></a>
    </div>
  </div>
</section>

{portal}

<section class="section section--tight" id="faq">
  <div class="container">
    <h2 class="svc-h2">{esc(faq_a)} <span class="grad">{esc(faq_b)}</span></h2>
    <div class="faq-list svc-faq">{faq_items}</div>
  </div>
</section>

<section class="section section--tight" id="start">
  <div class="container">
    <div class="card one-cta"><div class="one-cta-logo">{ONE_LOGO.replace('alt="H.M One"', 'alt=""')}</div>{buttons}</div>
  </div>
</section>
</main>"""
    return page_shell(ctx, lang, head, "one", main, pages)


def render_one_solution(ctx: dict, lang: str, sol: dict, pages: list[dict]) -> str:
    """A page for one Solution: every function it performs, grouped the way the product groups them."""
    ui = sc.UI[lang]
    o = sc.ONE[lang]
    SITE = ctx["SITE"]
    slug = f"one/{sol['slug']}"
    en_path, ar_path = f"/{slug}/", f"/ar/{slug}/"
    url = SITE + (en_path if lang == "en" else ar_path)
    one_url = f"{SITE}{LANG_PREFIX[lang]}/one/"
    name = sol["name"][lang]
    summary = sol["summary"][lang]
    count = solution_count(sol)
    fn_a, fn_b = o["functions_h"]
    oth_a, oth_b = o["others_h"]
    wa = qa(wa_link(ctx, o["wa_solution_page"].format(name=name)))
    buttons = f"""<div class="svc-hero-cta">
      <a class="btn btn-accent btn-lg" href="{wa}" target="_blank" rel="noopener"><svg class="ic"><use href="#i-wa"/></svg> <span>{esc(o['sol_request'])}</span></a>
      <a class="btn btn-ghost btn-lg" href="{LANG_PREFIX[lang]}/one/">{esc(o['all_solutions'])}</a>
    </div>"""
    highlights = "".join(f'<li class="pill">{esc(h[lang])}</li>' for h in sol["highlights"])
    jump = "".join(f'<li><a href="#g{i}">{esc(g["title"][lang])} <small>{len(g["items"])}</small></a></li>' for i, g in enumerate(sol["groups"], 1))
    groups = "".join(
        f'<section class="card fn-group rv" id="g{i}"><h3>{esc(g["title"][lang])} <small>{len(g["items"])}</small></h3>'
        f'<ul class="tick-list">{"".join(f"<li>{esc(item[lang])}</li>" for item in g["items"])}</ul></section>'
        for i, g in enumerate(sol["groups"], 1)
    )
    visual = sc.ONE_VISUALS[sol["slug"]]
    at = 0 if lang == "en" else 1
    flow_a, flow_b = o["flow_h"]
    area_a, area_b = o["areas_h"]
    scr_a, scr_b = o["screens_h"]
    hero_shot = visual["screens"][0]
    steps = "".join(
        f'<li class="flowline-step rv" style="--d:{i}"><span class="flowline-node">{i + 1}</span><span class="flowline-label">{esc(step[at])}</span></li>'
        for i, step in enumerate(visual["flow"])
    )
    stats = "".join(
        f'<li class="stat rv" style="--d:{i}"><b data-count="{value}">{value}</b><span>{esc(label)}</span></li>'
        for i, (value, label) in enumerate([(count, o["stat_functions"]), (len(sol["groups"]), o["stat_areas"]), (len(sol["roles"]), o["stat_roles"]), (2, o["stat_langs"])])
        if value
    )
    largest = max(len(g["items"]) for g in sol["groups"])
    bars = "".join(
        f'<li class="bar rv" style="--d:{i % 6}"><a href="#g{i}"><span class="bar-label">{esc(g["title"][lang])}</span>'
        f'<span class="bar-track"><i style="--w:{round(100 * len(g["items"]) / largest)}%"></i></span><b>{len(g["items"])}</b></a></li>'
        for i, g in enumerate(sol["groups"], 1)
    )
    screens = "".join(
        f'<figure class="screen"><img src="/assets/one/{shot[0]}.webp" width="1600" height="1000" loading="lazy" alt="{qa(o["screen_alt"].format(name=shot[1 + at]))}">'
        f'<figcaption>{esc(shot[1 + at])}</figcaption></figure>'
        for shot in visual["screens"]
    )
    # "Works with" lines start with the other Solution's name: turn those into linked cards with that Solution's icon.
    by_name = {other["name"][lang]: other for other in ONE_FEATURES}
    links = ""
    for w in sol["works_with"]:
        head, _, tail = w[lang].partition(":")
        other = by_name.get(head.strip())
        if other and tail:
            links += (f'<a class="card link-card rv" href="{solution_path(lang, other)}"><span class="sol-ic">{solution_icon(other)}</span>'
                      f'<span><b>{esc(other["name"][lang])}</b><small>{esc(tail.strip())}</small></span></a>')
        else:
            links += f'<div class="card link-card rv"><span class="sol-ic">{one_icon("puzzle")}</span><span><b>{esc(head.strip())}</b><small>{esc(tail.strip())}</small></span></div>'
    roles = "".join(f'<li>{one_icon("hr")}<span>{esc(r[lang])}</span></li>' for r in sol["roles"])
    extra = ""
    if False and sol["roles"]:
        extra += f'<div class="card svc-col"><h2>{esc(o["roles_h"])}</h2><ul class="role-list">{"".join(f"<li>{esc(r[lang])}</li>" for r in sol["roles"])}</ul></div>'
    if sol["works_with"]:
        extra += f'<div class="card svc-col"><h2>{esc(o["works_h"])}</h2>{tick_list([w[lang] for w in sol["works_with"]])}</div>'
    others = "".join(
        f'<a class="card sol sol--link" href="{solution_path(lang, other)}"><span class="sol-ic">{solution_icon(other)}</span>'
        f'<h3>{esc(other["name"][lang])}</h3><p>{esc(o["functions_count"].format(n=solution_count(other)))}</p></a>'
        for other in ONE_FEATURES if other["slug"] != sol["slug"]
    )
    app_id = f"{SITE}/one/#software"
    graph = [
        {"@type": ["Organization", "ProfessionalService"], "@id": ctx["ORG_ID"], "name": ctx["BRAND"], "url": SITE + "/"},
        {"@type": "SoftwareApplication", "@id": f"{url}#software", "name": f"H.M One: {name}", "applicationCategory": "BusinessApplication",
         "operatingSystem": "Web", "description": summary, "inLanguage": ["en", "ar"], "url": url,
         "isPartOf": {"@id": app_id}, "provider": {"@id": ctx["ORG_ID"]},
         "featureList": [item[lang] for g in sol["groups"] for item in g["items"]]},
        {"@type": "WebPage", "@id": f"{url}#webpage", "url": url, "name": o["sol_title"].format(name=name), "description": summary, "inLanguage": lang,
         "isPartOf": {"@id": ctx["WEBSITE_ID"]}, "about": {"@id": f"{url}#software"}, "breadcrumb": {"@id": f"{url}#breadcrumb"}},
        {"@type": "BreadcrumbList", "@id": f"{url}#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ctx["BRAND"], "item": SITE + home_path(lang)},
            {"@type": "ListItem", "position": 2, "name": "H.M One", "item": one_url},
            {"@type": "ListItem", "position": 3, "name": name, "item": url},
        ]},
    ]
    head = head_common(ctx, lang, title=o["sol_title"].format(name=name), description=summary, en_path=en_path, ar_path=ar_path, graph=graph)
    main = f"""<main id="top">
<section class="svc-hero sol-hero">
  <div class="container">
    <nav class="crumbs" aria-label="{qa(ui['breadcrumb'])}">
      <ol>
        <li><a href="{home_path(lang)}">{ctx['BRAND']}</a></li>
        <li><a href="{LANG_PREFIX[lang]}/one/">H.M One</a></li>
        <li aria-current="page">{esc(name)}</li>
      </ol>
    </nav>
    <div class="sol-hero-grid">
      <div>
        <div class="sol-hero-head">
          <span class="sol-ic sol-ic--xl">{solution_icon(sol)}</span>
          <div>
            <span class="eyebrow">H.M One · {esc(o['functions_count'].format(n=count))}</span>
            <h1 class="svc-h1">{esc(name)}</h1>
          </div>
        </div>
        <p class="svc-intro">{esc(summary)}</p>
        <ul class="pills pills--start">{highlights}</ul>
        {buttons}
      </div>
      <div class="mockup mockup--side" aria-hidden="true">
        <div class="mockup-bar"><i></i><i></i><i></i><span>one.h-m.agency</span></div>
        <img src="/assets/one/{hero_shot[0]}.webp" width="1600" height="1000" alt="" fetchpriority="high">
      </div>
    </div>
    <ul class="stats">{stats}</ul>
  </div>
</section>

<section class="section section--tight" id="flow">
  <div class="container">
    <h2 class="svc-h2">{esc(flow_a)} <span class="grad">{esc(flow_b)}</span></h2>
    <ol class="flowline" style="--n:{len(visual['flow'])}">{steps}</ol>
  </div>
</section>

<section class="section section--tight" id="screens">
  <div class="container"><h2 class="svc-h2">{esc(scr_a)} <span class="grad">{esc(scr_b)}</span></h2></div>
  <div class="screens{' screens--few' if len(visual['screens']) < 3 else ''}" role="group" aria-label="{qa(o['screens_label'])}" tabindex="0">{screens}</div>
</section>

<section class="section section--tight" id="areas">
  <div class="container">
    <h2 class="svc-h2">{esc(area_a)} <span class="grad">{esc(area_b)}</span></h2>
    <ul class="bars">{bars}</ul>
  </div>
</section>

<section class="section section--tight" id="functions">
  <div class="container">
    <h2 class="svc-h2">{esc(fn_a)} <span class="grad">{esc(fn_b)}</span></h2>
    <div class="fn-grid">{groups}</div>
  </div>
</section>

{f'<section class="section section--tight" id="roles"><div class="container"><h2 class="svc-h2">{esc(o["roles_h"])}</h2><ul class="role-cards">{roles}</ul></div></section>' if roles else ''}

{f'<section class="section section--tight" id="works-with"><div class="container"><h2 class="svc-h2">{esc(o["works_h"])}</h2><div class="link-grid">{links}</div></div></section>' if links else ''}

<section class="section section--tight" id="other">
  <div class="container">
    <h2 class="svc-h2">{esc(oth_a)} <span class="grad">{esc(oth_b)}</span></h2>
    <div class="sol-grid sol-grid--small">{others}</div>
  </div>
</section>

<section class="section section--tight" id="start">
  <div class="container">
    <div class="card one-cta"><div class="one-cta-logo">{ONE_LOGO.replace('alt="H.M One"', 'alt=""')}</div>{buttons}</div>
  </div>
</section>
</main>"""
    return page_shell(ctx, lang, head, slug, main, pages)


WALL_ROW_HEIGHT = 240
WALL_VIDEOS = 3  # one auto-playing video card per row


def render_work(ctx: dict, lang: str, pages: list[dict]) -> str:
    w = sc.WORK[lang]
    SITE = ctx["SITE"]
    url = f"{SITE}{LANG_PREFIX[lang]}/work/"
    h1_a, h1_b = w["h1"]
    still_width = round(WALL_ROW_HEIGHT * 16 / 9)

    # The cards are a showcase only: they are not links.
    def image_card(src: str, width: int, alt: str, hidden: bool) -> str:
        extra = ' aria-hidden="true"' if hidden else ""
        return (f'<div class="wall-card"{extra}><img src="{src}" width="{width}" height="{WALL_ROW_HEIGHT}" loading="lazy" '
                f'alt="{"" if hidden else qa(alt)}"></div>')

    def video_card(n: int, vid: str, hidden: bool) -> str:
        extra = ' aria-hidden="true"' if hidden else f' role="img" aria-label="{qa(w["video_label"].format(n=n))}"'
        return (f'<div class="wall-card wall-video" data-video="{vid}"{extra}>'
                f'<img src="https://i.ytimg.com/vi/{vid}/hqdefault.jpg" width="{still_width}" height="{WALL_ROW_HEIGHT}" loading="lazy" alt="">'
                f'<span class="wall-live" aria-hidden="true"><svg><use href="#i-play"/></svg></span></div>')

    # Video stills and designs alternate, so the wall shows many clients and kinds of work.
    stills = [(f"/assets/home/wall-{n:02d}.webp", still_width, "") for n in range(1, HOME_WALL_STILLS + 1)]
    designs = [(d["thumb"], round(WALL_ROW_HEIGHT * d["w"] / d["h"]), w["design_alt"].format(n=n)) for n, d in enumerate(ctx["designs"], 1)]
    designs = designs[13:] + designs[:13]
    mixed = []
    for i in range(max(len(stills), len(designs))):
        mixed += stills[i:i + 1] + designs[i:i + 1]
    rows_html = []
    for r in range(3):
        items = mixed[r::3]

        def cards(hidden: bool) -> str:
            out = [image_card(src, width, alt, hidden) for src, width, alt in items]
            if r < WALL_VIDEOS and r < len(ctx["videos"]):
                out.insert(min(3, len(out)), video_card(r + 1, ctx["videos"][r], hidden))
            return "".join(out)
        rows_html.append(f'<div class="wall-row{" wall-row--rev" if r % 2 else ""}"><div class="wall-track" style="--t:{80 + r * 16}s">{cards(False)}{cards(True)}</div></div>')

    index = 0 if lang == "en" else 1
    fields = [f[index] for f in sc.WORK_FIELDS]
    rotator = json.dumps(fields, ensure_ascii=False)
    field_links = "".join(
        f'<li><a href="{qa(wa_link(ctx, w["wa_field"].format(field=field)))}" target="_blank" rel="noopener">{esc(field)}</a></li>'
        for field in fields
    ) + f'<li class="fields-more">{esc(w["more_fields"])}</li>'
    graph = [
        {"@type": ["Organization", "ProfessionalService"], "@id": ctx["ORG_ID"], "name": ctx["BRAND"], "url": SITE + "/"},
        {"@type": "CollectionPage", "@id": f"{url}#webpage", "url": url, "name": w["title"], "description": w["description"], "inLanguage": lang,
         "isPartOf": {"@id": ctx["WEBSITE_ID"]}, "about": {"@id": ctx["ORG_ID"]}, "breadcrumb": {"@id": f"{url}#breadcrumb"}},
        breadcrumb_node(ctx, lang, url, w["label"]),
    ]
    head = head_common(ctx, lang, title=w["title"], description=w["description"], en_path="/work/", ar_path="/ar/work/", graph=graph)
    main = f"""<main id="top">
<section class="svc-hero folio">
  <div class="container folio-copy">
    <h1 class="folio-h1">{esc(h1_a)} <span class="grad">{esc(h1_b)}</span></h1>
    <p class="svc-intro">{esc(w['intro'])}</p>
    <p class="looking">{esc(w['looking'])} <span class="looking-word" id="looking-word" data-words="{qa(rotator)}">{esc(fields[0])}</span>{"؟" if lang == "ar" else "?"}</p>
  </div>
  <div class="wall" role="group" aria-label="{qa(w['wall_label'])}">
    <div class="wall-plane">
      {''.join(rows_html)}
    </div>
    <a class="wall-cta" href="{qa(wa_link(ctx, w['wa_all']))}" target="_blank" rel="noopener">
      <span class="wall-cta-ring" aria-hidden="true"></span><span class="wall-cta-ring" aria-hidden="true"></span>
      <svg class="ic"><use href="#i-wa"/></svg> <span>{esc(w['cta'])}</span> <span class="arr" aria-hidden="true">→</span>
    </a>
  </div>
  <nav class="fields" aria-label="{qa(w['fields_label'])}">
    <ul class="fields-track">{field_links}</ul>
  </nav>
</section>
</main>"""
    return page_shell(ctx, lang, head, "work", main, pages)


def render_all(ctx: dict, parse_price) -> tuple[list[dict], dict]:
    """Returns (pages, {relative output path: html})."""
    global _PRICE_PARSER
    _PRICE_PARSER = parse_price
    pages = resolve_pages(ctx)
    outputs = {}
    for p in pages:
        for lang in ("en", "ar"):
            outputs[f"{LANG_PREFIX[lang].strip('/')}/services/{p['slug']}/index.html".lstrip("/")] = render_page(ctx, lang, p, pages)
    for lang in ("en", "ar"):
        outputs[f"{LANG_PREFIX[lang].strip('/')}/about/index.html".lstrip("/")] = render_about(ctx, lang, pages)
        outputs[f"{LANG_PREFIX[lang].strip('/')}/one/index.html".lstrip("/")] = render_one(ctx, lang, pages)
        for sol in ONE_FEATURES:
            outputs[f"{LANG_PREFIX[lang].strip('/')}/one/{sol['slug']}/index.html".lstrip("/")] = render_one_solution(ctx, lang, sol, pages)
        outputs[f"{LANG_PREFIX[lang].strip('/')}/work/index.html".lstrip("/")] = render_work(ctx, lang, pages)
    return pages, outputs
