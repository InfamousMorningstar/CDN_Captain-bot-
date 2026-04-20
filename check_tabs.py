import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://www.cdndayz.com/rules", wait_until="networkidle", timeout=30000)
        
        # Check each candidate selector
        for selector in ['[role="tab"]', '[data-tab]', '.tab-btn', '.tab-button', 'button[class*="tab"]', 'div[class*="tab"]', '[class*="Tab"]']:
            els = await page.query_selector_all(selector)
            if els:
                texts = []
                for el in els[:5]:
                    t = await el.inner_text()
                    cls = await el.get_attribute("class")
                    role = await el.get_attribute("role")
                    texts.append(f"  text={repr(t[:40])!r} class={repr(cls)!r} role={repr(role)!r}")
                print(f"SELECTOR {repr(selector)}: {len(els)} found")
                for t in texts:
                    print(t)
        
        # Also dump all button elements
        buttons = await page.query_selector_all("button")
        print(f"\nAll buttons ({len(buttons)} total):")
        for btn in buttons:
            t = await btn.inner_text()
            cls = await btn.get_attribute("class")
            print(f"  text={repr(t[:50])!r} class={repr(cls)!r}")
        
        await browser.close()

asyncio.run(main())
