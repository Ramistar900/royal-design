# ROYAL AUDIO

ROYAL AUDIO is the shared, versioned sound library for the ROYAL application family.

## V1 scope

- Notification sounds: message, alert, success, warning, error, update.
- UI sounds: tap, select, open, close, back, confirm.
- Commerce sounds: order received, purchase, payment success, cart add.
- Media sounds: play, pause, channel change, connection and stream errors.
- Voice clips: short human voice announcements and confirmations.
- Music: short original intro themes and optional ambient background beds.

Music is enabled in the approved V1 scope. Human voice clips are also enabled.

## Repository layout

- `catalog.json`: stable machine-readable index and category definitions.
- `assets/ogg/`: preferred compressed Android playback assets.
- `assets/wav/`: high-quality source masters where available.
- `licenses/`: per-pack provenance and license records.
- `../scripts/validate-audio-catalog.py`: catalog and asset validation.

## Asset rules

1. Only original recordings or assets with documented redistribution and app-embedding rights may be added.
2. Record creator/source, license name, license URL or proof reference, attribution requirements, and modification status for every track.
3. Do not add ripped audio from films, games, streaming services, or other apps.
4. Prefer OGG for Android runtime playback; retain WAV masters when practical. MP3 is allowed only when justified by compatibility.
5. Keep notification/UI effects short, normalized, and non-fatiguing. Keep voice and music opt-in per app and user preference.
6. Never overwrite an existing track ID. Deprecate IDs rather than reusing them.
7. Keep audio assets separate from the existing `icons/` tree and do not modify the icon catalog.

## Catalog contract

Each track has a unique stable `id`, a category, a localized display name, a relative asset path, format, duration, and license metadata. The initial catalog intentionally contains no audio binaries; tracks are added only after their rights and files are verified.

## Integration guidance

Apps should consume a pinned catalog version and use stable track IDs, not hard-coded repository paths. Each app should provide independent volume/mute controls for effects, notifications, voice, and music. Playback should respect Android audio focus and avoid overlapping repeated alerts.

## Current status

V1 foundation only: directory contract, catalog schema, documentation, and CI validation. No sound files have been added yet, and no application has been connected to the library.
