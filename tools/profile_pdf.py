"""Builds the short company profile PDF: cover, services, designs and videos, English and Arabic on every page.

    python3 tools/profile_pdf.py

Run it after changing services, prices or the portfolio, and commit the new PDF. It writes
assets/pdf/hm-media-company-profile.pdf, the file behind the "Company profile (PDF)" buttons.

The profile is deliberately short: it does not repeat the website. Service names and starting
prices come from index.html and every row links to its page on the site for the details. The
portfolio is a selection (DESIGNS, VIDEOS below) chosen by the owner's brief: a mix of clients,
with only one piece from Ma Hawa, and creative work first with AI as one of the tools.

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

# Portfolio selection. Designs are positions in tools/work_designs.json (1 = first entry);
# videos are YouTube ids from portfolio-videos.txt. One page of each: 9 designs, 18 videos.
# Beauty and perfume first (16 Khas Oud & Perfumes, 18 Purity Perfumes, 19 Omega Clinic), then
# 17 Origins, 8 the one Ma Hawa piece, 14 real estate, 15 retail sale, 20 SuperFuture, 23 ZBX.
DESIGNS = [16, 18, 19, 17, 8, 14, 15, 20, 23]
VIDEOS = [
    "E3ms8T00kNE",  # Video portfolio reel
    "S8aDIat3kkw",  # Deyaar advertisement
    "et9KdAG5oN8",  # HomeCenter banner animation (Landmark Group)
    "Y_oFNMsaskw",  # Reels for Al Aan TV
    "l9X_BniLV7E",  # SHEEL platform promo
    "qwTjrFI4NSE",  # Imdaat event promo
    "1UoZUdNysD4",  # Mobile shoot and edit (event)
    "yWAyfPUTgqw",  # Farm in Al Ain: shoot and edit
    "VHPPo8D7c5k",  # Guinness record video
    "KfLCOY4AwGs",  # Commercial ad
    "9j2eYryyDPQ",  # Ma Hawa brand intro (the one Ma Hawa video)
    "Zai3_AkXUIk",  # Deyaar logo animation
    "icBho8tUjfw",  # Logo animation (Dr Bob Lorinser)
    "D9Z8jOfIav0",  # Logo animation (Arabic)
    "OaxgKerMWr4",  # Logo animations
    "nPY4qOfaNkQ",  # Puffy mattress concept ad (AI)
    "69zX4V_b4LE",  # Cinematic video "Balance from the inside" (AI)
    "TZePv-D88Ls",  # Cinematic video, penguin (AI)
]
COVER_STILLS = [1, 3, 4, 5, 6, 7]  # assets/home/wall-NN.webp; wall-02 is Ma Hawa, so it is left out

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
    "designs": ("Selected designs", "مختارات من التصاميم"),
    "videos": ("Selected videos & motion", "مختارات من الفيديو والموشن"),
    "tap_designs": ("Tap a design to open it full size.", "اضغط على أي تصميم لفتحه بالحجم الكامل."),
    "tap_videos": ("Tap a video to watch it.", "اضغط على أي فيديو لمشاهدته."),
    "more": ("More work on h-m.agency", "المزيد من الأعمال على الموقع"),
    "portfolio": ("Portfolio", "أعمالنا"),
    "whatsapp": ("WhatsApp", "واتساب"),
    "source": ("Company profile PDF", "الملف التعريفي PDF"),
}


def e(text: str) -> str:
    return html.escape(text, quote=True)


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
    known = {line.split("v=")[1].strip() for line in (ROOT / "portfolio-videos.txt").read_text(encoding="utf-8").splitlines() if "v=" in line}
    missing = [v for v in VIDEOS if v not in known]
    if missing or max(DESIGNS) > len(designs):
        raise SystemExit(f"profile_pdf: selection points at work that is not on the site: {missing or max(DESIGNS)}")
    return {
        "sprite": re.search(r'<svg width="0" height="0" style="position:absolute".*?</svg>', source, re.S).group(0),
        "fonts": re.search(r'<link href="(https://fonts\.googleapis\.com/css2[^"]+)"', source).group(1),
        "ai": [s for s in services if not s["group"]],
        "groups": list(groups.values()),
        "designs": [designs[i - 1] for i in DESIGNS],
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


def page(inner: str, number: int, anchor: str = "") -> str:
    attrs = f' id="{anchor}"' if anchor else ""
    return f'<section class="page"{attrs}>{header(number)}<div class="body">{inner}</div>{footer()}</section>'


# --------------------------------------------------------------------------- pages
def cover() -> str:
    stills = "".join(f'<img src="{(ROOT / "assets" / "home" / f"wall-{i:02d}.webp").as_uri()}" alt="">' for i in COVER_STILLS)
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


def designs_page(data: dict, number: int) -> str:
    tiles = []
    for d in data["designs"]:
        local = (ROOT / urllib.parse.unquote(d["full"]).lstrip("/")).as_uri()
        tiles.append(f'<a class="tile" href="{build.SITE}{d["full"]}"><img src="{local}" alt=""></a>')
    inner = f"""{bi('designs', 'h2', 't')}
{bi('tap_designs', 'p', 'note top')}
<div class="dgrid">{''.join(tiles)}</div>"""
    return page(inner, number, anchor="work")


def videos_page(number: int) -> str:
    tiles = "".join(
        f'<a class="vt" href="https://www.youtube.com/watch?v={v}"><img src="https://i.ytimg.com/vi/{v}/hqdefault.jpg" alt=""><span class="play"></span></a>'
        for v in VIDEOS
    )
    inner = f"""{bi('videos', 'h2', 't')}
{bi('tap_videos', 'p', 'note top')}
<div class="vgrid">{tiles}</div>
<div class="closing">
  {bi('slogan', 'p', 'slogan sm')}
  <div class="cover-btns">
    <a class="btn" href="{e(wa('ar'))}"><svg><use href="#i-wa"/></svg>{e(TEXT['whatsapp'][0])} · <span lang="ar">{e(TEXT['whatsapp'][1])}</span></a>
    <a class="btn ghost" href="{build.SITE}/work/">{e(TEXT['more'][0])} · <span lang="ar">{e(TEXT['more'][1])}</span></a>
  </div>
