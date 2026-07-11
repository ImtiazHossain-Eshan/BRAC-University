# CSE 489 — Assignment 2

Android app practicing **fragments**, the **navigation drawer**, and **Jetpack** (Navigation
component, ViewBinding, Kotlin). A drawer swaps between four feature fragments; the Broadcast
Receiver feature branches into dedicated activities.

## Requirement → implementation map

| Requirement | Where it lives |
|---|---|
| Navigation drawer + fragments (Jetpack) | `MainActivity` + `res/navigation/mobile_navigation.xml` + `res/menu/activity_main_drawer.xml` |
| **A. Broadcast Receiver** — spinner (2 options) + Proceed | `ui/broadcast/BroadcastReceiverFragment` + `res/values/arrays.xml` |
| A.1 — 2nd activity takes plain-text input | `broadcast/TextInputActivity` |
| A.1 — 3rd activity: **custom** `BroadcastReceiver` receives the text | `broadcast/CustomReceiverActivity` + `broadcast/CustomBroadcastReceiver` |
| A.2 — 2nd activity receives **battery** percentage broadcast | `broadcast/BatteryActivity` (`Intent.ACTION_BATTERY_CHANGED`) |
| A.2 — 3rd activity does nothing | (battery flow ends at `BatteryActivity`) |
| **B. Image scale** — load from internet + pinch to zoom | `ui/image/ImageScaleFragment` (Glide) + `ui/image/ZoomableImageView` (`ScaleGestureDetector`) |
| **C. Video** — play a video in-app | `ui/video/VideoFragment` (`VideoView` + `MediaController`, `res/raw/sample_video.mp4`) |
| **D. Audio** — play audio in-app | `ui/audio/AudioFragment` (`MediaPlayer`, `res/raw/sample_audio.mp3`) |

### Custom broadcast flow (A.1)
`BroadcastReceiverFragment` → **Proceed** → `TextInputActivity` (type text) → **Send broadcast** →
`CustomReceiverActivity`. There a `CustomBroadcastReceiver` is registered dynamically
(`RECEIVER_NOT_EXPORTED`); the activity sends an app-internal broadcast with the text, and the
receiver catches it and shows it.

## Build & run

Open the folder in Android Studio and press **Run**, or from the command line:

```bash
./gradlew installDebug      # build + install to a running emulator/device
./gradlew assembleDebug     # just build the APK (app/build/outputs/apk/debug/)
```

## Tech stack
- Kotlin, ViewBinding, Material Components
- Jetpack **Navigation** component (drawer)
- Glide (internet image loading)
- AGP 9 (built-in Kotlin) · Gradle 9.4.1 · `compileSdk 36` · `minSdk 26` · `targetSdk 34`

`targetSdk` is 34 so the platform does not force Android 15+ edge-to-edge; the classic ActionBar
then insets content correctly on every screen. `compileSdk` remains 36.
