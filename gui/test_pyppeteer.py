#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import asyncio
import time

from pyppeteer import launch


async def main():
    browser = await launch(dumpio=True, headless=False, args=['--start-maximized'])
    print('1')
    page = await browser.newPage()
    await page.goto('https://www.baidu.com')
    print(await page.evaluate("screen.height"))
    time.sleep(60)


asyncio.get_event_loop().run_until_complete(main())


