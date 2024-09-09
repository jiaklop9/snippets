#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from datetime import datetime


if __name__ == '__main__':
    timestamp = 1566453314
    time_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d_%H.%M.%S")
    print(time_str)
