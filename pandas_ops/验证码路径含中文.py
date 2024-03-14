#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import cv2
import numpy as np


def main():
    img = cv2.imdecode(np.fromfile(r'图片路径', dtype=np.uint8), -1)
    img = cv2.imencode(".png", img)[1].tobytes()
    """
    其他
    """


if __name__ == "__main__":
    main()
