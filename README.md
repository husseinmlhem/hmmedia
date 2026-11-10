# H.M Media website

Static site for [h-m.agency](https://h-m.agency/), served by GitHub Pages from `main`.

## How it is put together

- `index.html` is the **single source of truth**. English text sits in the markup and the
  Arabic translation in each element's `data-ar` attribute.
- `ar/index.html` is the Arabic page at `https://h-m.agency/ar/`. It is **generated**: do
  not edit it by hand.
- `llms.txt`, `sitemap.xml` and the SEO block in the `<head>` of `index.html` (between the
  `build:head` markers) are generated too.

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
