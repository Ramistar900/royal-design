# ALMALAKI motion assets

Each *_animated.svg has its own matching static 2D and 3D files listed in ../catalog.json.
Motion is separate from static artwork. The fixed gloss/highlights never animate.
Start motion only when visible or when the user invokes the action; stop when off-screen.
When reduced motion is enabled, use the matching static SVG instead.
These SVG files are motion source/preview assets. Android 8 VectorDrawable/AnimatedVectorDrawable exports and real-device validation remain a separate integration step.
