#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import json
from rocketmq.client import Producer
from rocketmq.client import Message

# 初始化生产者
producer = Producer('auto_task_group')
# 设置NameServer地址
producer.set_namesrv_addr('172.16.13.129:9876')
# producer.set_session_credentials("access_key", "secret_key", 'authChannel')  # 完成设置验证
# 启动生产者
producer.start()

# 构建消息(需要将消息发送到指定Topic)
message = Message('executeTaskTopic')
# 设置消息内容(注意消息只能是字符串)
msg_body = {
        "createId": 1,
        "createTime": "2024-04-12 09:25:12",
        "dataStatus": 0,
        "flowId": "202404111438450037",
        "params": {},
        "processName": "zxtest0411",
        "remark": json.dumps([
            {
                'child': [{
                    'activityId': 'Activity_1pe59dk',
                    'componentType': '12',
                    'createTime': '2024-04-11 14:38:45',
                    'describeInfo': '',
                    'dynamicProperty': json.dumps({
                        "remarkR": "封禁ip",
                        "host": "",
                        "deviceId": 14,
                        "deviceName": "深信服防火墙",
                        "action": "SangforFirewallIpBlocking",
                        "paramValue": [{"name": "目标IP", "val": "123"}],
                        "remarkC": "",
                        "variable": "",
                        "method": "终止流程",
                        "time": 0
                    }),
                    'executeUser': 1,
                    'flowEndFlag': True,
                    'flowId': '202404111438450037',
                    'id': 3368, 'ispackage': 1,
                    'label': '封禁IP',
                    'onlyKey': 'luuvbklj-cnqxahykm',
                    'parent': 'FIREWALL',
                    'status': '1',
                    'taskId': '803f8859bb5e459e8983ed17cc081fd0',
                    'uuid': '3295c61effd54263af685f7a62385c88'
                }],
                'componentType': '11',
                'describeInfo': '',
                'dynamicProperty': json.dumps({
                    "remarkR": "登录防火墙",
                    "deviceId": 14,
                    "deviceName": "深信服防火墙",
                    "remarkC": "",
                    "variable": "",
                    "method": "终止流程",
                    "time": 0
                }),
                'executeUser': 1,
                'flowEndFlag': False,
                'flowId': '202404111438450037',
                'id': 3369,
                'ispackage': 0,
                'label': '登录防火墙设备',
                'onlyKey': 'luuvbdx5-uuxuukwra',
                'parent': 'FIREWALL',
                'status': '1',
                'taskId': '803f8859bb5e459e8983ed17cc081fd0',
                'uuid': 'ce57e5a97ea24d6abf7ddd568362c510'
            }]),
        "status": "1",
        "taskId": "803f8859bb5e459e8983ed17cc081fd0"
    }
message.set_body(json.dumps(msg_body).encode('utf-8'))
# 可以设置其他属性，如Tags、Keys等
# message.set_tags('your_tag')
# message.set_keys('your_key')

try:
    # 发送消息(此处就会发送消息到RocketMQ服务器)
    ret = producer.send(message)
    # 打印发送结果
    if ret.status == Message.SendStatus.OK:
        print("发送成功")
    else:
        print(f"发送失败, 消息状态: {ret.status}")
except Exception as e:
    # 处理发送过程中可能出现的异常
    print(f"Send message failed, exception: {e}")
finally:
    # 停止生产者
    producer.shutdown()