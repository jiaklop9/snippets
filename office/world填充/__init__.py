#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import base64
import datetime
import json
import requests
from docxtpl import DocxTemplate
from urllib.parse import urlparse


def is_url(string):
    try:
        result = urlparse(string)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def check_and_trans_result(result):
    """
    检查是否为base64并输出
    若为base64则是列表，转换下输出
    若为url, 则下载图片并插入
    :param result:
    :return:
    """
    try:
        data = base64.b64decode(result)
        # 部分组件列表不合规 [[], {}, {}]转换为 [[], [,,,]]形式
        data = json.loads(data.decode('utf-8'))
        result = list()
        for index, values in enumerate(data):
            if index == 0:
                result.append(values)
                continue
            if isinstance(values, dict):
                result.append(list(values.values()))
            else:
                result.append(values)
        return result
    except:
        return result


def get_api_data():
    # url = 'http://172.16.13.135:8062/api/scene/task/result/202406041849310555'
    # url = 'http://172.16.13.135:8062/api/scene/task/result/202406041843430554'
    # url = 'http://172.16.13.135:8062/api/scene/task/result/202405231118170548'
    url = 'http://172.16.13.129:8062/api/flow/result/202405291645540421'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'Token': 'eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjkyMWIwZmYxLTRhODQtNDdlZi05MmM0LTE3YjdiY2ExODdjZCJ9.EPJZ-3APx8uUZ-oppsq3YCUXr1Xu6XF32es3g9fh8GHjV2NI6C2p5hQCsNiogrk_Ay1xU0GuhjwMERIGhpPdHQ',
        'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6IjkyMWIwZmYxLTRhODQtNDdlZi05MmM0LTE3YjdiY2ExODdjZCJ9.EPJZ-3APx8uUZ-oppsq3YCUXr1Xu6XF32es3g9fh8GHjV2NI6C2p5hQCsNiogrk_Ay1xU0GuhjwMERIGhpPdHQ'
    }
    response = requests.get(url=url, headers=headers)
    response.raise_for_status()
    response = response.json()
    with open('data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(response))
    if response['code'] != 200:
        raise Exception(response['msg'])
    data = list()
    for step in response['data']:
        result = dict()
        dynamic_property = json.loads(step['dynamicProperty'])
        result['title'] = dynamic_property['title']
        result['label'] = step['label']
        params = dynamic_property.get('paramValue', '')
        # TODO device_name做占位符不太准确
        if params:
            result['device_name'] = [' '.join(kv.values()) for kv in params][0]
        else:
            device_name = dynamic_property.get('deviceName', '')
            if device_name:
                result['device_name'] = device_name
            else:
                command = dynamic_property.get('CommandValue', '')
                if command:
                    result['device_name'] = command
                else:
                    result['device_name'] = ''
        result['output_result'] = check_and_trans_result(step['outputResult'])
        data.append(result)

    return data


def main():
    doc = DocxTemplate("models.docx")
    context = {
        "step": get_api_data()
    }

    doc.render(context)
    doc.save("result.docx")


if __name__ == '__main__':
    main()



