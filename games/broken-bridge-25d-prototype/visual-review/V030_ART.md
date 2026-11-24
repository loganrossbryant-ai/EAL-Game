# Ranger clearing art direction — v0.3.0

The revision holds the shelter layout, river, light and sightline. It separates mountain and bank treatment, adds wet cedar canopy and a mossy foreground obstacle at distinct depths, and uses a fixed registered pair for the damaged and repaired deck. The same lantern, footing and weather carry between shots. A shelter dialogue shot, a closer repair shot and a wide exploration shot share the same world coordinates.

## OpenAI ImageGen original inputs

### exec-20e45035-9127-4a37-96ef-308fee0152aa.png

Production game sprite atlas, three equal-width columns in a single wide rectangular image, pure flat #ff00ff chroma-key background (no shadow on background, no captions, no borders, no UI). Original objects for richly detailed late-afternoon Pacific Northwest forest adventure after a storm. Each asset touches no cell edge. LEFT THIRD: large gnarled brown and dark evergreen cedar branch with dangling intricate needles and bristly hanging moss, silhouette extended sideways like a canopy, meant to be placed at top-left foreground; realistic original painted game asset with light from upper left. MIDDLE THIRD: low wet moss-covered river boulder and fern clump, textured rock and needles, silhouette low and broad with transparent pad on all sides, for actors to pass behind on the edge of a gravel trail. RIGHT THIRD: one downed broken storm branch, mud-covered butt with split wood and water-darkened torn ropes, broad horizontal footprint and strands, will sit directly at the base of an unsafe bridge. Natural material detail, no duplicated assets and distinct readable silhouettes. Painterly realism, dark cool forest shadows and warm natural light from upper left.

### exec-1e0c790a-34ad-4f14-a8d5-243683c7bfba.png

Edit this original chroma-key game asset pair. Deliver exactly the same two equal side by side cells (left damaged bridge, right repaired bridge), same pure #ff00ff background and camera, no ground or extra assets. Preserve positions, alignment, silhouette and wooden abutments of both assets precisely. Keep warm rainy cypress color and amber late-afternoon rim light. The RIGHT restored state remains continuous, with taut fresh hemp safety rope and its pale central deck. On the LEFT, make the missing deck very legible at small game scale: enlarge the central void vertically to about 50 percent of the visible walk surface; widen it to the sound side support rails; tear the right handline off with loose frayed rope and jagged timber ends curling into the open hole; retain sturdy straight dark timber stringers at the very outer sides so two preassembled deck boards can span the opening crosswise. Distinguish two clear flat seating ledges at near and far ends of the gap with wet sawn wood. Keep all contact points and camera angles matched. Natural wear and storm damage, crisp workpiece edges. No UI, no lettering, no erasing the chroma magenta key.

The bridge edit used the original v0.2 chroma-key sheet as input. Only project-owned game artwork was supplied to the generator. No reference game art was copied.

## Source and derived assets

- The foreground atlas produced `storm-canopy`, `storm-boulder` and `storm-debris`.
- The edited bridge atlas produced `bridge-damaged-v3`, `bridge-restored-v3` and the two registered deck patch layers.
- The original v0.2 character sheet produced the v3 character frames and dialogue portrait with edge despill. The original textures remain available.
- The v0.2 forest plate produced `scenery-distance` and the feathered `scenery-bank`.

The actual source sheets are under `originals/`. Reproduce the conversion with `python3 visual-review/prepare_v030.py` from this project. Uses Pillow and NumPy.

```text
72dc91de2207843e9c448982638f4d42cfc776229a315d86074313a05aed1408  visual-review/originals/exec-0750e7af-4a26-4a5c-975d-4ecdc08dc23b.png
2fd0c7949a4c7ffd3af58909eef21f8d1faf3cd2e555c62097e5d79694bcf281  visual-review/originals/exec-1e0c790a-34ad-4f14-a8d5-243683c7bfba.png
1367d9e47c4a7fed5eb2ff70d1ee4ede0fc104fbbd54ac74f3256bf701060c53  visual-review/originals/exec-20e45035-9127-4a37-96ef-308fee0152aa.png
76bc3607596d3dab978e9c46161757681254c0ee1c33710093474b7decfccb8e  assets/bridge-damaged-v3.webp
3328fc67bcfeba8c3f60410485cb77f5a0143bfac90e369f48f974dd8c0677ed  assets/bridge-patch-v3-0.webp
ede3c168be9d21567979274dababff9b5a78ce62fbd6a57c7024573dbbb15264  assets/bridge-patch-v3-1.webp
4aae4d7f57ee1e14ddc54151d4e37188ca77c8b9c4904e5409a81d49478f537b  assets/bridge-restored-v3.webp
fac89ea8700913163f61dbddfb5d3e5fed74c55707a4b7aebd97c22796e268a2  assets/ranger-v3-0.webp
838e0c587c13f028472760fc5c19b79f37a974561c49fa3f763453df1510035c  assets/ranger-v3-1.webp
94d4ba9ba89300e60aef228531661a34dbfcf9f95ca16f1fc6eb133e65248063  assets/ranger-v3-2.webp
385d3992dc6d9cfecc404c7519aad4f7438636ceea168e6e5abe44fe632fc8a7  assets/ranger-v3-3.webp
bc37006aca6e24f2b16020d8424584b5d2575255d91407ef4807af242ef070fc  assets/ranger-v3-portrait.webp
b10f4420d7628ac6f041aeb3fd7850714eda5a52079edffb330aa877367e709a  assets/scout-v3-0.webp
6cbb23b479f228b7e276c6b335e25db836131b6a76af6a9148b557c636b72f03  assets/scout-v3-1.webp
f927ac2cdb57ce4d27e0682690c409c859646e122c21d36a9d31417acc1cbb25  assets/scout-v3-2.webp
ab17587d82c1ef870811a682122f55b09ccabaa2c37fdd6331f76652d1be0f28  assets/scout-v3-3.webp
bb2fa92ee3636935eb824259157abc0c4ce468578b7bbb3f0b4adf5d4e4dac20  assets/scenery-bank.webp
bc032bd5400ce90959752d4e03334272cd4089294ca214c2025e3fc8abf17534  assets/scenery-distance.webp
ad2385839085523b221dd10f7ef99d269a7e730c452c4d7e6609ee8ad696586c  assets/storm-boulder.webp
e82a09e8357134d65955697a356881e2eb1b8be32f33c6888ddf20e9279a8f84  assets/storm-canopy.webp
0c4b6b795af8d3fa93a69f894088d82ea3994fd38282f0f2f87e2770d9aefbb4  assets/storm-debris.webp
```
