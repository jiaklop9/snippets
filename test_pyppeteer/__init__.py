#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import asyncio
import time

from pyppeteer import launch


async def main():
    try:
        browser = await launch(executablePath=r'C:\Users\jiakl\AppData\Local\Google\Chrome\Application\chrome.exe', headeless=False)
    except Exception as e:
        print(f'打开异常: {e}')
    print('1')
    page = await browser.newPage()
    time.sleep(60)
    # await page.goto('https://www.gsxt.gov.cn/socialuser-use-login.html')
    # await page.waitForSelector('#btn_login')
    # btn = await page.querySelector('#btn_login')
    # if btn:
    #     location = await btn.boundingBox()
    #     print(location)


asyncio.get_event_loop().run_until_complete(main())


