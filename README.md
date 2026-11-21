# JayNova Brands

A fictional creative studio and satirical storefront for AI-style content, logos, and digital products.

## Features

- Responsive storefront with product category filters
- Three original, free demo downloads: an editable SVG logo, 24 captions, and a short digital playbook
- Browser-based brand lab with three visual moods, custom SVG export, and caption copying
- Product dialogs, mobile navigation, accessible FAQ disclosures, and reduced-motion support

## Preview locally

No build step or package installation is required. From the repository root, run:

```sh
python3 -m http.server 8080 --directory dist
```

Open http://localhost:8080 in your browser.

## Files

- `dist/index.html` — page markup and content
- `dist/styles.css` — responsive styles
- `dist/app.js` — filters, dialogs, downloads, and brand generator
- `dist/assets/` — original SVG assets
- `.openai/hosting.json` — existing Sites deployment configuration

The site uses optional Google Fonts with local fallback fonts. The brand lab runs entirely in the browser without a live AI API, account signup, checkout, or analytics.

## Content notice

This is an independent fictional brand and a parody of online hustle culture. It makes no claims about real people or businesses and presents no sales, client, or earnings claims. Original demo designs and text may be used and edited for personal or commercial projects, non-exclusively, without warranty or trademark clearance.

## Validation

JavaScript syntax and local asset references were checked. Product filters, all three product downloads, SVG generation and export, caption copying, and mobile navigation were exercised in the browser. Desktop and 390px mobile layouts were reviewed.
