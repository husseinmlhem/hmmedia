# H.M Media website

Static site for [h-m.agency](https://h-m.agency/), served by GitHub Pages from `main`.

## How it is put together

- `index.html` is the **single source of truth**. English text sits in the markup and the
  Arabic translation in each element's `data-ar` attribute.
- `ar/index.html` is the Arabic page at `https://h-m.agency/ar/`. It is **generated**: do
  not edit it by hand.
- `llms.txt`, `sitemap.xml` and the SEO block in the `<head>` of `index.html` (between the
  `build:head` markers) are generated too.
- **Service pages**: `services/<slug>/` (English) and `ar/services/<slug>/` (Arabic) are generated too: one page
  per AI service plus one per agency category (design, video, marketing, web). Names, prices and shared FAQ
  answers are read from `index.html`; the extra wording is in `tools/service_content.py` and the page
  template is `tools/service_pages.py`. To add a page, add an entry to `tools/service_content.py` and rerun the build.
  Keep the copy to what the home page already says about the service.

## After changing any text, price, service or FAQ

```sh
python3 tools/build.py            # regenerate ar/index.html, llms.txt, sitemap.xml and the head block
python3 tools/build.py --check    # exits 1 if the generated files are out of date
```

Commit the regenerated files together with your change. The script needs only Python 3.

## Where SEO settings live

Everything is at the top of `tools/build.py`: page titles and descriptions for both
languages, the business details used in the schema.org structured data (phone, email,
address, areas served, social profiles, founder) and the share images.

The services, prices and FAQs in the structured data and in `llms.txt` are read from the
page itself, so they always match what visitors see.

Keep the business name, phone and address identical to the Google Business Profile.

## Languages

English is served at `/` and Arabic at `/ar/`. The language switch navigates between the
two, and both pages declare each other with `hreflang`. Old `/?lang=ar` links redirect to
`/ar/`.

## Bing and IndexNow

`75940b3faad763cfcdc621f0a77714d5.txt` is the IndexNow ownership key (keep it in the site root). After a deploy, notify Bing of changed pages with a POST to `https://api.indexnow.org/indexnow` containing `host`, `key`, `keyLocation` (`https://h-m.agency/75940b3faad763cfcdc621f0a77714d5.txt`) and `urlList`.
