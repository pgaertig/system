#!/bin/env python3
import os
import sys
import shutil
import asyncio
from pyppeteer import launch


async def main():
    if len(sys.argv) != 4:
        current_script = os.path.basename(__file__)
        print(f"Usage: {current_script} <country_code> <VAT ID> <screenshot-file.png>")
        print(f"Example:  {current_script} IE 1244556H vies-company.png")
        sys.exit(1)

    _, country_code, vat_id, screenshot_file = sys.argv
    chromium_path = shutil.which('chromium')
    browser = await launch({
        'headless': True,
        'devtools': False,
        'args': ['--no-sandbox'],
        'executablePath': chromium_path,
        'defaultViewport': {"width": 800, "height": 800, "deviceScaleFactor": 1.5}
        })
    page = await browser.newPage()
    await page.goto('https://ec.europa.eu/taxation_customs/vies/?locale=pl')
    await page.click('.wt-cck-btn-add')
    await page.select('select[name="memberStateCode"]', country_code)
    await page.select('select[name="requesterMemberStateCode"]', country_code)
    await page.type(selector='input[name="number"]', text=vat_id)
    await page.type(selector='input[name="requesterNumber"]', text=vat_id)
    await asyncio.wait([
        asyncio.create_task(page.click('#submit')),
        asyncio.create_task(page.waitForNavigation())])

    dimensions = await page.evaluate('''() => {
            const element = document.querySelector('#layout');
            const {x, y, width, height} = element.getBoundingClientRect();
            return {x, y, width, height};
        }''')

    await page.screenshot({
        'path': screenshot_file,
        'clip': dimensions,
        'fullPage': False
    })

    await browser.close()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
