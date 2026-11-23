# Art sources and processing

The assets were generated for The Broken Bridge with OpenAI Image Generation. No source image from another game was provided to the generator or included in the build. The tool did not request a purchase or an external asset subscription.

| Source original in `/workspace/generated_images/` | Production assets | Processing |
|---|---|---|
| `exec-eaf1435c-872d-4705-bdf3-668fdb0d3e43.png` | forest, current, front-left, front-right | WebP optimization; water and foreground masks extracted from registered regions |
| `exec-0750e7af-4a26-4a5c-975d-4ecdc08dc23b.png` | ranger-0 through ranger-3, ranger-portrait, scout-0 through scout-3, rack, depth, sign, flags, flag-0, flag-1 | Atlas split, chroma key, WebP optimization, normalized character feet |
| `exec-cd1e335b-131e-44bf-ad62-2f029c334c47.png` | broken, repaired, bridge-fill-0, bridge-fill-1 | Atlas split, chroma key, matched scale and abutment origin, cropped partial deck overlays |
| `exec-4291870d-90a6-434d-969c-1e721027233a.png` | board, rope, supplies, rack-loaded | Atlas split, chroma key, WebP optimization |

The art is original to this prototype and includes no intentionally replicated IP or reference-game assets. Gen-art originals remain in the workspace. Runtime assets are checked into `assets/`. [Generation prompts](IMAGEGEN_PROMPTS.md) and [preparation script](prepare_art.py) document the processing path. The asset and original checksums below identify the exact inputs and outputs.

```text
8dd933db4489dc05026cc16b248f9b7c05973deb879a490d373aba0da10e111f  assets/board.webp
31552fd805ffa26b58423b6ae62a2ba0b2b2102373b447d5da6465197ebfeb28  assets/bridge-fill-0.webp
d7aaa6992c4b0f328d870b8a4abffde7bc8a99dd0bc9cc065244fa0fdfe34c30  assets/bridge-fill-1.webp
aa1c3b0d08cd5ff7d061594f48339eece2dffd09b38fecebd02868e1ecf3dd9a  assets/broken.webp
5ccc05ef9193f8795ff887a2075f09e020563232ab2ab7feb005a0276ed93bfa  assets/current.webp
70c85092a6936049987f0bb902c42cfe2bc30f9c0b4f5d0240ff9a35b943f4e2  assets/depth.webp
f53e22812bdeb6954c4e99ce36a54fe7e426623b18ee275f00a33e17cf222388  assets/flag-0.webp
41ef68001a33eab6e775259cd0e0f1efa0c7fe300c99c1533e186327eae8eed5  assets/flag-1.webp
10b12637ed2d5c9af91cb1d934a9c903f1ee1f1d8508ddb78a0cfa34b35ff875  assets/flags.webp
05ab10ed78b042f6cd6c756d0f864ec3aa173527684568cd2ac7626ae87b5f4e  assets/forest.webp
a582c8a1966ba024e28d95d3c0d301a14b861bda12df2e395147599ff480fda7  assets/front-left.webp
12843dc249efca3b03f388c8234f1f1522979cc91705b653fb54ba0e0d0f6ea3  assets/front-right.webp
6a50b8854ff8428a9ee9ebac5809383f3ed5e0e7be01f60be1e4981f34ed7c5c  assets/rack-loaded.webp
c7e7ed4d80b23a669db70f9587c11732e2c8b17ae21f8b90dee80e6f25f4a220  assets/rack.webp
bf7abf0c4c29796b31632673c8968adf3669bf12e2650782455c4f98438eae7e  assets/ranger-0.webp
765b8fcfd6e0da6f0049746f93170b73341523c3187cc0ec5c163e59e7f7a430  assets/ranger-1.webp
b160278ecca62ed58061d5acc13266b21cfa36a6dedeffd94ffe91c414aae6b4  assets/ranger-2.webp
274fff81fc2b48da7aae469715fe5bb060f41eafe7749d875cf321d805edd11b  assets/ranger-3.webp
21aa167b4012fefdc4685caa38527ddaa18c480a26b0e112f7fd9c32a6c8fa80  assets/ranger-portrait.webp
3dba0e16420b36fbefbb3d39a8ab7bad1883eda3e47ae234ec916322791020c6  assets/repaired.webp
7b1457ef7c08ce4321d89f3472e684c31cb67b7464f504ffbf5b2088886b5030  assets/rope.webp
8fd9ab909b95e119d3e204d20693b7f355405209a9d2c92d77325da6add00bc4  assets/scout-0.webp
4a7644b678152bcffa6537c3e1b9767a59a11cb4f5c878a1cea237da9b379154  assets/scout-1.webp
a8d5ce89937a063a5822861b4d73cac70b049f3cb66d52cf6f9b7a3477b4664a  assets/scout-2.webp
c9795985842d6345bf0cbf7a370a2d84b5611551416525b74f4f1f59a389f08e  assets/scout-3.webp
8073a0dfe778a5a94cde2812c7f03d2814dc045daba12f13c2a7957b4cddb1b0  assets/sign.webp
8cb6f65d6f68d7ecbd8eb3d634b8688e2004c82ab54d1c5626acdb4b64a295c2  assets/supplies.webp
e3ed3e2978fb266076c44babfed7d6de2c9c26229fe895188f92e9a41c1a1612  /workspace/generated_images/exec-eaf1435c-872d-4705-bdf3-668fdb0d3e43.png
72dc91de2207843e9c448982638f4d42cfc776229a315d86074313a05aed1408  /workspace/generated_images/exec-0750e7af-4a26-4a5c-975d-4ecdc08dc23b.png
45735d166867773a4e64d5c33e769030a66f20d903e59a0aaa41bc5b9d6a613f  /workspace/generated_images/exec-cd1e335b-131e-44bf-ad62-2f029c334c47.png
98868fafe092f2a0c15fb47298bcbf5b3bff0886344a3094dcf9758b1dfde91f  /workspace/generated_images/exec-4291870d-90a6-434d-969c-1e721027233a.png
```
