#!/bin/env python3
import os
import shutil
import asyncio
import keyring
import getpass
import argparse
from pyppeteer import launch

intro = """
 Automated AnyConnect VPN login (customized). To be used with OpenConnect.
 Example:
    
    ./webvpn-login.py USER@COMPANY.com 'https://YOUR-VPN-HOST/+CSCOE+/logon.html' /tmp/vpncookie && cat /tmp/vpncookie | sudo time openconnect -v --cookie-on-stdin YOUR-VPN-HOST
 
 License: GPL 3.0
"""

the_script = os.path.basename(__file__)

async def getError(page):
    return await page.evaluate('''() => {
            const errorType = document.querySelector('.alert-error .type');
            const type = errorType ? errorType.innerText : null ;
            const errorContent = document.querySelector('.alert-error .content');
            const content = errorContent ? errorContent.innerText : null;
            return {type, content};
    }''')

async def main():

    parser = argparse.ArgumentParser(description=intro)
    parser.add_argument('user', help='Anyconnect user email')
    parser.add_argument('url', help='Anyconnect endpoint URL')
    parser.add_argument('cookie_file', help='File to store the VPN cookie')
    args = parser.parse_args()

    chromium_path = shutil.which('chromium')
    browser = await launch({
        'headless': True,
        'devtools': False,
        'args': ['--no-sandbox'],
        'executablePath': chromium_path,
        'defaultViewport': {"width": 800, "height": 800}
    })
    page = await browser.newPage()
    await asyncio.wait([
        asyncio.create_task(page.goto(args.url)),
        asyncio.create_task(page.waitForNavigation())])
    await asyncio.wait([
        asyncio.create_task(page.click('input[name="Login"]')),
        asyncio.create_task(page.waitForNavigation())])

    while True:
        keyring_password = keyring.get_password(the_script, args.user)
        password = keyring_password or getpass.getpass('Anyconnect user password:')
        await page.evaluate('''() => {document.querySelector('input[name="username"]').value="";}''')
        await page.evaluate('''() => {document.querySelector('input[name="password"]').value="";}''')
        await page.type(selector='input[name="username"]', text=args.user)
        await page.type(selector='input[name="password"]', text=password)
        await asyncio.wait([
            asyncio.create_task(page.click('#kc-login')),
            asyncio.create_task(page.waitForNavigation(waitUntil='networkidle0'))])

        errorInfo = await getError(page)
        if errorInfo['type']:
            print(f"{errorInfo['type']} - {errorInfo['content']}")
            if keyring_password:
                keyring.delete_password(the_script, args.user)
        else:
            await page.waitForSelector('#oath')
            # Once logged in remember the password
            keyring.set_password(the_script, args.user, password)
            break


    while True:
        auth_code = input('Enter the received auth code: ')
        await page.evaluate('''() => {document.querySelector('#oath').value="";}''');
        await page.type(selector='#oath', text=auth_code)
        await asyncio.wait([
            asyncio.create_task(page.click('#kc-login')),
            asyncio.create_task(page.waitForNavigation(waitUntil='networkidle0'))])

        await page.waitFor(5000)
        errorInfo = await getError(page)
        if errorInfo['type']:
            print(f"{errorInfo['type']} - {errorInfo['content']}")
        else:
            break

    webvpn_cookie = [c['value'] for c in await page.cookies() if c["name"] == 'webvpn']
    await browser.close()

    if len(webvpn_cookie) == 1:
        with open(args.cookie_file, "w") as text_file:
            text_file.write(webvpn_cookie[0])
        print(f"Cookie {webvpn_cookie}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.close()