</div>"""
    return page(inner, number, anchor="videos")


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
.note.top { margin: 0 0 5mm; }
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
.dgrid { flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(3, 1fr); grid-template-rows: repeat(3, minmax(0, 1fr)); gap: 3.5mm; margin-bottom: 4mm; }
.tile { background: var(--card); border: 1px solid var(--line); border-radius: 3mm; overflow: hidden; display: flex; align-items: center; justify-content: center; }
.tile img { width: 100%; height: 100%; object-fit: contain; display: block; }
.vgrid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm; }
.vt { position: relative; display: block; aspect-ratio: 16 / 9; border-radius: 2.5mm; overflow: hidden; background: var(--card); border: 1px solid var(--line); }
.vt img { width: 100%; height: 100%; object-fit: cover; display: block; }
.play { position: absolute; left: 50%; top: 50%; width: 8mm; height: 8mm; margin: -4mm 0 0 -4mm; border-radius: 50%; background: var(--accent); }
.play::after { content: ""; position: absolute; left: 3.2mm; top: 2.3mm; border-style: solid; border-width: 1.7mm 0 1.7mm 2.8mm; border-color: transparent transparent transparent var(--on-accent); }
.closing { margin-top: auto; padding-top: 5mm; border-top: 1px solid var(--line); margin-bottom: 3mm; }
.closing .cover-btns { margin-top: 4mm; }
"""


def render(data: dict) -> str:
    pages = [cover(), services_page(data, 2), designs_page(data, 3), videos_page(4)]
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>H.M Media — Company Profile | الملف التعريفي</title>
<meta name="author" content="H.M Media">
<meta name="description" content="H.M Media company profile: creative agency services with starting prices and selected work. Details at h-m.agency.">
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
    data = load()
    document = render(data)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        page_path = pathlib.Path(tmp) / "profile.html"
        page_path.write_text(document, encoding="utf-8")
        command = [
            chrome_path(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
            "--generate-pdf-document-outline", "--run-all-compositor-stages-before-draw",
            "--virtual-time-budget=45000", "--allow-file-access-from-files",
            f"--user-data-dir={pathlib.Path(tmp) / 'chrome'}",
            f"--print-to-pdf={OUT}", page_path.as_uri(),
        ]
        result = subprocess.run(command, capture_output=True, text=True, timeout=240)
        if result.returncode != 0 or not OUT.exists():
            print(result.stderr[-2000:], file=sys.stderr)
            return 1
    print(f"profile_pdf: wrote {OUT.relative_to(ROOT)} ({OUT.stat().st_size / 1_048_576:.1f} MB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
