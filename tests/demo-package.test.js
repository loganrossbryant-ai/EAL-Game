import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';

// Validate the deliverable students actually download, rather than only the
// source bundle. Packaging must preserve JavaScript syntax and embed its assets.
const html = readFileSync(new URL('../demo/Signal-Play.html', import.meta.url), 'utf8');
const scripts = [...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)];
const styles = [...html.matchAll(/<style\b[^>]*>([\s\S]*?)<\/style\s*>/gi)];
const markup = html.replace(/<script\b[^>]*>[\s\S]*?<\/script\s*>/gi, '')
  .replace(/<style\b[^>]*>[\s\S]*?<\/style\s*>/gi, '');

test('downloadable game contains a complete, syntactically valid inline module', () => {
  assert.equal(scripts.length, 1, 'Expected exactly one embedded application script.');
  assert.match(scripts[0][1], /\btype\s*=\s*["']module["']/i);
  assert.ok(scripts[0][2].length > 100000, 'The complete game bundle must be embedded.');
  const result = spawnSync(process.execPath, ['--check', '--input-type=module'], {
    input: scripts[0][2],
    encoding: 'utf8',
    maxBuffer: 10 * 1024 * 1024,
  });
  assert.ifError(result.error);
  assert.equal(result.status, 0, `The packaged application must parse before delivery.\n${result.stderr}`);
});

test('downloadable game has inline styles and no external script, stylesheet, or artwork dependencies', () => {
  for (const [, attributes] of scripts) {
    assert.doesNotMatch(attributes, /\bsrc\s*=/i, 'Scripts must be embedded for offline use.');
  }
  assert.ok(styles.length > 0 && styles.some(([, css]) => css.length > 1000), 'Application CSS must be embedded.');
  assert.doesNotMatch(markup, /<link\b[^>]*\brel\s*=\s*["'](?:stylesheet|modulepreload|preload)["']/i);
  assert.doesNotMatch(markup, /<(?:img|source)\b[^>]*\bsrc(?:set)?\s*=\s*["'](?!data:)[^"']+/i);
  for (const [, css] of styles) {
    assert.doesNotMatch(css, /@import\b/i, 'CSS cannot import an external stylesheet.');
    assert.doesNotMatch(css, /url\(\s*["']?(?!data:|#)[^\s"')][^)]*\)/i, 'CSS assets must be embedded.');
  }
  assert.doesNotMatch(scripts.map(([, , script]) => script).join('\n'), /["']\/assets\/[^"']+\.(?:webp|png|jpe?g|svg)["']/i);
});

test('both explorable environments have real embedded WebP artwork', () => {
  const script = scripts.map(([, , code]) => code).join('\n');
  for (const name of ['media-room-photo', 'courtyard-photo']) {
    const embedded = script.match(new RegExp(`(["'])${name}\\1\\s*,\\s*(["'])data:image/webp;base64,([A-Za-z0-9+/=]+)\\2`));
    assert.ok(embedded, `${name} artwork must be embedded in its actual Phaser image declaration.`);
    const bytes = Buffer.from(embedded[3], 'base64');
    assert.equal(bytes.toString('ascii', 0, 4), 'RIFF');
    assert.equal(bytes.toString('ascii', 8, 12), 'WEBP');
    assert.ok(bytes.length > 10000, `${name} must contain the full artwork.`);
    assert.equal(bytes.readUInt32LE(4) + 8, bytes.length, `${name} must be a complete WebP file.`);
  }
});
