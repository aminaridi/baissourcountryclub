# Baissour Country Club — Website & Menu

Bilingual (English / Arabic) website and restaurant menu for **Baissour Country Club**,
a riverside resort in Baissour, Aley District, Mount Lebanon.

- Live preview: https://claude.ai/code/artifact/8dd05977-61f4-4a0e-8fb6-1df339bf138f
- Contact: baissourcountryclub@gmail.com · WhatsApp +961 81 130 345

## Repository layout

| Folder | What it is |
|---|---|
| `deploy/` | **Production-ready website.** Upload the *contents* of this folder to the web root (`public_html/`) of baissourcountryclub.com. Includes `README.txt` with hand-off instructions. |
| `site/` | Website source: `build_site.py` (generator), `site.json` (all content, both languages), `assets/` (photos & videos), `index.html` (self-contained single-file build). |
| `menu/` | Restaurant menu: `build.py` + `menu.json` sources, `web.html` (interactive), `print.html`, `BCC-Menu.pdf` (print-ready, A4). |

## Editing content

All website text, prices, and photo assignments live in `site/site.json` (English and
Arabic side by side). All menu items and prices live in `menu/menu.json`.

Rebuild after editing (requires Python 3 with Pillow):

```bash
cd site && python3 build_site.py            # → site/index.html (single-file)
cd site && BCC_DEPLOY=1 python3 build_site.py   # → site/dist/ (multi-file deploy)
cd menu && python3 build.py                 # → menu/web.html + menu/print.html
```

## Notes for the webmaster

- The site is fully static — no server-side code or database.
- Forms open WhatsApp (+961 81 130 345) and email, with an automatic email copy via
  FormSubmit.co — the first submission after going live sends a one-time activation
  email to baissourcountryclub@gmail.com; click **Activate** once.
- Fonts load from Google Fonts; keep `fonts.googleapis.com` reachable.
- Enable HTTPS on the host (Let's Encrypt is fine).
