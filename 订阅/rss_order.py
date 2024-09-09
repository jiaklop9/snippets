#!/usr/bin/env python3
# -*- encoding: utf-8 -*-


import feedparser

# RSS订阅源URL
rss_url = 'https://feedpress.me/wx-girlswhocode'

# 解析RSS订阅源
feed = feedparser.parse(rss_url)

# 打印订阅源标题
print(f"订阅源标题: {feed.feed.title}")

# 遍历并打印每篇⽂章的标题和链接
for entry in feed.entries:
    print(f"⽂章标题: {entry.title}")
    print(f"链接: {entry.link}\n")