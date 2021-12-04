import json
import asyncio
from pyppeteer import launch

with open('screenshot.json') as f:
    data = json.load(f)


async def screenshot():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://oscar-wos.github.io')
    await page.screenshot(data)
    await browser.close()

asyncio.get_event_loop().run_until_complete(screenshot())
