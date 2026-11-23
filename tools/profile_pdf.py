"""Builds the company profile PDF: cover, services, then the whole portfolio, English and Arabic on every page.

    python3 tools/profile_pdf.py

Run it after changing services, prices or the portfolio, and commit the new PDF. It writes
assets/pdf/hm-media-company-profile.pdf, the file behind the "Company profile (PDF)" buttons.

The text is deliberately short: it does not repeat the website. Service names and starting prices
come from index.html and every row links to its page on the site. The portfolio is complete: every
design in tools/work_designs.json and every video in portfolio-videos.txt. Designs are laid out in
justified rows (each image keeps its own shape, rows fill the page width and the pages fill their
height), beauty and perfume work first and Ma Hawa last so no single client leads. Every design
opens full size on the site and every video opens on YouTube.

It needs Google Chrome (set CHROME to its path if it is not in a usual place) and an internet
connection for the web fonts and the YouTube thumbnails. build.py --check does not cover the PDF.
"""

from __future__ import annotations

import html
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import build  # noqa: E402  site constants and the index.html parser
import service_content as sc  # noqa: E402
import service_pages as sp  # noqa: E402

OUT = ROOT / "assets" / "pdf" / "hm-media-company-profile.pdf"
CHROME_CANDIDATES = [
    os.environ.get("CHROME", ""),
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "google-chrome",
    "chromium",
]

# Order of the designs (positions in tools/work_designs.json, 1 = first). Beauty and perfume lead
# (16 Khas Oud & Perfumes, 18 Purity Perfumes, 19 Omega Clinic); the rest follow the site's order,
# which already puts the Ma Hawa pieces (1-13) last.
DESIGNS_FIRST = [16, 18, 19]
MA_HAWA_DESIGNS = range(1, 14)
COVER_STILLS = [1, 3, 4, 5, 6, 7]  # assets/home/wall-NN.webp; wall-02 is Ma Hawa, so it is left out

# Page geometry in millimetres (A4 portrait).
CONTENT_W = 180.0      # 210 mm minus 15 mm margins
BODY_H = 247.0         # usable height below the page header
GAP = 2.2              # gap between tiles and rows
ROW_TARGETS = [t / 2 for t in range(64, 125)]  # 32 - 62 mm: target row heights tried for each page
TITLE_H = 21.0         # page title + note
SUB_H = 9.0            # "Designs" / "Videos" sub-heading
CLOSING_H = 30.0

TEXT = {
    "profile": ("Company Profile", "الملف التعريفي"),
    "slogan": ("We work hard and smart, together.", "نعمل بجد وذكاء معاً."),
    "intro": (
        "H.M Media is a creative agency in the UAE. Specialist designers, video makers and marketers "
        "work side by side with AI to deliver design, video, marketing, websites and smart solutions "
        "for brands across the GCC.",
        "H.M Media وكالة إبداعية في الإمارات. مصممون وصنّاع فيديو ومسوّقون متخصصون يعملون جنباً إلى جنب "
        "مع الذكاء الاصطناعي، لنقدّم التصميم والفيديو والتسويق والمواقع والحلول الذكية للعلامات التجارية في الخليج.",
    ),
    "services": ("Our services", "خدماتنا"),
    "agency": ("Creative agency", "الوكالة الإبداعية"),
    "ai": ("AI solutions", "حلول الذكاء الاصطناعي"),
    "from": ("Starting from", "يبدأ من"),
    "note": (
        "Every project gets an exact quote before work starts. Tap a service for its details on h-m.agency.",
        "تحصل على عرض سعر دقيق لكل مشروع قبل البدء. اضغط على أي خدمة لتفاصيلها على الموقع.",
    ),
    "work": ("Our work", "أعمالنا"),
    "work_note": (
        "Tap a design to open it full size, or a video to watch it.",
        "اضغط على أي تصميم لفتحه بالحجم الكامل، أو على أي فيديو لمشاهدته.",
    ),
    "designs": ("Designs", "تصاميم"),
    "videos": ("Videos & motion", "فيديو وموشن"),
    "more": ("More on h-m.agency", "المزيد على الموقع"),
    "portfolio": ("Portfolio", "أعمالنا"),
    "whatsapp": ("WhatsApp", "واتساب"),
    "source": ("Company profile PDF", "الملف التعريفي PDF"),
}


def e(text: str) -> str:
    return html.escape(text, quote=True)


