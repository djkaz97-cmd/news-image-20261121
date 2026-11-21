// news-image-20261121 — make.fun entry (program/v1, Node 22, standard library only).
// The front page is pre-rendered at build time (build/render.py) and ships as
// entry.png beside this file. The program validates the image against the
// competition's gate limits and copies it to the output directory. No network,
// no clock, no randomness: two runs write exactly the same bytes.
//
// Local test: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const MAX_BYTES = 1_048_576; // 1 MiB gate cap
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const here = dirname(fileURLToPath(import.meta.url));
const image = readFileSync(join(here, 'entry.png'));

if (image.length < 8 || !image.subarray(0, 8).equals(PNG_MAGIC)) {
  console.error('entry.png: not a PNG (bad magic)');
  process.exit(1);
}
if (image.length > MAX_BYTES) {
  console.error(`entry.png: ${image.length} bytes exceeds the ${MAX_BYTES}-byte cap`);
  process.exit(1);
}

// IHDR: the first chunk must describe an image within the 1024x1024 gate cap.
if (image.length < 24 || image.toString('latin1', 12, 16) !== 'IHDR') {
  console.error('entry.png: missing IHDR chunk');
  process.exit(1);
}
const width = image.readUInt32BE(16);
const height = image.readUInt32BE(20);
if (width < 1 || height < 1 || width > 1024 || height > 1024) {
  console.error(`entry.png: ${width}x${height} exceeds the 1024x1024 cap`);
  process.exit(1);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const dest = join(outDir, 'entry.png');
writeFileSync(dest, image);
console.log(`wrote ${dest} (${image.length} bytes, ${width}x${height})`);
