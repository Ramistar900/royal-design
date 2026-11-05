# ROYAL AUDIO

ROYAL AUDIO is the shared, versioned sound library for the ROYAL application family. It is additive and does not replace or modify the existing icon library.

## Approved V1 scope
- Short human voice recordings and confirmations (Arabic-first).
- Sound effects for notifications, UI, commerce, media/TV, system status, and reminders.
- **Background music and intro music are excluded from V1.**
- WAV (PCM) masters; OGG delivery assets for Android. MP3 only when a real compatibility need is documented.

## Repository layout
- `catalog.json`: stable machine-readable index.
- `assets/wav/`: lossless source masters.
- `assets/ogg/`: optimized Android playback assets.
- `licenses/`: provenance, performer consent, and licence evidence.
- `../scripts/validate-audio-catalog.py`: automated catalog and asset validation.

## Stable IDs
Use lowercase stable IDs such as `notification.message.new`, `ui.button.tap.soft`, `commerce.order.received`, `media.channel.connected`, and `voice.order.received.ar`. Never reuse an ID for a different sound.

## Rights and production rules
1. Use original recordings or audio with explicit redistribution and app-embedding rights.
2. Record creator/performer, source, licence name and evidence, redistribution permission, attribution, modifications, and review date.
3. Obtain explicit performer consent for the intended apps and redistribution scope.
4. No ripped audio, unlicensed samples, impersonation, or voice cloning of identifiable people.
5. Preserve clean WAV masters; create OGG delivery copies without overwriting masters.
6. Keep UI/notification effects short, clear, non-fatiguing, and free of clipping.
7. Respect Android audio focus, notification-channel settings, accessibility speech, and user mute/volume preferences.

## Integration guidance
Applications reference stable catalog IDs, not guessed filenames. Missing optional audio must never crash app startup. Each app should control effects, notifications, and voice separately. Rate-limit UI effects and avoid overlapping alerts.

## Current status
V1 foundation only: documentation, planned catalog entries, and CI validation. Catalog entries remain planned until real files and rights evidence are checked in. No app integration or playable audio assets are claimed yet.