# Chrome stores WebP images in a PDF losslessly, which makes the file huge, but passes JPEG through
# as is. So every site image goes in as a JPEG copy made with ffmpeg in a temporary folder.
JPEG_DIR: pathlib.Path | None = None


def image_uri(site_path: str) -> str:
    """file:// URI of a JPEG copy of a site image (site_path like /assets/work/design-01.webp)."""
    source = ROOT / urllib.parse.unquote(site_path).lstrip("/")
    if JPEG_DIR is None or source.suffix.lower() in (".jpg", ".jpeg") or not shutil.which("ffmpeg"):
        return source.as_uri()
    target = JPEG_DIR / (source.stem + ".jpg")
    if not target.exists():
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(source), "-vf", "format=yuvj420p",
                        "-q:v", "4", "-frames:v", "1", str(target)], check=True, stdin=subprocess.DEVNULL)
    return target.as_uri()


def bi(key: str, tag: str = "span", cls: str = "") -> str:
    """English (left) and Arabic (right) versions of one text, side by side."""
    en, ar = TEXT[key]
    c = f' class="{cls}"' if cls else ""
    return f'<div class="bi"><{tag}{c} lang="en">{e(en)}</{tag}><{tag}{c} lang="ar" dir="rtl">{e(ar)}</{tag}></div>'


def chrome_path() -> str:
    for candidate in CHROME_CANDIDATES:
        if candidate and (pathlib.Path(candidate).exists() or shutil.which(candidate)):
            return candidate
    raise SystemExit("profile_pdf: Google Chrome not found; set CHROME to its path")


def load() -> dict:
    source = (ROOT / "index.html").read_text(encoding="utf-8")
    page = build.PageParser(source)
    services = [s for s in page.services if s["title"] and s["price"]]
    groups: dict[str, dict] = {}
    for s in services:
        if s["group"]:
            groups.setdefault(s["group"]["en"], {"name": s["group"], "items": []})["items"].append(s)
    designs = json.loads((ROOT / "tools" / "work_designs.json").read_text(encoding="utf-8"))
    positions = list(range(1, len(designs) + 1))
    rest = [p for p in positions if p not in DESIGNS_FIRST and p not in MA_HAWA_DESIGNS]
    order = DESIGNS_FIRST + rest + [p for p in MA_HAWA_DESIGNS if p not in DESIGNS_FIRST]
    videos = [line.split("v=")[1].strip() for line in (ROOT / "portfolio-videos.txt").read_text(encoding="utf-8").splitlines() if "v=" in line]
    return {
        "sprite": re.search(r'<svg width="0" height="0" style="position:absolute".*?</svg>', source, re.S).group(0),
        "fonts": re.search(r'<link href="(https://fonts\.googleapis\.com/css2[^"]+)"', source).group(1),
        "ai": [s for s in services if not s["group"]],
        "groups": list(groups.values()),
        "designs": [designs[p - 1] for p in order],
        "videos": videos,
    }


def wa(lang: str) -> str:
    source = TEXT["source"][0 if lang == "en" else 1]
    return sp.wa_link({"WHATSAPP": build.WHATSAPP}, sc.UI[lang]["wa_talk"].format(source=source))


def page_url(lang: str, slug: str) -> str:
    return build.SITE + sp.path(lang, slug)


def slug_for(title_en: str, defs: list[dict]) -> str | None:
    return next((d["slug"] for d in defs if d["match"] == title_en), None)


def price_cell(service: dict) -> str:
    if build.parse_price(service["price"]["en"])[0] is None:
        return f'<span class="pr req">{e(service["price"]["en"])} · <span lang="ar">{e(service["price"]["ar"])}</span></span>'
    return f'<span class="pr">{e(service["price"]["en"])}</span>'


def service_row(service: dict, slug: str) -> str:
    return (
        f'<div class="srow"><a lang="en" href="{page_url("en", slug)}">{e(service["title"]["en"])}</a>'
        f'{price_cell(service)}'
        f'<a lang="ar" dir="rtl" href="{page_url("ar", slug)}">{e(service["title"]["ar"])}</a></div>'
    )


def header(number: int) -> str:
    return (f'<header class="ph"><a class="brand" href="#cover"><svg><use href="#i-logo"/></svg><span>H.M Media</span></a>'
            f'<span class="pn">{number:02d}</span></header>')


