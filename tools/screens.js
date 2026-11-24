// Prepare app screenshots for the site: crop Android's own status bar (24 dp at 3.5x = 84 px) and record the
// app colour behind it, so the site can draw a clean status bar in the phone frame.
//   node tools/screens.js <out-dir> <lang>:<key>=<png> ...   (Node 20+, playwright, cwebp)
// Writes <out-dir>/screen-<lang>-<key>.webp and merges colours into content/screens.json.
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path'); const os = require('os');
const { execFileSync } = require('child_process');
const SB = 84;
(async () => {
  const [out, ...pairs] = process.argv.slice(2);
  const jsonPath = path.join(out, '../../content/screens.json');
  const meta = fs.existsSync(jsonPath) ? JSON.parse(fs.readFileSync(jsonPath, 'utf8')) : {};
  const b = await chromium.launch({ channel: process.env.PW_CHANNEL || undefined }); const p = await b.newPage();
  for (const pair of pairs) {
    const [id, src] = pair.split('=');
    const [lang, key] = id.split(':');
    const res = await p.evaluate(async ({ data, SB }) => {
      const im = new Image(); im.src = data; await im.decode();
      const c = document.createElement('canvas'); c.width = im.width; c.height = im.height - SB;
      const x = c.getContext('2d'); x.drawImage(im, 0, SB, im.width, im.height - SB, 0, 0, im.width, im.height - SB);
      const k = document.createElement('canvas'); k.width = im.width; k.height = SB; k.getContext('2d').drawImage(im, 0, 0);
      const px = k.getContext('2d').getImageData(6, SB - 6, 1, 1).data;
      return { url: c.toDataURL('image/png'), rgb: [px[0], px[1], px[2]], w: im.width, h: im.height - SB };
    }, { data: 'data:image/png;base64,' + fs.readFileSync(src).toString('base64'), SB });
    const tmp = path.join(os.tmpdir(), `scr-${lang}-${key}.png`);
    fs.writeFileSync(tmp, Buffer.from(res.url.split(',')[1], 'base64'));
    execFileSync('cwebp', ['-quiet', '-q', '82', '-resize', '645', '0', tmp, '-o', path.join(out, `screen-${lang}-${key}.webp`)]);
    const [r, g, bl] = res.rgb; const dark = (0.299 * r + 0.587 * g + 0.114 * bl) < 128;
    meta[`${lang}-${key}`] = { bg: `rgb(${r},${g},${bl})`, dark, h: Math.round(645 * res.h / res.w) };
    console.log(lang, key, meta[`${lang}-${key}`]);
  }
  await b.close();
  fs.writeFileSync(jsonPath, JSON.stringify(meta, null, 1));
})();
