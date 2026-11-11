# ROYAL Design V18 — semantic motion

- Animated SVGs updated: **213**
- Static SVGs preserved: **213**
- Focused SVGs preserved: **25**
- Total SVGs preserved: **451**
- Animation format: basic SVG SMIL using animate and animateTransform.
- No JavaScript, CSS keyframes, filters, external assets, or file removals.
- Motion is applied to icon glyphs or meaningful details, not the tile background.
- The original SVG artwork remains visible as a static fallback when animation is unsupported.

## Processed by category

| Category | Animated SVGs |
|---|---:|
| display | 45 |
| launcher | 25 |
| player_music | 21 |
| player_video | 20 |
| store | 45 |
| tv | 57 |

## Android 8 rendering note

The assets use basic SVG elements and SMIL animation only. Android 8 devices need an SVG-capable renderer or WebView to play motion. A native ImageView/VectorDrawable parser that accepts only static vector paths will still show the unchanged icon artwork, but will not execute SMIL.
