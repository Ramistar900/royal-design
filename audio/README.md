# ROYAL AUDIO

ROYAL AUDIO is the shared, versioned sound-effects library for the ROYAL application family. It is additive and does not replace or modify the existing icon library or existing audio assets.

## Approved V1 scope
- Sound effects only: notifications, UI interaction, commerce, media/TV, system status, and reminders.
- Human voice recordings and spoken announcements are excluded.
- Music and background/intro themes are excluded; only functional sound effects are included.
- WAV (PCM) masters; OGG delivery assets for Android. MP3 only when a real compatibility need is documented.

## Repository layout
- `catalog.json`: stable machine-readable index.
- `assets/wav/`: lossless source masters.
- `assets/ogg/`: optimized Android playback assets.
- `licenses/`: provenance and licence evidence.
- `../scripts/validate-audio-catalog.py`: automated catalog and asset validation.

## Stable IDs
Use lowercase stable IDs such as `notification.message.new`, `ui.button.tap.soft`, `commerce.order.received`, and `media.channel.connected`. Never reuse an ID for a different sound.

## Rights and production rules
1. Use original sound-effect recordings or audio with explicit redistribution and app-embedding rights.
2. Record creator, source, licence name and evidence, redistribution permission, attribution, modifications, and review date.
3. No ripped audio or unlicensed samples.
4. Preserve clean WAV masters; create OGG delivery copies without overwriting masters.
5. Keep UI/notification effects short, clear, non-fatiguing, and free of clipping.
6. Respect Android audio focus, notification-channel settings, and user mute/volume preferences.

## Integration guidance
Applications reference stable catalog IDs, not guessed filenames. Missing optional audio must never crash app startup. Each app should control effects and notifications separately. Rate-limit UI effects and avoid overlapping alerts. Do not add spoken prompts or background music.

## Current status
V1 foundation only: documentation, planned catalog entries, and CI validation. Catalog entries remain planned until real files and rights evidence are checked in. No app integration or playable audio assets are claimed yet.
