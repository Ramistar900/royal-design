# ROYAL Design v5 — Finance & Shopping

Reusable original icon set for ROYAL applications.

- 20 icons covering money, wallets, payments, shopping, orders, discounts, and quantity controls.
- SVG source: 24 × 24 viewBox, outline style, 1.8 stroke, `currentColor` tinting.
- Android resources: matching VectorDrawable XML files in `android/res/drawable/`.
- Android vectors use a neutral dark stroke; apply `android:tint` or a theme tint when displaying them.
- Resource names keep the `royal_` prefix and are safe to use as drawable identifiers.
- The isolated Android validation module compiles v3 and v5 vector resources together.
- Existing v2, v3, and v4 source assets are not replaced.

## Android usage

Copy the XML files from `android/res/drawable/` into an app's `res/drawable/` directory, then reference them by name, for example `R.drawable.royal_wallet`.

## SVG source files

- `royal_coin.svg`
- `royal_banknote.svg`
- `royal_wallet.svg`
- `royal_credit_card.svg`
- `royal_receipt.svg`
- `royal_cart.svg`
- `royal_basket.svg`
- `royal_shopping_bag.svg`
- `royal_plus.svg`
- `royal_minus.svg`
- `royal_circle_plus.svg`
- `royal_circle_minus.svg`
- `royal_discount.svg`
- `royal_tag.svg`
- `royal_calculator.svg`
- `royal_cash_register.svg`
- `royal_transfer.svg`
- `royal_hand_coins.svg`
- `royal_order_check.svg`
- `royal_payment_terminal.svg`

## Android VectorDrawable files

The Android directory contains one XML resource for each SVG icon, with the same `royal_` resource name.