def footer() -> str:
    return (f'<footer class="pf"><a href="{e(wa("en"))}">WhatsApp {e(build.PHONE_DISPLAY)}</a>'
            f'<a href="mailto:{build.EMAIL}">{build.EMAIL}</a><a href="{build.SITE}/">h-m.agency</a></footer>')


def page(inner: str, number: int, anchor: str = "", body_class: str = "body") -> str:
    attrs = f' id="{anchor}"' if anchor else ""
    return f'<section class="page"{attrs}>{header(number)}<div class="{body_class}">{inner}</div>{footer()}</section>'


# --------------------------------------------------------------------------- cover and services
def cover() -> str:
    stills = "".join(f'<img src="{image_uri(f"/assets/home/wall-{i:02d}.webp")}" alt="">' for i in COVER_STILLS)
    return f"""<section class="page cover" id="cover">
  <div class="collage">{stills}</div>
  <div class="cover-in">
    <div class="cover-brand"><svg><use href="#i-logo"/></svg><span>H.M Media</span></div>
    {bi('profile', 'h1', 'cover-h')}
    {bi('slogan', 'p', 'slogan')}
    {bi('intro', 'p', 'intro')}
    <div class="cover-btns">
      <a class="btn" href="#services">{e(TEXT['services'][0])} · <span lang="ar">{e(TEXT['services'][1])}</span></a>
      <a class="btn" href="#work">{e(TEXT['portfolio'][0])} · <span lang="ar">{e(TEXT['portfolio'][1])}</span></a>
      <a class="btn ghost" href="{e(wa('ar'))}"><svg><use href="#i-wa"/></svg>{e(TEXT['whatsapp'][0])} · <span lang="ar">{e(TEXT['whatsapp'][1])}</span></a>
    </div>
    <p class="cover-contact"><a href="{e(build.WHATSAPP)}">{e(build.PHONE_DISPLAY)}</a> · <a href="mailto:{build.EMAIL}">{build.EMAIL}</a> · <a href="{build.SITE}/">h-m.agency</a></p>
  </div>
</section>"""


def services_page(data: dict, number: int) -> str:
    blocks = [
        f'<div class="srow hdr"><span lang="en">Service</span><span class="pr">{e(TEXT["from"][0])} · <span lang="ar">{e(TEXT["from"][1])}</span></span><span lang="ar" dir="rtl">الخدمة</span></div>',
        f'<div class="ghead">{bi("agency", "h2", "gh")}</div>',
    ]
    for g in data["groups"]:
        gslug = slug_for(g["name"]["en"], sc.GROUP_PAGES)
        rows = "".join(service_row(s, slug_for(s["title"]["en"], sc.AGENCY_PAGES) or gslug) for s in g["items"])
        blocks.append(
            f'<div class="grp"><div class="bi sub"><a lang="en" href="{page_url("en", gslug)}">{e(g["name"]["en"])}</a>'
            f'<a lang="ar" dir="rtl" href="{page_url("ar", gslug)}">{e(g["name"]["ar"])}</a></div>{rows}</div>'
        )
    ai_rows = "".join(service_row(s, slug_for(s["title"]["en"], sc.AI_PAGES)) for s in data["ai"])
    blocks.append(f'<div class="ghead ai">{bi("ai", "h2", "gh")}</div><div class="grp">{ai_rows}</div>')
    inner = f"""{bi('services', 'h2', 't')}
<div class="svc">{''.join(blocks)}</div>
{bi('note', 'p', 'note')}"""
    return page(inner, number, anchor="services")


# --------------------------------------------------------------------------- portfolio layout
def next_row(aspects: list[float], start: int, target: float) -> tuple[int, float]:
    """Greedy justified row from `start`: returns (end index, row height in mm) for a full-width row.
    A short tail that would make an over-tall last row is pulled into this row instead."""
    total, end = 0.0, start
    while end < len(aspects):
        total += aspects[end]
        end += 1
        height = (CONTENT_W - GAP * (end - start - 1)) / total
        if height <= target:
            break
    rest = sum(aspects[end:])
    if 0 < rest and (CONTENT_W - GAP * (len(aspects) - end - 1)) / rest > target * 1.45:
        total += rest
        end = len(aspects)
    return end, (CONTENT_W - GAP * (end - start - 1)) / total


