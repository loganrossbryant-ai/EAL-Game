# v0.4.0 animation sources

The atlas edit used the existing project-owned character sheet `exec-0750e7af-4a26-4a5c-975d-4ecdc08dc23b.png` as an identity reference. The new plates are original OpenAI ImageGen outputs. Their bytes are in `v040-originals/`. The game uses the existing v0.3 environment and repair texture pair. No reference-game assets are included.

The two locomotion plates have six individually authored frames in each of four directions and the action plate includes carry, fit, listening, inspection and handoff poses. The conversion script keys magenta, removes fringe, preserves a common scale by role and registers each silhouette to a shared boot baseline and torso axis. Walking phase follows accepted world displacement and direction. It remains active for scout input with reduced motion. Carrying uses the same directional gait with a separate depth-sorted carried prop and an authored stationary hold. The generated alternate carry-stride pose is retained as source for later work.

Run `python3 visual-review/prepare_v040.py` from the prototype folder to regenerate the frame files from the included PNGs.

### scout · exec-7cfe68bd-8f94-4138-af10-1507d998ae92.png

Use the reference sheet only for exact recognizable identity and painted realistic game-asset style. Generate a professional animation atlas for the teal rain jacket, burgundy knit cap teenage scout with rust backpack in the SECOND row. EXACT exact 6 columns and 4 rows, equal cells, full body feet included, each centered, PURE solid #ff00ff throughout background, no labels, no shadows, no borders. Same character scale and identity on every frame. Fixed slightly elevated 2.5D camera. TOP ROW six sequential stepping frames walking SCREEN RIGHT. SECOND ROW six sequential stepping frames walking SCREEN LEFT. THIRD ROW six frames walking TOWARDS camera (front three-quarter, face visible). FOURTH ROW six frames walking AWAY from camera, back of head and jacket visible, no face. Each row a genuine 6-frame cycle in this order: frame 1 right heel forward contact; frame 2 right leg takes full weight while left toes lift; frame 3 left leg passes under torso; frame 4 LEFT heel forward contact; frame 5 left leg takes weight and right toes lift; frame 6 right leg passes under torso. Opposing arm swings with feet. Hip height and exact boot ground line consistent. Same head size, realistic silhouette and fabric, tiny natural movement. Never repeat a pose across each row. Reference painterly wet forest game styling. Tight cell, objects never touch cell boundary. Landscape atlas. Only character sprites.

### ranger · exec-a47bc4a0-4bdc-4d2d-a972-6aadbaf181d5.png

Use the reference sheet only for exact recognizable identity and painted realistic game-asset style. Generate a professional animation atlas for the East Asian woman park ranger with amber rain jacket, dark trousers, utility satchel and field hat in the TOP row. EXACT exact 6 columns and 4 rows, equal cells, full body feet included, each centered, PURE solid #ff00ff throughout background, no labels, no shadows, no borders. Same character scale and identity on every frame. Fixed slightly elevated 2.5D camera. TOP ROW six sequential stepping frames walking SCREEN RIGHT. SECOND ROW six sequential stepping frames walking SCREEN LEFT. THIRD ROW six frames walking TOWARDS camera (front three-quarter, face visible). FOURTH ROW six frames walking AWAY from camera, back of head and jacket visible, no face. Each row a genuine 6-frame cycle in this order: frame 1 right heel forward contact; frame 2 right leg takes full weight while left toes lift; frame 3 left leg passes under torso; frame 4 LEFT heel forward contact; frame 5 left leg takes weight and right toes lift; frame 6 right leg passes under torso. Opposing arm swings with feet. Hip height and exact boot ground line consistent. Same head size, realistic silhouette and fabric, tiny natural movement. Never repeat a pose across each row. Reference painterly wet forest game styling. Tight cell, objects never touch cell boundary. Landscape atlas. Only character sprites.

### actions · exec-afcfab3c-b415-4674-93b9-d0b4e790306f.png

Create a chroma-key production character sheet matching the two original reference people precisely, six isolated full-body poses, exact 3 equal columns by 2 equal rows, pure #ff00ff flat background, no shadows or markings. All complete boots, consistent scale, 10 percent cell margins. TOP row the teen scout (teal rain jacket and burgundy knit hat with rust backpack) poses left to right: stationary carrying a flat board with BOTH EMPTY forearms extended horizontally at abdomen (do not draw the board, game layers it); one step walking to the right with forearms in exact same carrying pose; bending knees and reaching forward at hip height to seat a board, EMPTY hands. BOTTOM row the woman ranger (amber rain jacket, brim hat and dark trouser/satchel) poses left to right: crouching slightly and reaching to check bridge deck, standing upright listening with one hand on belt, standing with both empty hands presenting a supply pack (do NOT depict pack). Slightly elevated view, faces three-quarter right, worn natural material, painted realism, match characters exactly. Every figure centered in cell.

