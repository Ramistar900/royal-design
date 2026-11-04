# ROYAL Café, Restaurant & Orders — v9

A colorful, animated icon collection for café and restaurant products, order progress, delivery, bookings, and payments.

## Collection status

The first 29 icon concepts are now present in both static and motion variants.

### Food and drinks (10)
- `royal_coffee` — coffee, with gently rising steam
- `royal_juice` — juice, with floating bubbles
- `royal_food_shawarma` — shawarma
- `royal_food_burger` — burger
- `royal_food_pizza` — pizza
- `royal_food_dessert` — dessert
- `royal_food_tea` — tea
- `royal_food_sandwich` — sandwich
- `royal_food_ice_cream` — ice cream
- `royal_food_salad` — salad

### Orders and delivery (9)
- `royal_order_new` — new order
- `royal_order_accepted` — order received
- `royal_order_confirmed` — order confirmed
- `royal_order_preparing` — preparing
- `royal_order_ready` — ready
- `royal_order_pickup` — ready for pickup
- `royal_delivery_out` — out for delivery
- `royal_delivery_progress` — delivery in progress
- `royal_order_delivered` — delivered
- `royal_order_cancelled` — cancelled

### Bookings (6)
- `royal_booking_table_available` — table available
- `royal_booking_table_occupied` — table occupied
- `royal_booking_new` — new booking
- `royal_booking_confirmed` — confirmed booking
- `royal_booking_waiting` — awaiting confirmation
- `royal_booking_cancelled` — cancelled booking

### Payments (3)
- `royal_payment_pending` — payment in progress
- `royal_payment_success` — payment successful
- `royal_payment_refund` — refund

> The counts above are grouped by category; there are 29 icons total.

## Asset formats

- Static SVG: `svg/`
- Animated SVG (SMIL): `motion/svg/`
- Static Android VectorDrawable: `android/res/drawable/*.xml`
- Android AnimatedVectorDrawable: `android/res/drawable/*_animated.xml`
- Android animator resources: `android/res/animator/`

Static assets are preserved as fallbacks. Motion is optional and designed to be subtle, smooth, and non-distracting. Start animated drawables only when the related UI state is visible or changes, and stop them when the view is not visible. Respect reduced-motion preferences by using the static drawable.

## Palette and motion direction

Royal blue `#4B8FE8`, emerald `#16A085`, gold `#F5B942`, coral `#F26D5B`, violet `#8A6CE8`, plus food-specific warm tones.

Motion uses gentle pulses, slight floating, soft turns, and restrained directional movement. Avoid continuous animation when an icon is off-screen or when the user has requested reduced motion.

## Validation and integration

The Android resources are included in `icon-validation` and the GitHub Actions workflow watches `icons/v9/**`. A successful CI run is still required before marking the full collection build-verified.

This collection is library-only and has not been wired into Almalaki, ROYAL TV, or any other application.
