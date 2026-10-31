"""Exercise real browser movement and measure planted feet and living scenery.

Scene fixtures isolate visual checks; browser_slice.py still traverses the
actual gated Session 1 story. This test never advances story via debug globals.
"""
import asyncio
import io
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image
from playwright.async_api import async_playwright

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/far-horizon-tests/motion"
URL = os.environ.get("FH_URL", "http://127.0.0.1:8080")


async def run():
    OUT.mkdir(parents=True, exist_ok=True)
    errors = []
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(executable_path="/usr/bin/chromium", args=[
            "--no-sandbox", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--disable-dev-shm-usage"])
        context = await browser.new_context(viewport={"width": 1366, "height": 768})
        page = await context.new_page()
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        await page.goto(URL)
        await page.wait_for_function("window.farHorizonTestState", timeout=90000)
        await page.mouse.click(245, 348)
        await page.keyboard.down("d")
        await page.wait_for_timeout(1200)
        samples = []
        for i in range(44):
            samples.append(await page.evaluate("window.farHorizonTestState"))
            await page.wait_for_timeout(65)
        await page.keyboard.up("d")
        (OUT / "walk-samples.json").write_text(json.dumps(samples))
        assert all(member["rig"] for sample in samples for member in sample["party"])
        plants = []
        for before, after in zip(samples, samples[1:]):
            if before["clock"] == after["clock"]: continue
            for old, new in zip(before["party"], after["party"]):
                if min(old["vx"], new["vx"]) < 139: continue
                for a, b in zip(old["feet"], new["feet"]):
                    if a["stance"] and b["stance"] and a["contact"] == b["contact"]:
                        drift = abs(b["world_x"] - a["world_x"])
                        assert drift < 0.005, f"Foot slid during steady stance: {drift}px"
                        assert b["height"] == 0
                        plants.append(drift)
        assert len(plants) >= 20, "Insufficient steady contact observations"
        assert len({round(s["party"][0]["gait"], 2) for s in samples}) > 18
        assert len({round(m["gait"], 1) for m in samples[-1]["party"]}) == 4
        for sample in samples[6:]:
            for a, b in zip(sample["party"], sample["party"][1:]):
                assert 79 < a["x"] - b["x"] < 94
                assert b["vx"] > 135, "Follower paused during a steady walk"
        await page.wait_for_timeout(2000)
        stopped = await page.evaluate("window.farHorizonTestState")
        assert all(abs(m["vx"]) < 1 for m in stopped["party"]), stopped["party"]
        await page.screenshot(path=str(OUT / "settled-idle.png"))
        await page.keyboard.down("a")
        await page.wait_for_timeout(130)
        await page.screenshot(path=str(OUT / "planted-turn.png"))
        await page.wait_for_timeout(1700)
        left = await page.evaluate("window.farHorizonTestState")
        assert all(m["facing"] == -1 and m["vx"] < -130 for m in left["party"])
        await page.screenshot(path=str(OUT / "walk-left.png"))
        await page.keyboard.up("a")
        await context.close()

        motion = {}
        fixtures = {
            "terminal": [(520, 120, 1140, 245), (0, 440, 185, 690)],
            "launch": [(1025, 445, 1225, 520)],
            "habitation": [(0, 440, 190, 690)],
            "bridge": [(920, 150, 1330, 412), (900, 445, 1300, 490)],
            "ending": [(920, 150, 1330, 412)],
        }
        for scene, regions in fixtures.items():
            ctx = await browser.new_context(viewport={"width": 1366, "height": 768})
            fixture = {"version": 1, "scene": scene, "position": 520, "flags": {"begun": True}, "cue": 0}
            await ctx.add_init_script("localStorage.setItem('far-horizon-session1-v1'," + json.dumps(json.dumps(fixture)) + ")")
            tab = await ctx.new_page()
            tab.on("pageerror", lambda error: errors.append(str(error)))
            tab.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
            await tab.goto(URL)
            await tab.wait_for_function("window.farHorizonTestState", timeout=90000)
            await tab.keyboard.press("Escape")
            await tab.wait_for_timeout(1200)
            first = await tab.screenshot(path=str(OUT / f"{scene}-a.png"))
            await tab.wait_for_timeout(1500)
            second = await tab.screenshot(path=str(OUT / f"{scene}-b.png"))
            a = Image.open(io.BytesIO(first)).convert("RGB")
            b = Image.open(io.BytesIO(second)).convert("RGB")
            changes = []
            for region in regions:
                delta = np.abs(np.asarray(a.crop(region), dtype=float) - np.asarray(b.crop(region), dtype=float))
                changed = float((delta.max(axis=2) > 3).mean())
                assert changed > 0.0003, f"No visible independent motion in {scene}: {region}, fraction {changed}"
                changes.append(round(changed, 5))
            motion[scene] = changes
            print(json.dumps({"scene": scene, "changed_fractions": changes}), flush=True)
            await ctx.close()
        await browser.close()
    assert not errors, errors
    result = {"passed": True, "steady_contacts_checked": len(plants), "max_contact_drift_px": max(plants),
              "four_continuous_rigs": True, "staggered_gaits": True, "followers_maintain_speed": True,
              "idle_and_both_directions": True, "independent_scene_motion_changed_fractions": motion,
              "browser_errors": errors}
    (OUT / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result), flush=True)


if __name__ == "__main__":
    asyncio.run(run())
