import json
import time
from pyppeteer import launch
from trim import trim_image

with open('screenshot.json') as f:
    data = json.load(f)


async def screenshot(url=None):
    browser = await launch({'headless': 'false'})
    page = await browser.newPage()
    await page.goto(url)

    for i in range(30):
        data['path'] = f'screenshots/{i}.png'
        await page.screenshot(data)
        trim_image(f'screenshots/{i}.png', f'screenshots_trimmed/{i}.png')
        time.sleep(0.3)

    await browser.close()
