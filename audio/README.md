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
- Stable ID: `nature.owl.clear_night`; allowlisted for ROYAL+ Launcher only.
- The catalog entry is built and has a licensed OGG/WAV asset; device playback remains pending.
- Eligible only from 19:00 until 06:00 on the device's local clock, with confirmed current weather code 0 (clear sky) or 1 (mainly clear).
- Play as a one-shot at randomized intervals of 30–60 minutes; never loop continuously.
- Stop when the time window ends, weather changes or becomes stale/unavailable, ambience is muted, or the launcher leaves the active foreground session.
- Keep the catalog's activation and timing metadata authoritative.

### Phone and TV listening checklist
Open each OGG link below on the target device. If the browser downloads it instead of playing, open the downloaded file with the device's audio player. Check that the sound is audible, not clipped, not excessively loud, and appropriate for its event. Test short effects on the phone; test TV/media effects on the TV speakers where applicable. Record any track that is silent, distorted, too loud, too quiet, or assigned to the wrong event. Do not change any catalog status to `ready` until the real-device check is complete.


### الإشعارات

- [وصول رسالة جديدة — notification.message.new](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/notification.message.new.ogg) — 340 ms
- [تنبيه عام — notification.alert.general](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/notification.alert.general.ogg) — 480 ms
- [نجاح — notification.success](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/notification.success.ogg) — 430 ms
- [تعذر إتمام العملية — notification.failure](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/notification.failure.ogg) — 520 ms

### التفاعل والواجهة

- [نقرة زر خفيفة — ui.button.tap.soft](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/ui.button.tap.soft.ogg) — 75 ms
- [تأكيد الاختيار — ui.selection.confirm](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/ui.selection.confirm.ogg) — 180 ms
- [فتح لوحة — ui.panel.open](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/ui.panel.open.ogg) — 160 ms
- [إغلاق لوحة — ui.panel.close](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/ui.panel.close.ogg) — 140 ms
- [رجوع — ui.navigation.back](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/ui.navigation.back.ogg) — 120 ms

### الطلبات والعمليات

- [إضافة للسلة — commerce.cart.add](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/commerce.cart.add.ogg) — 220 ms
- [استلام طلب جديد — commerce.order.received](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/commerce.order.received.ogg) — 500 ms
- [نجاح الدفع — commerce.payment.success](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/commerce.payment.success.ogg) — 440 ms
- [اكتمال الطلب — commerce.order.complete](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/commerce.order.complete.ogg) — 480 ms

### الوسائط والتلفاز

- [تشغيل الوسائط — media.play](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/media.play.ogg) — 100 ms
- [إيقاف مؤقت — media.pause](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/media.pause.ogg) — 100 ms
- [تغيير القناة — media.channel.changed](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/media.channel.changed.ogg) — 180 ms
- [اتصال البث — media.channel.connected](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/media.channel.connected.ogg) — 340 ms
- [انقطاع البث — media.channel.disconnected](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/media.channel.disconnected.ogg) — 430 ms

### النظام والحالة

- [التحديث جاهز — system.update.ready](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/system.update.ready.ogg) — 430 ms
- [نجاح البناء — system.build.success](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/system.build.success.ogg) — 430 ms
- [فشل البناء — system.build.failure](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/system.build.failure.ogg) — 560 ms

### التذكيرات

- [انتهاء المؤقت — reminders.timer.finished](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/reminders.timer.finished.ogg) — 680 ms
- [تنبيه وقت الصلاة — reminders.prayer.alert](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/reminders.prayer.alert.ogg) — 490 ms

### أصوات الطبيعة

- [تغريد الطيور الطبيعي — nature.birds.general](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/nature.birds.general.ogg) — 15300 ms
- [أمواج البحر الهادئة — nature.ocean.waves](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/nature.ocean.waves.ogg) — 15290 ms
- [جريان جدول الماء — nature.water.stream](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/nature.water.stream.ogg) — 15300 ms
- [حفيف أوراق الأشجار — nature.leaves.rustle](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/nature.leaves.rustle.ogg) — 15274 ms
- [صوت الرياح الطبيعية الهادئة — nature.wind.gentle](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/nature.wind.gentle.ogg) — 15300 ms
- [أصوات العصافير الصباحية — nature.birds.morning](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/nature.birds.morning.ogg) — 15300 ms
- [نداء بومة ليلي هادئ — nature.owl.clear_night](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/nature.owl.clear_night.ogg) — 6000 ms

### أصوات الطقس

- [مطر طبيعي هادئ — weather.rain.natural](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/weather.rain.natural.ogg) — 9631 ms
- [مطر العاصفة الرعدية — weather.thunderstorm.rain](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/weather.thunderstorm.rain.ogg) — 15300 ms
- [دوي الرعد الطبيعي — weather.thunderstorm.thunder](https://raw.githubusercontent.com/Ramistar900/royal-design/f79622365c2d1d515d8f3761e5883dcf4a77389f/audio/assets/ogg/weather.thunderstorm.thunder.ogg) — 8000 ms


## Current status
- The catalog contains 33 indexed assets: 23 original non-verbal interface/system effects and 10 licensed natural weather/nature recordings.
- All 33 WAV masters and 33 OGG runtime files are packaged and have passed automated file, format, catalog and licence-metadata checks.
- Catalog state is built, not ready: playback still needs confirmation on a real phone and TV device.
- Stable integration IDs and app allowlists are present, but this library change does not yet add playback code to the applications.