def plan_rows(aspects: list[float], start: int, avail: float) -> tuple[list[tuple[int, int, float]], float]:
    """Rows that fill `avail` mm best from `start`, trying every target height. Returns (rows, leftover)."""
    best = None
    for target in ROW_TARGETS:
        rows, used, pos = [], 0.0, start
        while pos < len(aspects):
            end, height = next_row(aspects, pos, target)
            need = height + (GAP if rows else 0.0)
            if used + need > avail:
                break
            rows.append((pos, end, height))
            used, pos = used + need, end
        if not rows:
            continue
        leftover = 0.0 if pos == len(aspects) else avail - used
        score = (leftover, abs(target - 46))
        if best is None or score < best[0]:
            best = (score, rows, avail - used)
    return (best[1], best[2]) if best else ([], avail)


def video_thumb(vid: str) -> tuple[str, float]:
    """A JPEG of the video's YouTube thumbnail with any black bars cut off, and its aspect ratio, so a
    vertical reel keeps its tall shape instead of showing side bars."""
    fallback = (f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg", 16 / 9)
    if JPEG_DIR is None or not shutil.which("ffmpeg"):
        return fallback
    raw = JPEG_DIR / f"yt-{vid}-raw.jpg"
    out = JPEG_DIR / f"yt-{vid}.jpg"
    try:
        request = urllib.request.Request(f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg", headers={"User-Agent": "Mozilla/5.0"})
        raw.write_bytes(urllib.request.urlopen(request, timeout=30).read())
        probe = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(raw), "-vf", "cropdetect=limit=24:round=2:reset=0", "-f", "null", "-"],
                               capture_output=True, text=True, stdin=subprocess.DEVNULL)
        found = re.findall(r"crop=(\d+):(\d+):(\d+):(\d+)", probe.stderr)
        w, h, x, y = map(int, found[-1]) if found else (480, 270, 0, 45)
        if w < 120 or h < 120 or w * h < 0.15 * 480 * 360:  # a dark frame fooled the detector: use the 16:9 centre
            w, h, x, y = 480, 270, 0, 45
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(raw), "-vf", f"crop={w}:{h}:{x}:{y},format=yuvj420p",
                        "-q:v", "4", "-frames:v", "1", str(out)], check=True, stdin=subprocess.DEVNULL)
        return out.as_uri(), w / h
    except (OSError, ValueError, subprocess.CalledProcessError):
        return fallback


def row_html(tiles: list[dict], start: int, end: int, height: float) -> str:
    """One justified row: every tile is as wide as its image's shape needs at this height."""
    out = []
    for t in tiles[start:end]:
        play = '<span class="play"></span>' if t["video"] else ""
        out.append(f'<a class="jt" style="flex:{t["aspect"]:.4f} 1 0" href="{t["href"]}"><img src="{t["uri"]}" alt="">{play}</a>')
    return f'<div class="jrow" style="height:{height:.2f}mm">{"".join(out)}</div>'


def portfolio_pages(data: dict, first_number: int) -> list[str]:
    design_tiles = [{"uri": image_uri(d["thumb"]), "aspect": d["w"] / d["h"], "href": f"{build.SITE}{d['full']}", "video": False}
                    for d in data["designs"]]
    video_tiles = []
    for v in data["videos"]:
        uri, aspect = video_thumb(v)
        video_tiles.append({"uri": uri, "aspect": aspect, "href": f"https://www.youtube.com/watch?v={v}", "video": True})
    sections = [("designs", design_tiles), ("videos", video_tiles)]
    sub = lambda key, anchor: f'<div class="sub-h" id="{anchor}">{bi(key, "h3", "sh")}</div>'  # noqa: E731
    title = f'{bi("work", "h2", "t")}{bi("work_note", "p", "note top")}'
    closing = f"""<div class="closing">
  {bi('slogan', 'p', 'slogan sm')}
  <div class="cover-btns">
    <a class="btn" href="{e(wa('ar'))}"><svg><use href="#i-wa"/></svg>{e(TEXT['whatsapp'][0])} · <span lang="ar">{e(TEXT['whatsapp'][1])}</span></a>
    <a class="btn ghost" href="{build.SITE}/work/">{e(TEXT['more'][0])} · <span lang="ar">{e(TEXT['more'][1])}</span></a>
  </div>
</div>"""

    pages, number, si, pos = [], first_number, 0, 0
    first = True
    while si < len(sections):
        parts, avail, anchor = [], BODY_H, ""
        if first:
            parts.append(title)
            avail -= TITLE_H
            anchor = "work"
        while si < len(sections):
            key, tiles = sections[si]
            if pos == 0:
                if avail < SUB_H + 32:  # no room to start this section on this page
                    break
                parts.append(sub(key, key))
                avail -= SUB_H
            rows, leftover = plan_rows([t["aspect"] for t in tiles], pos, avail)
            if not rows:
                break
            parts += [row_html(tiles, s, e_, h) for s, e_, h in rows]
            pos, avail = rows[-1][1], leftover - GAP
            if pos < len(tiles):
                break  # page full
            si, pos = si + 1, 0  # section done: the next one may start on this page
        last = si >= len(sections)
        if last and avail >= CLOSING_H:
            parts.append(closing)
            last_done = True
        else:
            last_done = False
        pages.append(page("".join(parts), number, anchor=anchor, body_class="body fill" if not last else "body"))
        number += 1
        first = False
        if last and not last_done:
            pages.append(page(closing, number, body_class="body center"))
            number += 1
    return pages


