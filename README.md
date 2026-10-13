# CUZDEV

The multilingual CUZDEV studio and game website for **cuzdev.xyz**.

## Contents

- Independent, AI-assisted game-development introduction.
- Dedicated ZZZombie Assault and Floki Heaven pages with system-by-system explanations and matching screenshots.
- English, Brazilian Portuguese, Spanish, German, French and Italian on all three pages: 18 static localized routes.
- Original Akashi wind-idle, Satoshi three-strike sword combo and Floki running sprites, with pause and reduced-motion support.
- Real project screenshots and keyboard-accessible galleries.
- Responsive layout, self-hosted fonts, and an email contact link.
- No trackers, cookies, build dependencies, or third-party runtime requests.

Both games are in development. No release dates, storefronts, or playable-download claims are implied.

## Edit / preview

Edit translated copy in `content/<language>.json`. All six files must have the same structure; there is no English fallback. Generate pages with the standard-library-only builder, then run the route tests:

```sh
python tools/build_site.py
python -m unittest discover -s tests -v
```

Layout is in `styles.css` and `pages.css`; behavior is in `site.js`. The old `script.js` is retained for history but is not loaded by the generated pages. For a local preview, run:

```sh
python -m http.server 8784 --bind 127.0.0.1
```

Then open `http://127.0.0.1:8784`.

The English pages are `/`, `/zzzombie-assault/` and `/floki-heaven/`. Other languages use `/pt-br/`, `/es/`, `/de/`, `/fr/` and `/it/` prefixes. The language selector preserves the current game. Content is readable without JavaScript; galleries and sprite animation use it. Text inside original screenshots retains the captured build's language.

## Hosting

GitHub Pages publishes the `main` branch from the repository root. `.nojekyll` keeps the static files unchanged. `CNAME` binds the custom domain; preserve it when updating the site.

The domain and DNS remain managed at Hostinger. Website records point to GitHub Pages; mail records must remain intact.

## Assets

The ZZZombie Assault lead screenshot shows Aurora Refuge at dawn, captured in the game with the HUD hidden. It is a staged development capture, not an uninterrupted playthrough. Its WebP export preserves the original rendered pixels without color grading or thumbnail overlays.

Game screenshots belong to their respective game creators and are included for this website's promotional use. They are not a general-purpose asset pack. Self-hosted Barlow Condensed and Space Grotesk fonts are distributed under their included SIL Open Font License files in `assets/fonts/`.
