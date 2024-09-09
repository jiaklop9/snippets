#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import smtplib
import ssl
import os
import json
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from SecretResources import get_secret_msg


def check_chinese_char(_str):
    """判断字符串中是否包含中文"""
    for ch in _str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def get_mail_account_msg():
    kv = get_secret_msg('邮件发送带附件', url='http://172.16.13.129:8062/api/secret/')
    return {item['key']: item['val'] for item in json.loads(kv['data']['secretData'])}


class EmailClient(object):
    def __init__(self, subject, body, sender, receivers, password, attaches, body_type='html'):
        self.subject = subject
        self.body = body
        self.sender = sender
        self.receivers = receivers
        self.password = password
        self.attaches = attaches
        # 邮件正文内容类型，默认文本
        self.body_type = body_type

        self.message = None
        self._initialized()

    def _initialized(self):
        self.message = MIMEMultipart()
        self.message["From"] = self.sender
        self.message["To"] = ','.join(self.receivers)
        self.message["Subject"] = self.subject
        # self.message["Bcc"] = self.receivers  # Recommended for mass emails

    def add_body(self, body):
        if self.body_type == "html":
            self.message.attach(MIMEText(self.body, _subtype='html', _charset='utf-8'))
        else:
            self.message.attach(MIMEText(body, "plain"))

    def _add_attachment(self, filename):
        if not os.path.exists(filename) or not os.path.isfile(filename):
            return
        with open(filename, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode the message's payload in Base64.
        encoders.encode_base64(part)

        if check_chinese_char(filename):
            part.add_header("Content-Disposition", "attachment", filename=("gbk", "", f"{os.path.basename(filename)}"))
        else:
            # 不包含中文
            part["Content-Disposition"] = f'attachment; filename="{os.path.basename(filename)}")'
        self.message.attach(part)

    def add_attachments(self, filenames):
        if not filenames:
            return
        if isinstance(filenames, list):
            for attach in filenames:
                self._add_attachment(attach)
            return
        self._add_attachment(filenames)

    def send_mail(self):
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.qq.com", 465, context=context) as server:
            try:
                server.login(self.sender, self.password)
                server.sendmail(self.sender, self.receivers, self.message.as_string())
                print(True)
            except smtplib.SMTPException as e:
                print(False)

    def main(self):
        if self.body:
            self.add_body(self.body)
        self.add_attachments(self.attaches)
        self.send_mail()

# 主要功能说明: 邮件发送

# 用户可修改区域-开始
#########################################################################
# subject：邮件主题
# body: 邮件正文
# body_type： 正文类型，文本的话默认 'plain'， 否则为 'html'
# sender: 发送邮箱，需要提前打开pop获取授权码
# receivers： 接收者，列表或者字符串
# password： 发送邮箱授权码
# attaches： 附件绝对路径，列表或者字符串


config = {
    'subject': "An email with attachment from Python",
    'body': "This is an email with attachment sent from Python",
    'body_type': 'plain',
    'receivers': ["1714476383@qq.com"],
    'attaches': r'D:\workspace\snippets\mail\企业微信对接.pdf',
    'sender': '1714476383@qq.com',
    'password': 'tjjobomdevjlccjb'
 }

#########################################################################
# 用户可修改区域-结束

# config.update(get_mail_account_msg())


if __name__ == '__main__':
    EmailClient(**config).main()
