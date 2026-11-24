// node tools/og.js → assets/img/og-<lang>.jpg (1200×630 share images), using content/og.json
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const texts = JSON.parse(fs.readFileSync(path.join(__dirname, '../content/og.json'), 'utf8'));
  const b = await chromium.launch({ channel: process.env.PW_CHANNEL || undefined });
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  for (const [lang, t] of Object.entries(texts)) {
    await p.goto('file://' + path.join(__dirname, 'og.html'));
    await p.evaluate(({ t, src }) => { document.getElementById('h').innerHTML = t.h; document.getElementById('p').textContent = t.p; document.getElementById('s').src = src; },
      { t, src: '../assets/img/' + t.screen });
    await p.waitForTimeout(300);
    await p.screenshot({ path: path.join(__dirname, `../assets/img/og-${lang}.jpg`), type: 'jpeg', quality: 85 });
  }
  await b.close();
})();
