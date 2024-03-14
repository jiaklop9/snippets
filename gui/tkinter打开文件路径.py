#!/usr/bin/env python3
# -*- coding: utf8 -*-

import sys
import tkinter as tk
from tkinter import filedialog


class FolderChoice(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry()
        self.folder = ''

    def get_base_folder(self):
        file_path = filedialog.askdirectory(title="选择数据文件夹")
        if file_path:
            print("选择的文件路径:", file_path)
            self.folder = file_path
            self.root.destroy()

    def main(self):
        print('打开数据源文件所在文件夹')
        # 创建主窗口
        # 创建打开文件按钮
        open_button = tk.Button(self.root, text="打开数据源文件所在文件夹", command=self.get_base_folder)
        open_button.pack(pady=20)
        # 启动主循环
        self.root.mainloop()
        if not self.folder:
            sys.exit("未选择数据源文件所在文件夹,退出")
