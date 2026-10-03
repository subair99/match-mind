# Friction log

## 1. Vega installer exits before writing ~/vega/env (3 Oct)
- **Task attempted:** Install Vega SDK 0.24.12112 on Ubuntu 24.04 (WSL2)
- **Steps taken:** Ran the get_vvm.sh installer
- **Expected:** Install completes and `vega` is on PATH
- **What actually happened:** Stray input during download was taken as the answer to the optional Vega Studio prompt; installer printed "Invalid input" and exited. SDK was installed but ~/vega/env was never created, so `vega` was not found
- **Severity:** Medium
- **Workaround used:** Removed ~/vega and re-ran the installer
- **Actionable suggestion:** Write ~/vega/env before optional prompts, and re-ask on invalid input instead of exiting

## 2. Virtual Device silently fails: missing system libraries (3 Oct)
- **Task attempted:** `vega virtual-device start`
- **Expected:** Device boots
- **What actually happened:** CLI only said "virtual device unresponsive" after the timeout. Real cause, in instances/<id>/virtual_device.err: libpulse.so.0 missing, then libtinfo.so.5 (not packaged on Ubuntu 24.04)
- **Severity:** High
- **Workaround used:** `apt install libpulse0`; symlinked libtinfo.so.6 to libtinfo.so.5
- **Actionable suggestion:** Installer checks these libraries; CLI prints virtual_device.err when the emulator exits early

## 3. Sports sample postinstall needs Java and `python` (3 Oct)
- **Task attempted:** `npm install` in vega-sports-app
- **What actually happened:** Shaka Player build failed: "required dependency is missing: java" and "/usr/bin/env: 'python': No such file"
- **Severity:** Medium
- **Workaround used:** `apt install default-jre-headless python-is-python3`
- **Actionable suggestion:** List Java and python in the sample's README prerequisites

## 4. Sports sample crashes the Virtual Device without GPU acceleration (3 Oct)
- **Task attempted:** Launch vega-sports-app on VVD started with `--no-gl-accel`
- **What actually happened:** Emulator crashed on app launch; virtual_device.err showed only crash-reporter output. With GPU acceleration on it runs, with intermittent player errors that give no reason
- **Severity:** Medium
- **Workaround used:** Start VVD without `--no-gl-accel`
- **Actionable suggestion:** Clear crash message; show the underlying error code in the sample's player error screen