# JayNova Brands

A fictional creative studio with a real, free digital-product starter guide, original logo demos, a caption pack, and a browser-based brand lab.

## Free starter guide

`assets/jaynova-digital-product-starter-guide.pdf` is a 12-page original beginner workbook. It covers choosing a useful product, defining an audience, outlining and drafting, using AI responsibly, testing, packaging, privacy basics, and a first-week plan. No account, email address, payment, or optional analytics consent is required.

## GitHub Pages hosting

This repository is a buildless static site. The publishing files live at the repository root. In **Settings → Pages**, select **Deploy from a branch**, **main**, **/(root)**, and **Save**. The root `CNAME` file specifies `jaynovabrands.com`; `.nojekyll` disables unnecessary Jekyll processing. Future commits to `main` publish through GitHub Pages once it is enabled.

Configure the custom domain in GitHub Pages before switching DNS. The Namecheap records for GitHub Pages are:

| Type | Host | Value |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | nadidoug.github.io. |

Remove conflicting former hosting A/AAAA/ALIAS records at `@` and the former `www` CNAME as part of that switch. Enable HTTPS in GitHub Pages when its certificate is ready.

## Local preview

No build step or package installation is required:

```sh
python3 -m http.server 8080
```

Open http://localhost:8080. All fonts come from the visitor's device; no external font request is made.

## Optional database counting

The existing Supabase project hosts an isolated `jaynova_private` schema. The browser has no direct read or write access to these tables. The `jaynova-download` Edge Function checks the public application key, request origin, consent flag, version, and product ID, then calls a backend-only database function. Only the public publishable key is present in `config.js`; server secrets stay in the function environment.

- Analytics are off until a visitor explicitly opts in.
- Essential-only downloads work without an analytics request.
- The browser sends only the guide identifier, consent flag, and notice version.
- Daily totals are event counts, not unique people, customers, or sales.
- A daily-rotating keyed IP hash is used for basic abuse throttling. Raw IP addresses, names, emails, user agents, and visitor profiles are not stored in the application tables.
- A named daily cleanup job removes expired abuse-control hashes and old aggregate counts. Providers may independently retain service logs.
- Global Privacy Control and Do Not Track keep optional counting off.
- The consent preference is stored on the device for up to 180 days and can be changed from the footer.

Backend source is in `backend/schema.sql`, `backend/retention.sql`, and `backend/functions/jaynova-download/`. The schema and retention job are already applied, and the function is deployed. Backend totals are available only to authorized project administrators:

```sql
select day, product_slug, downloads
from jaynova_private.daily_downloads
order by day desc;
```

No signup database, mailing list, payment collection, or marketing email has been enabled.

## Privacy and terms

`privacy.html` describes the implemented data flow, preference storage, providers, retention, and contact route. `terms.html` describes the free guide and permitted use. These pages are technical notices, not a guarantee against legal claims or a certification of compliance in every jurisdiction. They must be reviewed when the operator, audience, data use, or services change.

## PDF source

The guide's source is `scripts/create_starter_guide.py`. Regeneration requires Python, ReportLab, and DejaVu Sans fonts. In this repository layout, set the script's output path to `assets/jaynova-digital-product-starter-guide.pdf` if regenerating outside the original workspace.

## Validation

JavaScript syntax and local assets were checked. The 12-page PDF was rendered and visually reviewed. Browser checks confirmed the free download, preference controls, and counting only after opt-in. Database checks verified backend-only privileges and rate limiting. The security advisor reports default-deny RLS on the private tables as informational; no visitor policies are intentionally granted.
