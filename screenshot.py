import json
from pyppeteer import launch

with open('screenshot.json') as f:
    data = json.load(f)


async def screenshot(url=None):
    browser = await launch({'headless': 'false'})
    page = await browser.newPage()
    await page.goto(url)
    await page.screenshot(data)
    await browser.close()