CSS = """
@page { size: A4; margin: 0; }
:root { --bg:#060706; --card:#0c0f0d; --line:#1b1f1d; --text:#f3f5f4; --text-2:#a9b0ac; --text-3:#6f7773;
        --accent:#3dbe72; --accent-hi:#74f0a6; --on-accent:#03140a; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { background: var(--bg); color: var(--text); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Manrope', 'IBM Plex Sans Arabic', sans-serif; font-size: 9.5pt; line-height: 1.5; }
[lang=ar] { font-family: 'IBM Plex Sans Arabic', 'Manrope', sans-serif; }
a { color: inherit; text-decoration: none; }
svg { fill: currentColor; }
.page { width: 210mm; height: 297mm; padding: 12mm 15mm 16mm; position: relative; overflow: hidden; break-after: page; display: flex; flex-direction: column; }
.page:last-child { break-after: auto; }
.body { flex: 1; min-height: 0; display: flex; flex-direction: column; }
.body.fill { justify-content: space-between; }
.body.center { justify-content: center; }
.ph { display: flex; justify-content: space-between; align-items: center; padding-bottom: 4mm; margin-bottom: 7mm; border-bottom: 1px solid var(--line); font-size: 8pt; color: var(--text-3); }
.brand { display: inline-flex; align-items: center; gap: 2mm; color: var(--text); font-weight: 700; font-size: 9pt; }
.brand svg { width: 5.5mm; height: 5.5mm; color: var(--accent); }
.pf { position: absolute; left: 15mm; right: 15mm; bottom: 7mm; display: flex; justify-content: space-between; font-size: 7.5pt; color: var(--text-3); }
/* English on the left, Arabic on the right */
.bi { display: flex; justify-content: space-between; align-items: baseline; gap: 10mm; }
.bi > [lang=en] { text-align: left; }
.bi > [lang=ar] { text-align: right; }
.t { font-size: 21pt; line-height: 1.15; font-weight: 800; letter-spacing: -0.01em; color: var(--text); }
.bi:has(.t) { margin-bottom: 2mm; }
.note { color: var(--text-2); font-size: 8.5pt; margin-top: 5mm; }
.note.top { margin: 0 0 4mm; }
.bi .note, .bi .intro, .bi .slogan { flex: 1; }
.btn { display: inline-flex; align-items: center; gap: 2mm; height: 10mm; padding: 0 5mm; border-radius: 5mm; background: var(--accent); color: var(--on-accent); font-weight: 800; font-size: 9.5pt; white-space: nowrap; }
.btn svg { width: 4.2mm; height: 4.2mm; }
.btn.ghost { background: var(--card); color: var(--text); border: 1px solid #2a302c; }
.cover { padding: 0; }
.collage { position: absolute; left: 0; right: 0; top: 0; height: 112mm; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr 1fr; gap: 1.5mm; }
.collage img { width: 100%; height: 100%; object-fit: cover; display: block; }
.cover-in { position: absolute; left: 15mm; right: 15mm; bottom: 16mm; }
.cover-brand { display: flex; align-items: center; gap: 3mm; font-weight: 800; font-size: 15pt; margin-bottom: 7mm; }
.cover-brand svg { width: 11mm; height: 11mm; color: var(--accent); }
.cover-h { font-size: 30pt; line-height: 1.1; font-weight: 800; }
.slogan { color: var(--accent-hi); font-size: 14pt; font-weight: 700; margin-top: 3mm; }
.slogan.sm { font-size: 12pt; }
.intro { color: var(--text-2); font-size: 10pt; margin-top: 6mm; }
.cover-btns { display: flex; flex-wrap: wrap; gap: 3mm; margin-top: 8mm; }
.cover-contact { color: var(--text-3); font-size: 8.5pt; margin-top: 6mm; }
.svc { margin-top: 3mm; }
.ghead { display: flex; justify-content: space-between; align-items: end; gap: 4mm; margin: 2.5mm 0 0; }
.ghead .bi { flex: 1; }
.ghead.ai { margin-top: 4.5mm; }
.gh { font-size: 11pt; color: var(--accent-hi); font-weight: 800; }
.srow.hdr { border-top: 0; color: var(--text-3); font-size: 7.8pt; font-weight: 700; text-transform: uppercase; letter-spacing: .06em; padding-bottom: 0; }
.srow.hdr .pr { color: var(--text-3); font-size: 7.8pt; }
.srow.hdr [lang=ar] { letter-spacing: 0; }
.grp { margin-top: 0.5mm; }
.sub { font-size: 7.6pt; text-transform: uppercase; letter-spacing: .08em; color: var(--text-3); font-weight: 700; padding: 1.8mm 0 0.6mm; }
.sub [lang=ar] { letter-spacing: 0; }
.srow { display: grid; grid-template-columns: 1fr auto 1fr; align-items: center; gap: 4mm; padding: 1.05mm 0; border-top: 1px solid var(--line); font-size: 9pt; line-height: 1.35; }
.srow [lang=ar] { text-align: right; }
.pr { color: var(--accent-hi); font-weight: 700; font-size: 8.8pt; white-space: nowrap; text-align: center; min-width: 30mm; }
.pr.req { color: var(--text-2); font-weight: 600; }
/* Portfolio: justified rows. Each tile's width follows its image's shape, so nothing is cropped or left empty. */
.sub-h { height: 9mm; display: flex; align-items: center; }
.sub-h .bi { flex: 1; }
.sh { font-size: 11pt; color: var(--accent-hi); font-weight: 800; }
.jrow { display: flex; gap: 2.2mm; flex: none; }
.jt { position: relative; display: block; height: 100%; border-radius: 1.6mm; overflow: hidden; background: var(--card); min-width: 0; }
.jt img { width: 100%; height: 100%; object-fit: cover; display: block; }
.play { position: absolute; left: 50%; top: 50%; width: 6.5mm; height: 6.5mm; margin: -3.25mm 0 0 -3.25mm; border-radius: 50%; background: var(--accent); }
.play::after { content: ""; position: absolute; left: 2.6mm; top: 1.85mm; border-style: solid; border-width: 1.4mm 0 1.4mm 2.3mm; border-color: transparent transparent transparent var(--on-accent); }
.closing { padding-top: 5mm; border-top: 1px solid var(--line); flex: none; }
.closing .cover-btns { margin-top: 4mm; }
"""


