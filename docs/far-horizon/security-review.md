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

GitHub Pages deployment was verified through public run `41219520253`: Success, source `gh-pages`, reviewed commit `4537180a5d07fe74240e2674ee86d23074d60755`, successful build/deploy jobs, recorded URL `https://loganrossbryant-ai.github.io/hello-earth-demo/`. Pages is active. Live website navigation could not be tested from this runtime; local tests and uploaded file hashes were checked.

## Animation revision validation

The updated ordinary Web build passed a new scan: run `41227037912`, source
`81d1368b976c3ba4b345cbc23680f791d1522eea`, manifest SHA-256
`863db723d8df541ef0145bf21b469826fad3df797e48fe6e19a50047ee3656f3`.
Status `scan_passed`, native exit 0, no detections/error, matching hashes before
and after scanning. Active normal protection, script/archive scanning enabled,
no exclusions, engine `1.1.26100.4`, signatures `1.463.59.0`. Actual report:
`docs/far-horizon/defender-release-report.json` and private report branch
`codex/fh-defender-scan-41227037912-1`.

The exact standard animation build passed Chromium at 1280×720, including the
five-field save/restoration and new-class reset, without browser errors or
unexpected network requests. Separate checks passed all Session 1 story gates
and 166 steady foot contacts, with visible independent motion in every setting.
NPC recordings remain blocked on the ElevenLabs connection; no speech files
are claimed complete. Adding them will require a new build and scan.

Public animation release commit `07971c1af1de899ec831accf98b64e5ad15bccb2`
was deployed by Pages run `41227599343`, Status Success, on `gh-pages`.
The run records successful build/deploy jobs and the existing browser URL.
Verification used the public GitHub Actions summary, with exact-byte browser
checks locally; direct github.io access is still blocked by this runtime policy.

## Sessions 1–3 PC/iPhone publication — 2026-11-01

The user authorized the new publication. Active Windows Defender run
**41322320949**, review commit `a4fdcc3cb468f6a254d1cca0b63c4f77b4dda5e8`,
passed with native exit0, no detections/errors, signatures1.463.73.0, normal active
protection, script/archive scanning, no exclusions and matching hashes before
and after scan. Manifest SHA-256
`2f484806730de72363d1b11c01bfbdd0e71709a7b1dce430935d0641442cdc56`
covers22 ordinary game/preview/license files. See
`defender-pc-iphone-report.json` and `pc-iphone-release-verification.json`.

Exact release QA passed all64 beats at1280×720, save/reload, dialogue, three
gloss languages and reset/preservation with zero errors. PC shared-entry and
iPhone-size touch/rotation/reading tests passed with zero errors. A physical
iPhone and Safari engine were not tested; the official WebKit download was
blocked by network policy. No restriction was bypassed.

Public Pages commit `7953e570a3da1b236df1361e3e1cbcf2390237e3` adds only
`far-horizon/`, preserving the root and Alan Island game. Pages run41323549024
succeeded for that exact commit; hosted game-file hashes match the scan. URL:
https://loganrossbryant-ai.github.io/hello-earth-demo/far-horizon/play.html.
Direct live HTTP navigation remains unavailable in this runtime; deployment
verification used GitHub's actual successful run, commit and published tree.
Old scan/deployment entries above are historical. The packed HTML/ZIP remains
withdrawn and no absolute malware-free guarantee is made.
