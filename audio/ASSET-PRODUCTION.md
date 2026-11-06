# ROYAL AUDIO asset production

## Asset groups
- 23 original, non-verbal procedural cues for notifications, interface actions, commerce, media, system status and reminders.
- 10 natural weather and nature recordings, including the clear-night owl call, reserved for ROYAL+ Launcher.

## File formats
- Preservation masters: WAV PCM, 48 kHz, 24-bit.
- Android playback copies: OGG Vorbis.
- Natural loops are crossfaded at the loop point. Thunder and the owl call are one-shot overlays; the app controls their spacing and weather/time conditions.

## Readiness states
- planned: no approved files are packaged yet.
- built: WAV and OGG files exist, licence/source metadata is recorded, hashes are written, and automated checks pass.
- ready: requires the built checks plus actual playback verification on a phone and a TV device. The CI script does not set ready automatically.

## Safety boundaries
- No spoken words, voice clips, voice clones, music, or background themes.
- Natural ambience is allowlisted only for ROYAL+ Launcher; existing catalog activation and opt-in conditions remain authoritative.
- Missing audio must remain optional and must never block app startup, navigation, ordering, playback, or builds.
- This process changes only the ROYAL AUDIO feature branch and does not modify application source, Supabase, or release workflows.