def render(data: dict) -> str:
    pages = [cover(), services_page(data, 2)] + portfolio_pages(data, 3)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>H.M Media — Company Profile | الملف التعريفي</title>
<meta name="author" content="H.M Media">
<meta name="description" content="H.M Media company profile: creative agency services with starting prices and the full portfolio of designs and videos. Details at h-m.agency.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{data['fonts']}" rel="stylesheet">
<style>{CSS}</style>
</head>
<body>
{data['sprite']}
{''.join(pages)}
</body>
</html>
"""


def main() -> int:
    global JPEG_DIR
    data = load()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        JPEG_DIR = pathlib.Path(tmp) / "jpeg"
        JPEG_DIR.mkdir()
        document = render(data)
        page_path = pathlib.Path(tmp) / "profile.html"
        page_path.write_text(document, encoding="utf-8")
        command = [
            chrome_path(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--generate-pdf-document-outline", "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=60000", "--allow-file-access-from-files",
            f"--user-data-dir={pathlib.Path(tmp) / 'chrome'}",
            f"--print-to-pdf={OUT}", page_path.as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=300)
        if result.returncode != 0 or not OUT.exists():
            print(result.stderr[-2000:], file=sys.stderr)
            return 1
    pages = document.count('<section class="page')
    print(f"profile_pdf: wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1_048_576:.1f} MB, {pages} pages, "
          f"{len(data['designs'])} designs, {len(data['videos'])} videos)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
