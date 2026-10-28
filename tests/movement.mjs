import assert from 'node:assert/strict';
import { chromium } from '@playwright/test';

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || '/usr/bin/chromium', headless: true, args: ['--no-sandbox'] });
const context = await browser.newContext({ viewport: { width: 1440, height: 1050 } });
const page = await context.newPage();
const errors = [];
page.on('pageerror', error => errors.push(error.message));
const position = () => page.evaluate(() => ({ x: window.__gameScene.player.x, y: window.__gameScene.player.y }));
const hold = async (key, ms = 190) => { await page.keyboard.down(key); await page.waitForTimeout(ms); await page.keyboard.up(key); await page.waitForTimeout(65); };
const clickWorld = async (x, y) => {
  const box = await page.locator('canvas').boundingBox();
  assert.ok(box, 'The exploration canvas is visible');
  await page.mouse.click(box.x + x / 1280 * box.width, box.y + y / 780 * box.height);
};
const closeInteraction = async () => {
  await page.waitForFunction(() => window.__gameScene?.pausedByUI);
  await page.waitForTimeout(100);
  await page.keyboard.press('Escape');
  await page.getByRole('dialog').waitFor({ state: 'hidden' });
  await page.waitForFunction(() => window.__gameScene && !window.__gameScene.pausedByUI);
  await page.waitForTimeout(100);
};

try {
  await page.goto(process.env.BASE_URL || process.env.GAME_URL || 'http://127.0.0.1:5173', { waitUntil: 'networkidle' });
  await page.waitForFunction(() => window.__gameScene?.player && !window.__gameScene.pausedByUI);
  assert.equal(await page.evaluate(() => window.__gameScene.hasPhoto), true, 'The cinematic environmental art loads');
  for (const [key, axis, direction] of [
    ['w', 'y', -1], ['s', 'y', 1], ['a', 'x', -1], ['d', 'x', 1],
    ['ArrowUp', 'y', -1], ['ArrowDown', 'y', 1], ['ArrowLeft', 'x', -1], ['ArrowRight', 'x', 1],
  ]) {
    const before = await position();
    await hold(key);
    const after = await position();
    assert.ok((after[axis] - before[axis]) * direction > 12, `${key} moves the visible player in the expected direction`);
  }
  console.log('PASS: WASD and all four arrow keys move the character.');

  await hold('w', 1800);
  const blocked = await position();
  assert.ok(blocked.y >= 445 && blocked.y < 470, `Upper desk blocks movement before entering furniture (${blocked.y.toFixed(1)})`);
  await hold('w', 400);
  const stillBlocked = await position();
  assert.ok(Math.abs(stillBlocked.y - blocked.y) < 2, 'Holding a movement key cannot pass through the desk');
  await hold('s', 700);
  console.log('PASS: Furniture collisions block sustained keyboard movement.');

  await clickWorld(650, 655);
  await page.waitForFunction(() => window.__gameScene?.player && Math.hypot(window.__gameScene.player.x - 650, window.__gameScene.player.y - 655) < 12);
  console.log('PASS: Clicking the floor walks to the chosen position.');

  await clickWorld(260, 220);
  await page.getByRole('dialog', { name: 'Community noticeboard' }).waitFor({ timeout: 10000 });
  const atNotice = await position();
  assert.ok(Math.hypot(atNotice.x - 230, atNotice.y - 460) < 20, 'Clicking a noticeboard paths to its physical approach point');
  assert.equal(await page.evaluate(() => window.__gameScene.pausedByUI), true, 'An in-world interface pauses scene movement');
  await hold('d', 350);
  assert.deepEqual(await position(), atNotice, 'Character stays still while interacting with a document');
  await closeInteraction();
  await page.keyboard.press('e');
  await page.getByRole('dialog', { name: 'Community noticeboard' }).waitFor();
  await closeInteraction();
  console.log('PASS: Object click approaches and opens; E interacts; modal pauses movement.');

  for (const [x, y, title] of [[440, 300, 'Newsroom laptop'], [850, 385, 'A conversation with Maya'], [970, 340, 'Maya’s email'], [1210, 300, 'The courtyard door']]) {
    await clickWorld(x, y);
    await page.getByRole('dialog', { name: title }).waitFor({ timeout: 10000 });
    await closeInteraction();
  }
  console.log('PASS: Laptop, NPC, inbox and doorway are reachable through actual mouse controls.');
  assert.deepEqual(errors, [], 'No uncaught browser errors occurred');
  console.log('PASS: Movement smoke completed without uncaught browser errors.');
} finally {
  await context.close();
  await browser.close();
}
