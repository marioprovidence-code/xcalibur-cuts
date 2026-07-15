# Xcalibur Cuts — Android App (APK) Build Config

The website is already a PWA, so the fastest way to ship a real Android app is to
wrap that PWA. Two options are provided; **TWA (Bubblewrap)** is recommended because
it just opens the live site (no rebuild needed when you update the website).

Site URL : https://marioprovidence-code.github.io/xcalibur-cuts/
Manifest  : https://marioprovidence-code.github.io/xcalibur-cuts/manifest.webmanifest
Package ID: com.xcaliburcuts.app

=====================================================================
PREREQUISITES (needed for either path)
=====================================================================
1. Node.js 20+        -> https://nodejs.org
2. Java JDK 17        -> https://adoptium.net  (set JAVA_HOME)
3. Android SDK        -> install "Android Studio", then SDK Platform 34 + Build-Tools
   set ANDROID_HOME to the SDK path (e.g. C:\Users\You\AppData\Local\Android\Sdk)
4. Accept licenses:   in Android Studio -> SDK Manager -> SDK Tools -> "Google Play Licensing" + accept,
   or run:  sdkmanager --licenses

=====================================================================
OPTION A — TWA via Bubblewrap (recommended)
=====================================================================
# one-time install of the CLI
npm install -g @bubblewrap/cli

# generate the Android project from the live PWA manifest
bubblewrap init --manifest https://marioprovidence-code.github.io/xcalibur-cuts/manifest.webmanifest

# build the signed AAB/APK (follow prompts; create a keystore when asked)
bubblewrap build

Output: app-release-bundle.aab (upload to Google Play) and/or app-release-signed.apk
(to install directly: adb install app-release-signed.apk)

A prefilled template is in twa-manifest.json (Bubblewrap will regenerate/complete it).

=====================================================================
OPTION B — Capacitor (bundles a WebView)
=====================================================================
npm install
npx cap init "Xcalibur Cuts" com.xcaliburcuts.app
npx cap add android
npx cap sync
npx cap build android        # or: npx cap open android  (build in Android Studio)

capacitor.config.json points server.url at the live site, so updates to the website
show in the app without rebuilding.

=====================================================================
NOTES
=====================================================================
- To publish on Google Play you need a Play Console account (one-time $25) and the AAB.
- For direct APK distribution (no Play Store), install the signed APK via adb or share it.
- "Install App" button + QR on the website already let Android users add the PWA today,
  no APK required. This APK is only needed if you want a store listing / standalone package.
