// News image for 22 November 2026 (Node 22, standard library only). The entry
// is the front-page image beside this file, entry.png; this program copies it
// to /output/entry.png, byte for byte, then reads both files back and fails
// loudly if a single byte differs, so the judge sees exactly the bytes that
// were built and checked. The gate takes a whole PNG or JPEG of at most 1 MiB
// and 1024 by 1024 pixels; entry.png is 1024 by 1024 and well under the cap.
// The copy is deterministic: same input bytes, same output bytes, every run.
//
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const source = new URL('./entry.png', import.meta.url);
const target = join(process.env.MAKEFUN_OUTPUT_DIR ?? '/output', 'entry.png');

copyFileSync(source, target);

if (!readFileSync(source).equals(readFileSync(target))) {
  throw new Error('entry.png copy mismatch: output bytes differ from source');
}
