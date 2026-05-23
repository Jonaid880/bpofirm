// Capture screenshots of the service-page blocks at multiple states.
// Usage: node preview/screenshot.js
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');

const OUT = path.join(__dirname, 'screenshots');
fs.mkdirSync(OUT, { recursive: true });

const url = 'file://' + path.join(__dirname, 'index.html');

const desktop = { width: 1440, height: 900 };
const mobile  = { width: 390,  height: 844 };

(async () => {
	const browser = await chromium.launch();

	async function shootHeroStates(viewport, prefix) {
		const ctx = await browser.newContext({ viewport, deviceScaleFactor: 2 });
		const page = await ctx.newPage();
		await page.goto(url, { waitUntil: 'networkidle' });

		const states = [
			{ name: 'initial',    progress: 0,    label: 'Hero — initial (banner)' },
			{ name: 'mid-expand', progress: 0.5,  label: 'Hero — mid-expand (50%)' },
			{ name: 'expanded',   progress: 1,    label: 'Hero — fully expanded' },
		];

		for (const s of states) {
			await page.evaluate(p => window.__setHeroProgress(p), s.progress);
			await page.evaluate(label => { document.getElementById('preview-label').textContent = label; }, s.label);
			await page.waitForTimeout(400);
			await page.locator('#hero').screenshot({
				path: path.join(OUT, `${prefix}-hero-${s.name}.png`),
			});
		}
		await ctx.close();
	}

	async function shootIntegrations(viewport, prefix) {
		const ctx = await browser.newContext({ viewport, deviceScaleFactor: 2 });
		const page = await ctx.newPage();
		await page.goto(url, { waitUntil: 'networkidle' });

		await page.evaluate(() => { document.getElementById('preview-label').textContent = 'Integrations — default'; });
		await page.locator('#integrations').scrollIntoViewIfNeeded();
		await page.waitForTimeout(500);
		await page.locator('#integrations').screenshot({
			path: path.join(OUT, `${prefix}-integrations-default.png`),
		});

		await page.evaluate(() => { document.getElementById('preview-label').textContent = 'Integrations — chip hover'; });
		// Stop carousel animation AND reset to position 0 so the chip we
		// flag with .is-preview-hover is the visually-leftmost one.
		// Also force a deterministic hover style — headless :hover via
		// Locator.hover is unreliable across runs.
		await page.addStyleTag({ content: `
			.bpo-integrations__row--left .bpo-integrations__track,
			.bpo-integrations__row--right .bpo-integrations__track {
				animation: none !important;
				transform: translateX(0) !important;
			}
			.bpo-integrations__chip.is-preview-hover {
				transform: translateY(-4px) scale(1.08) !important;
				box-shadow:
					0 10px 25px -5px rgba(239, 73, 75, 0.35),
					0 6px 12px -4px rgba(0, 0, 0, 0.15) !important;
				outline-color: #ef494b !important;
			}
			.bpo-integrations__chip.is-preview-hover > img {
				transform: scale(1.12) !important;
			}
		` });
		await page.evaluate(() => {
			var chip = document.querySelector('#track-1 .bpo-integrations__chip');
			if (chip) chip.classList.add('is-preview-hover');
		});
		await page.waitForTimeout(400);
		await page.locator('#integrations').screenshot({
			path: path.join(OUT, `${prefix}-integrations-hover.png`),
		});

		await ctx.close();
	}

	console.log('Capturing desktop…');
	await shootHeroStates(desktop, 'desktop');
	await shootIntegrations(desktop, 'desktop');

	console.log('Capturing mobile…');
	await shootHeroStates(mobile, 'mobile');
	await shootIntegrations(mobile, 'mobile');

	await browser.close();
	console.log('Done. Screenshots in', OUT);
})();
