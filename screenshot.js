const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1280, height: 800 });
  await page.goto('file:///home/aliple/.openclaw/workspace/trading-journey-prototype.html');
  await page.screenshot({ path: 'prototype-screenshot.png', fullPage: true });
  await browser.close();
})();
