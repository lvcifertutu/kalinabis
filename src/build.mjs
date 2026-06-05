import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const src = (...parts) => join(__dirname, ...parts);
const out = join(__dirname, '..', 'grimorio.html');

const JS_FILES = [
  'data.js',
  'proyectos.js',
  'particles.js',
  'tronos.js',
  'audio.js',
  'ui.js',
  'chat.js',
  'modal.js',
  'bosque.js',
  'luna.js',
  'sigilos.js',
  'tarot.js',
  'init.js',
];

const HTML_PARTS = [
  'head.html',
  'pre-app.html',
  'panels.html',
];

const JS_WRAP = (code) => `<script>\n${code}\n</script>`;

const HTML_AFTER_SCRIPT = [
  'overlays.html',
  'tail.html',
];

function read(name) {
  return readFileSync(src(name), 'utf-8');
}

let output = '';

// HTML antes del script
for (const part of HTML_PARTS) {
  output += read(part);
}

// JS concatenado envuelto en <script>
let jsBundle = '';
for (const file of JS_FILES) {
  jsBundle += read(file) + '\n';
}
output += JS_WRAP(jsBundle);

// HTML después del script
for (const part of HTML_AFTER_SCRIPT) {
  output += read(part);
}

writeFileSync(out, output, 'utf-8');
console.log('✓ Build complete → grimorio.html');
