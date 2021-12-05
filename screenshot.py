import json
import asyncio
import time
from pyppeteer import launch
from trim import trim_image, make_gif

with open('screenshot.json') as f:
    data = json.load(f)


async def screenshot(url=None):
    browser = await launch({'headless': 'false'})
    page = await browser.newPage()
    await page.goto(url)

    for i in range(10):
        data['path'] = f'screenshots/{i}.png'
        await page.screenshot(data)
        trim_image(f'screenshots/{i}.png', f'screenshots_trimmed/{i}.png')
        time.sleep(1)

    await browser.close()
    make_gif()

asyncio.get_event_loop().run_until_complete(
    screenshot('https://oscar-wos.github.io'))
