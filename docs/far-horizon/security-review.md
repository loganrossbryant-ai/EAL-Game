# Defender alert — unresolved, download withdrawn

The user reported **Trojan:Script/Wacatac.B!ml**. Their Windows Security screenshot
shows **Severe** and **Active**. The affected filename/path is not established. The user reported no further details in the UI and later clarified they did not download the package.

The user was advised to use Defender's recommended quarantine/removal, keep
protection enabled, and run a full scan if the HTML had been opened. Do not
recommend restoring the package, adding exclusions, or bypassing the warning.

## Containment

Public commit `5923d19e5f6d7368224ca5f212d67decf76150f9` removes the current Far
Horizon HTML and ZIP from `hello-earth-demo/main`. The README records the hold.
This is withdrawal from the current branch; Git history and local evidence are
preserved. The unrelated root demo was not changed.

## Checks completed

- The ZIP contains exactly one unencrypted, normally named HTML file and passes
  its ZIP CRC checks. Its HTML matches the release package byte-for-byte.
- Embedded JS, WebAssembly, game PCK, and two audio helpers match the local
  release export byte-for-byte.
- The engine JS, WebAssembly, and both audio helpers match the official Godot
  4.6.3 non-threaded Web release template byte-for-byte.
- The downloaded template archive matches its release SHA-512 manifest.
- The project's browser-bridge calls handle local saves, the user-requested JSON
  export, and a debug-only observation snapshot. The source search found no
  project use of process execution, shell opening, HTTP clients, or sockets.
- The single-file loader decompresses embedded data and runs the official engine
  through Blob script/module URLs. This packaging pattern is a possible
  detection factor; that hypothesis has not been verified.

## Evidence identifiers

- ZIP SHA-256:
  `35a586759794ee79ad9979b3a2df704bc095f3f119bc39c90adccd36597af590`
- Embedded HTML SHA-256:
  `aae65757c483e136d1fcb9ab79683d2c2b1aabbd20e79f5a63cad3b3b7bf7e6e`
- Detailed local reports: ignored `artifacts/far-horizon-security/`.

## Limits and next step

These are provenance, integrity, and limited source checks, **not an antivirus
scan or security clearance**. This Linux environment has no Microsoft Defender
scanner. No false-positive verdict has been established. Do not advertise a
replacement as clean on this evidence, or modify packaging simply to get past
Defender. A Windows Defender investigation/validation is needed before another
download is recommended. Do not upload the sample to third-party scanning
services without authorization.

## Replacement validation

The user chose a normal browser play link. The standard separate-file Godot Web replacement passed a real Windows Defender custom scan, with active normal protection, script/archive scanning enabled, current signatures, no exclusions, native exit code 0, and no detections. Every game-file hash matched before and after scanning. Final run: `41218947705`, source commit `fe242de394fd069263ad5793246e9eada51f0ec8`; manifest SHA-256 `91d34fe39ad8486e25258560a636c6c0d36233999b69059f77b6cbbf713bd27e`. Engine `1.1.26100.4`, signatures `1.463.58.0`. Samples were not automatically uploaded for analysis.

The standard release also passed Chromium checks at 1280×720 without browser errors or unexpected network requests. Source and known-engine checks remain supplementary evidence. No verdict of false positive is being made for the old packed HTML; it stays withdrawn. No antivirus scan guarantees the absence of all malware.

The public `gh-pages` branch contains the exact scanned game bytes and the actual scan report/manifest. Pages activation is a separate hosting step, not a malware fix or security clearance. This runtime cannot directly open the github.io site due to its network policy.
