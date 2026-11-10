# ROYAL Design

Private shared design and icon library for ROYAL projects.

## الفهرس الشامل للمكتبة

- **[فهرس جميع الأيقونات V2–V9](./icons/README.md)** — الأسماء العربية، مفاتيح الاستخدام، معرّفات Android وروابط SVG وXML والحركة.
- **[الفهرس الآلي JSON](./icons/catalog.json)** — بيانات منظمة لأدوات المطور والبحث الآلي.
- **[المعرض المرئي الخاص](./gallery/README.md)** — معاينة صور SVG الأصلية لجميع أيقونات V2–V9 داخل المستودع الخاص، مع الاسم ومفتاح الاستخدام ومورد Android.

الإجمالي: **162 أيقونة أساسية**، و162 مورداً ثابتاً لـAndroid، إضافة إلى 37 نسخة SVG متحركة و37 مورداً Android متحركاً في V9.

## ROYAL DESIGN V13 — Original 2D icons

- Guide: [icons/v13/2d/README.md](./icons/v13/2d/README.md)
- Catalog: [icons/v13/2d/catalog.json](./icons/v13/2d/catalog.json)
- First batch: 8 original concepts with separate Flat and Glass SVGs (16 files). Visual approval is still pending; no IconScout artwork is included.

## ROYAL AUDIO — Shared Audio Library

- **[ROYAL UI SOUNDS listening gallery](./audio/ui-sounds/player.html)** — 49 interface and TV effects with direct playback, kept separate from nature/weather audio.

- Guide: [audio/README.md](./audio/README.md)
- Catalog: [audio/catalog.json](./audio/catalog.json)
- Recording guide: [audio/recording-guidelines.md](./audio/recording-guidelines.md)
- Integration contract: [audio/INTEGRATION.md](./audio/INTEGRATION.md)
- Validation workflow: [Validate ROYAL AUDIO](./.github/workflows/validate-royal-audio.yml)
- Licence and attribution records: [audio/licenses/ATTRIBUTIONS.md](./audio/licenses/ATTRIBUTIONS.md)

V1 contains 23 original non-verbal effects and 10 licensed natural/weather recordings. All 33 tracks have WAV masters and OGG runtime files (66 files total). Automated validation passes; device playback is still pending, so tracks remain `built`, not `ready`. Human voice clips and background music are excluded.

## Android Icons v2

The version 2 archive contains Android VectorDrawable XML and SVG icon assets.

- Archive: [ROYAL_Android_Icons_v2.zip](./ROYAL_Android_Icons_v2.zip)
- Contents: 22 Android VectorDrawable XML icons, 22 SVG icons, and the included README.

## Android Icons v3 — Preview

The v3 preview contains 10 additional icon concepts in SVG and Android VectorDrawable formats. Version 2 remains unchanged.

- Preview guide: [icons/v3/README.md](./icons/v3/README.md)
- Android VectorDrawable XML: [icons/v3/android/res/drawable/](./icons/v3/android/res/drawable/)
- Editable SVG sources: [icons/v3/svg/](./icons/v3/svg/)
- Automated Android resource compilation: [Validate ROYAL Android Icons v3–v9](./.github/workflows/validate-royal-icons-v3.yml)
- Package workflow: [Package ROYAL Android Icons v3](./.github/workflows/package-royal-icons-v3.yml)

## Finance & Shopping Icons v5

A reusable set of 20 original outline icons for money, wallets, payments, shopping, orders, discounts, and quantity controls.

- Guide: [icons/v5/finance-shopping/README.md](./icons/v5/finance-shopping/README.md)
- SVG source assets: [icons/v5/finance-shopping/svg/](./icons/v5/finance-shopping/svg/)
- Android VectorDrawable XML: [icons/v5/finance-shopping/android/res/drawable/](./icons/v5/finance-shopping/android/res/drawable/)

## Colorful Finance & Shopping Icons v6

A bright, filled multi-color companion collection with 12 new icons in SVG and Android VectorDrawable formats.

- Guide: [icons/v6/colorful-finance-shopping/README.md](./icons/v6/colorful-finance-shopping/README.md)
- SVG source assets: [icons/v6/colorful-finance-shopping/svg/](./icons/v6/colorful-finance-shopping/svg/)
- Android VectorDrawable XML: [icons/v6/colorful-finance-shopping/android/res/drawable/](./icons/v6/colorful-finance-shopping/android/res/drawable/)
- Palette: royal blue, emerald, gold, coral, and violet.

## Colorful Controls & Media Icons v7

A modern multi-color collection for search, settings, navigation arrows, window actions, back/close/menu, and music playback.

- Guide: [icons/v7/colorful-controls-media/README.md](./icons/v7/colorful-controls-media/README.md)
- SVG: [icons/v7/colorful-controls-media/svg/](./icons/v7/colorful-controls-media/svg/)
- Android VectorDrawable: [icons/v7/colorful-controls-media/android/res/drawable/](./icons/v7/colorful-controls-media/android/res/drawable/)

## Colorful Media & Product Badges v8

A colorful collection for Android music/video player controls and product-card badges such as NEW, special offer, sale, Premium, limited, bestseller, and featured.

- Guide: [icons/v8/colorful-media-product-badges/README.md](./icons/v8/colorful-media-product-badges/README.md)
- SVG: [icons/v8/colorful-media-product-badges/svg/](./icons/v8/colorful-media-product-badges/svg/)
- Android VectorDrawable: [icons/v8/colorful-media-product-badges/android/res/drawable/](./icons/v8/colorful-media-product-badges/android/res/drawable/)

## Café, Restaurant & Order Icons v9 — Expanded, validation pending

The v9 starter set contains 37 food/drink, purchase/order/delivery, booking, and payment icon concepts. Every icon has static and animated SVG and Android variants.

- Guide and complete name list: [icons/v9/cafe-orders/README.md](./icons/v9/cafe-orders/README.md)
- Static SVG: [icons/v9/cafe-orders/svg/](./icons/v9/cafe-orders/svg/)
- Static Android VectorDrawable: [icons/v9/cafe-orders/android/res/drawable/](./icons/v9/cafe-orders/android/res/drawable/)
- Animated SVG: [icons/v9/cafe-orders/motion/svg/](./icons/v9/cafe-orders/motion/svg/)
- Android AnimatedVectorDrawable and animator resources: [icons/v9/cafe-orders/android/res/](./icons/v9/cafe-orders/android/res/)

Motion includes coffee steam, juice bubbles, purchase and order pulses, delivery movement, food-icon micro-motion, booking indicators, and payment states. Static assets remain available for fallback and reduced-motion settings. The Android resource validator includes v9; a successful CI build must be confirmed before calling the collection build-verified.

Existing v2–v8 assets are retained. This repository is separate from the Almalaki, ROYAL TV, and ROYAL+ application repositories.
