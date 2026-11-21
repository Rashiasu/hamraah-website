# Hamraah Advisors website

Static multi-page site for Hamraah Advisors (SMC-Private) Limited, an expert-led study-abroad consultancy (USA focus, plus Europe). Live at https://www.hamraahadvisors.com via Vercel (each push to `main` deploys).

- Content lives in `_build/build.py` (services, experts, prices, FAQ, contact details). Edit there, then run `python3 _build/build.py` to regenerate the `.html` pages, `sitemap.xml` and `robots.txt`, and commit the output.
- `styles.css` brand styling (maroon #6B1E2E, deep #2A0C13, gold #C9A55A; DM Serif Display + Inter)
- `main.js` menu, scroll effects, booking form (sends via WhatsApp or email; number and email are constants at the top, keep them in sync with `build.py`)
- `vercel.json` clean URLs (`/pricing` serves `pricing.html`)
