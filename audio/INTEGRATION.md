# ROYAL AUDIO Application Integration Index

This document defines the stable contract for connecting the shared sound library to applications. The machine-readable source of truth is `audio/catalog.json`; this document explains how to consume it.

## Application keys

| Key | Application | Intended use |
|---|---|---|
| `almalaki` | Almalaki | Customer UI, orders, cart, payment, reminders and app status |
| `royal_tv` | ROYAL TV | TV interface feedback and stream/player state |
| `rami` | RAMİ DEVELOPER | Interface feedback, notifications and build results |
| `royalplus_launcher` | ROYAL+ Launcher | Launcher interaction, notifications and prayer/timer reminders |
| `sinjar_tv_show` | SİNJAR TV SHOW | TV interface feedback and stream/player state |

## Stable event IDs

Every track has an immutable `id` and a matching `integration.event_key`. Applications should request audio by this ID, never by a display name or a filename guessed independently.

| Category | Event ID pattern | Typical consumer |
|---|---|---|
| Notifications | `notification.*` | Relevant apps listed on each catalog entry |
| UI | `ui.*` | Shared UI feedback in supported apps |
| Commerce | `commerce.*` | Almalaki only |
| Media | `media.*` | ROYAL TV and SİNJAR TV SHOW |
| System | `system.*` | Update status in apps; build outcomes in RAMİ |
| Reminders | `reminders.*` | Almalaki, RAMİ and ROYAL+ Launcher as listed per track |

The exact application allowlist and suggested duration for each event live in the corresponding track's `integration` object in `catalog.json`.

## Asset naming and formats

- WAV source master: `audio/assets/wav/{track_id}.wav` (PCM, 48 kHz / 24-bit preferred).
- OGG Android runtime: `audio/assets/ogg/{track_id}.ogg`.
- Keep the WAV master unchanged when exporting OGG.
- Do not create placeholder, silent, generated-empty, or renamed files to make a track appear ready.
- A track remains `planned` until both real assets exist and the licence evidence is verified. Only then may it become `ready`.

## Runtime integration contract

1. Load the catalog as data; use `id` / `event_key` to resolve an effect.
2. Check that the current app key appears in `integration.applications` before requesting playback.
3. If an ID is absent, the file is missing, or playback fails, continue silently; audio must never block navigation, ordering, playback, startup, or build workflows.
4. Respect app sound settings, Android notification-channel settings, audio focus, device volume and mute state.
5. Rate-limit repeated UI effects; never replay a click sound for every animation frame or rapid key-repeat.
6. Use notification channels for background notifications. Do not use short UI effects as a substitute for critical visual alerts.
7. Keep playback local and lightweight; do not download or stream effects during a critical user action.
8. Apps may disable individual categories or all effects. No app may force sound on.

## Suggested playback behavior

- UI taps and navigation: very short, quiet, and rate-limited.
- Success and confirmation: one brief, distinct cue; avoid celebratory fanfare.
- Failure and disconnection: clear but restrained; do not loop.
- Commerce: play only after the corresponding action is confirmed by the app's business logic.
- Media: play on actual state changes, not on every buffering or rendering callback.
- Prayer and timer reminders: user-configurable, independently muteable, and never spoken.

## Release and compatibility

- Treat IDs as public integration keys once used by an app. Never repurpose an existing ID for a different sound.
- Add new effects with new IDs and update the catalog and this document in the same reviewed change.
- Keep optional sound loading defensive so older app versions can run with a newer catalog.
- Before marking an effect ready, validate rights, WAV/OGG files, duration and playback on phone and TV speakers.
- This index does not itself add audio playback code to any application.

## Current status

The 23 catalog entries are indexed for five application keys. All entries are still planned; no playable audio assets or app-side integrations are claimed by this index.
