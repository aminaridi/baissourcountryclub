# BCC Grill menu — one source, everywhere

`menu.json` is the only place a menu item, price or description is edited.
Then run:

    python3 grill-menu/sync_menu.py

which regenerates, in one pass:

| Output | Where |
|---|---|
| Website ordering page menu | `docs/grill/index.html` (MENU block) |
| Ordering app menu | `grill-menu/app-orders.html` → publish to https://claude.ai/artifact/XTxWubQaqW8fzNhVNYxP2o |
| Printed A4 menus EN + AR (PDF) | `docs/grill/menu/BCC-Grill-Menu-EN.pdf`, `-AR.pdf` (linked from the page) |
| TV boards 1920×1080 (bilingual / EN / AR) | `docs/grill/menu/BCC-Grill-TV-Board*.png` |
| Phone menu for WhatsApp / Instagram | `docs/grill/menu/BCC-Grill-Menu-Phone*.png` |

Then `git commit` + `git push` (the site is GitHub Pages from `docs/`).

Requires Node with Playwright (for the PDFs/PNGs); pass `--no-render` to update only the two pages.

## Photos
- Signature photos for print/TV live in `grill-menu/img/` (`photo` field on a signature).
- Per-item photos for the website and app: put the file in `docs/grill/menu/photos/` and set `"webPhoto": "<file>.jpg"` on the item in `menu.json`.

## Rules baked in
Meter Kabab is parked (not on any menu). Prices in USD. Phone 81 461 188. No delivery-time promise.
Say "take away". No employee names on anything customer-facing.
