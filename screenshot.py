import json
import asyncio
import time
from pyppeteer import launch

with open('screenshot.json') as f:
    data = json.load(f)


async def gif(url=None):

    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://oscar-wos.github.io')

    for x in range(7):
        data['path'] = f'screenshots/{x}.png'
        await page.screenshot(data)
        time.sleep(1)

    await browser.close()

asyncio.get_event_loop().run_until_complete(gif())