## Asset identity

```text
8b91620f6dcb470f1b58dd1ed6977d19a342c22b7f50b67fae2d769a30142e06  visual-review/v040-originals/exec-7cfe68bd-8f94-4138-af10-1507d998ae92.png
66eb425cf233e2b4cf2c8e58f57c2fb3a921b18b6daf521eb865b9ebb8e12148  visual-review/v040-originals/exec-a47bc4a0-4bdc-4d2d-a972-6aadbaf181d5.png
a45b1b956429d4bd52a3257b9610f0510a35c978e613a8f5c07eb5f1c292f17e  visual-review/v040-originals/exec-afcfab3c-b415-4674-93b9-d0b4e790306f.png
495a29ff29aa449d2ef4d89a98a1bd02845f6edca9bec449b5a3a2b439c53ec4  assets/ranger-v4-down-0.webp
04c00b8b9282be895748c75bd385e6931e9e973e12537bc3f36ebeaa7b509530  assets/ranger-v4-down-1.webp
aecbb7814a35bfebc9812c34c5fc6e7d687d9b5c4e81359d2941d4f19ee7ab49  assets/ranger-v4-down-2.webp
a99103f438b08fb8f7eba21cef4f5c5b561a7a37763f3b22b8618dd5bc5fe73b  assets/ranger-v4-down-3.webp
4cf8cb8eefd3620018ca5c0a2c5ee7f781bcb66cec6199ced71dc41e3e283055  assets/ranger-v4-down-4.webp
33781d1df059a02cad60239146d4bb6903bf153a91d9b66483473bb26b6052fc  assets/ranger-v4-down-5.webp
4c7e5b72d2f5dabdd9920893082c97ce57e687c81c793339f2534370ece12fbc  assets/ranger-v4-handoff.webp
0e8200fddae8fd9fcdbf7bbbebef11b8585e685ce8efdde59fc91e2d9b4c9aad  assets/ranger-v4-inspect.webp
012a7faa64ea450edb3e631c0564e027648617eb7eff63c7d60b0e903d44ff01  assets/ranger-v4-left-0.webp
741a0fc072149fbf2527ea067ad7d6601a260de639fa08c89936469849517527  assets/ranger-v4-left-1.webp
9f68440e76c0033bc142818f3872161203ecfbe9d6a57de5893824fa8671bc9b  assets/ranger-v4-left-2.webp
81e5724ba356f3bf4b0d3050a6078f341e179e64f91ef1689ec73f828d1fd375  assets/ranger-v4-left-3.webp
2e21faf3da8bc15aeaf11004ceb57d5d71bbf5c769ea3226b03b270d12579a12  assets/ranger-v4-left-4.webp
73dd446be7bdf61d4430c681435b1fe294a83158e75cb29686d6c0326bd49258  assets/ranger-v4-left-5.webp
0671ac8eac0c0b84e937c7433e974f9a2fb982ae41c7a24004f668761f116d3d  assets/ranger-v4-listen.webp
e8d8a72a22e3672b18ffa5faee9dfd79ba4169fceb2f73cfbf9af0a9424936f4  assets/ranger-v4-right-0.webp
b37f8a7dcad7e5f96dcb28b6c66ac4b27938d8818b9ce1edb6fef8c75b474342  assets/ranger-v4-right-1.webp
77e88acb17ca9ac3f1732ff1184ed7a978376bf2ed6acff4f6f5726c10d17e5a  assets/ranger-v4-right-2.webp
43e28dc88f9cbf5f67577113b75940122d34d284576c3ef3824e3c6ed0852ab3  assets/ranger-v4-right-3.webp
1c8389579e664d16431a674b50cc7b25d22d976dcfc61c6d238725d2bcbbe6fb  assets/ranger-v4-right-4.webp
3514d65b02abc1c32f2cdc56b0294dd89be81983c85fa76cf4c84e1c0c1d3f96  assets/ranger-v4-right-5.webp
2fae543ae2ac7cc53edb5e98fe117ea80262f69497aaa151fc1f5330a037324d  assets/ranger-v4-up-0.webp
179007b33f3c31edaa2245e2b0772be161079e31babac4fc4fe8937ee92f238c  assets/ranger-v4-up-1.webp
f31cdf492899c218ecb9ba1b0ec1243dcb1992a5b083ec335151a33fcec74f75  assets/ranger-v4-up-2.webp
7bc0ad5f194dbf0ea5ae5196afdfaa0a32cb3cd29319897410d74f9f684b7535  assets/ranger-v4-up-3.webp
1efd99e3cadb0ab2208fb8b16cbf3affabfb9cd42ba0fa14f545584526d2cce3  assets/ranger-v4-up-4.webp
77635f6afc4ca8f09e132ea9a4ea2c47101cff01543b438f8f5ce12300b72423  assets/ranger-v4-up-5.webp
04274cdfe8501e0867732811bed6db9b28570a7e716eb0934ca560892614a864  assets/scout-v4-carry-step.webp
3ca338cb440e8a81cbf2b2047230a0e9390758fdbc587b23dab78b682bdaf6fd  assets/scout-v4-down-0.webp
9b807920fcf187feeb902474cae8adce87fb2cce2f5a98995896d27f79fe0494  assets/scout-v4-down-1.webp
f93a383d3acfdac29316d1f71822b89ed5162ebe47a26dedaece5514438faf7b  assets/scout-v4-down-2.webp
93b20dd0f2dc05b0bebcb129ec9a8e52321adbdad38443280462435090889c1a  assets/scout-v4-down-3.webp
19b375ab1f43b4e98c57b30920323e02fac00b83317aa9f1f9a6ecbe7b548ae0  assets/scout-v4-down-4.webp
17a744b15b8dcb50579598c62672bd74890b29b0466b852a8049875ce648ccfe  assets/scout-v4-down-5.webp
355d9a93045d4e55dc4b7c29ef61d2d2de43086699b7a1baca9dcd082ebc6da1  assets/scout-v4-fit.webp
5bbf850d773f58f397daa4661a06f51d349cdd6558c5df59c7d671fd1e33cafe  assets/scout-v4-hold.webp
7648a5a6bb5031f9c924bd8bbe67f8c40416dc84533a59a2d3bc3b2b38ef97d0  assets/scout-v4-left-0.webp
b354127faf0b157ad7fb2ba08cbdfe0b5f6a708768b152d42f146459e9625c70  assets/scout-v4-left-1.webp
f80db5da7dea42d85b66b011c4c4f329fa3cd81d117e40e1f587dfe8a05f4f31  assets/scout-v4-left-2.webp
33252a72e5519917f08cebb047560f5e429dc71ebf584a33e62cc98056a4c460  assets/scout-v4-left-3.webp
f4b15db6920701142b1dd93158e7829d3636ce4ddbd5d5933803666817ace425  assets/scout-v4-left-4.webp
7164e477cd0268ee597ab4ab4616b87253c4484e6862f3b9e2c0ead14965ed16  assets/scout-v4-left-5.webp
53f977d0913e3e62b6ea53fbac2a70c655494da362dd5f8e56be18b61f89b5e5  assets/scout-v4-right-0.webp
92df3f11d9c47b4eb2ff53d88c4da6603d2638a9777a5c3878288a56bb7d0dde  assets/scout-v4-right-1.webp
597d336c343b9d6b28a55532f021e9141f6ae53527efac234566aad021e2bd7f  assets/scout-v4-right-2.webp
603481423b4509d0908a7b2bc0edc4a04fb2b67b222177cb319c647d14b6f863  assets/scout-v4-right-3.webp
8a66210980c40f352defe9fffe30664c96a85c8a4557a67a5fea600cdcba7a58  assets/scout-v4-right-4.webp
13d6113e21f546e1a7ca8840f04e2eef82d10d02f98d7272c29b15a7e2838ac0  assets/scout-v4-right-5.webp
73a2f81f320a42ceda678faa44fac6f78e8697d32ed4ea3babdce63a13dc0724  assets/scout-v4-up-0.webp
2677420913251048104ae5edeb0023c2782b765f9ca749aed233058c0d962d2b  assets/scout-v4-up-1.webp
ac4d01725fc8bf3bdaf44c8e88f28495e08fae87f12da77c42f4da84b209cd6c  assets/scout-v4-up-2.webp
b2311fe823e9ad927d183a64b6a623ec365cc80461a1d4dc0b176bbd2cd7432b  assets/scout-v4-up-3.webp
6bdaafd7ed2d5469ecf3292eb384b7e91894330c0727dc5464e7bc7682b1203f  assets/scout-v4-up-4.webp
94daa522356fdf52937492dfda71657594cd7be4e376e0de0e8ab09ff7f38b01  assets/scout-v4-up-5.webp
```
