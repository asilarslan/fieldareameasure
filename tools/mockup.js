// Real app screenshots (1080×2400) → phone mockups with transparent background:
//   node tools/mockup.js <out-dir> <lang>:<key>=<png> ...   → <out-dir>/screen-<lang>-<key>.webp (720 px wide)
const { chromium } = require('playwright');
const fs = require('fs'); const path = require('path'); const os = require('os');
const { execFileSync } = require('child_process');
(async () => {
  const [out, ...pairs] = process.argv.slice(2);
  const b = await chromium.launch({ channel: process.env.PW_CHANNEL || undefined });
  const p = await b.newPage({ deviceScaleFactor: 1.35, viewport: { width: 600, height: 1300 } });
  await p.goto('file://' + path.join(__dirname, 'mockup.html'));
  for (const pair of pairs) {
    const [id, src] = pair.split('='); const [lang, key] = id.split(':');
    await p.evaluate(async d => { const i = document.getElementById('s'); i.src = d; await i.decode(); },
      'data:image/png;base64,' + fs.readFileSync(src).toString('base64'));
    const tmp = path.join(os.tmpdir(), `mock-${lang}-${key}.png`);
    await p.locator('#ph').screenshot({ path: tmp, omitBackground: true });
    execFileSync('cwebp', ['-quiet', '-q', '84', '-alpha_q', '90', '-resize', '720', '0', tmp, '-o', path.join(out, `screen-${lang}-${key}.webp`)]);
    console.log('ok', lang, key);
  }
  await b.close();
})();
