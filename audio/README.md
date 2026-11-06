# ROYAL AUDIO

ROYAL AUDIO is the shared, versioned sound-effects library for the ROYAL application family. It is additive and does not replace or modify the existing icon library or existing audio assets.

## Approved V1 scope
- Non-verbal effects: notifications, UI interaction, commerce, media/TV, system status, and reminders.
- Optional natural ambience: weather and nature loops, currently indexed for ROYAL+ Launcher only.
- Human voice recordings and spoken announcements are excluded.
- Human speech and music/background themes remain excluded. Natural ambience is not music and is opt-in or weather-condition driven.
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
Applications reference stable catalog IDs, not guessed filenames. Missing optional audio must never crash app startup. Each app should control effects, notifications, and ambience separately. Rate-limit UI effects and avoid overlapping alerts. Natural ambience is currently allowlisted only for ROYAL+ Launcher; nature scenes require explicit user opt-in, while weather loops require a matching verified weather state. Thunder is a separate, spaced overlay used only with the thunderstorm rain bed. Do not add spoken prompts or music.


### Clear-night owl ambience
- Stable ID: `nature.owl.clear_night`; reserved for ROYAL+ Launcher only.
- Eligible only from 19:00 until 06:00 on the device's local clock, with a confirmed current weather code of 0 (clear sky) or 1 (mainly clear).
- Use short one-shot owl calls at randomized intervals of 30–60 minutes; do not loop the same call continuously.
- Stop immediately when the time window ends, the weather changes, weather data is loading/stale/unavailable, the user mutes ambience, or the launcher leaves the active foreground session.
- This entry remains `planned`; do not play anything until a real recording, OGG asset, and embedding/redistribution rights evidence are reviewed and committed.

## Current status
- The catalog contains 33 indexed assets: 23 original non-verbal interface/system effects and 10 licensed natural weather/nature recordings.
- All 33 WAV masters and 33 OGG runtime files are packaged and have passed automated file, format, catalog and licence-metadata checks.
- Catalog state is built, not ready: playback still needs confirmation on a real phone and TV device.
- Stable integration IDs and app allowlists are present, but this library change does not yet add playback code to the applications.
