#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import imaplib
import email
from email.header import decode_header

def fetch_emails(username, password, imap_server, folder="inbox"):
    # 连接到 IMAP 服务器
    mail = imaplib.IMAP4_SSL(imap_server)
    mail.login(username, password)
    mail.select(folder)

    # 搜索所有邮件
    status, messages = mail.search(None, 'ALL')
    email_ids = messages[0].split()

    for email_id in email_ids:
        # 获取邮件数据
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                # 解码邮件头部
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding if encoding else "utf-8")
                print("Subject:", subject)
                # 获取邮件内容
                # if msg.is_multipart():
                #     for part in msg.walk():
                #         content_type = part.get_content_type()
                #         content_disposition = str(part.get("Content-Disposition"))
                #         if "attachment" not in content_disposition:
                #             try:
                #                 body = part.get_payload(decode=True).decode()
                #                 print("Body:", body)
                #             except AttributeError:
                #                 pass
                #             except UnicodeDecodeError:
                #                 pass
                # else:
                #     try:
                #         body = msg.get_payload(decode=True).decode()
                #         print("Body:", body)
                #     except UnicodeDecodeError:
                #         pass


    mail.logout()

# 使用示例
username = "zhike.liu@foxmail.com"
password = "qrjruymrvjphcdjf"
imap_server = "imap.qq.com"
fetch_emails(username, password, imap_server)
