#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import base64
import os

import docxtpl
import requests
import json
from docxtpl import DocxTemplate
from docx import shared
from urllib.parse import urlparse

from jinja2 import Environment, BaseLoader


class Utils(object):
    def __init__(self):
        pass

    @classmethod
    def is_url(cls, string):
        try:
            result = urlparse(string)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    @classmethod
    def is_base64(cls, string):
        try:
            decoded = base64.b64decode(string)
            # Encode the decoded bytes back to a string
            encoded = base64.b64encode(decoded).decode('utf-8')
            # Compare the original string with the re-encoded string
            return encoded == string
        except:
            # If decoding fails or any exception occurs, return False
            return False

    # jinja2模板定义函数
    @classmethod
    def is_string(cls, string):
        return isinstance(string, str)

    @classmethod
    def is_obj(cls, obj):
        return isinstance(obj, object)

    @classmethod
    def is_list(cls, obj):
        return isinstance(obj, list)




class Report(object):
    def __init__(self, host, model_path='models.docx'):
        self.doc = DocxTemplate(model_path)
        self.host = host
        # self.headers = {
        #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        #     'Token': 'eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImJhZDkxMTJhLTYwNjItNDM1OS04MzMxLWRhNjc0Y2EwYTgxMSJ9.Y2yEK5p8gmysYnYOMYAHT5fkekHL5Cb4Bgv5apXawMmmTHkoiIHvMAZHQOYWDFS44vka9fvYaw_V9e3u65lqzw',
        #     'Authorization': 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl91c2VyX2tleSI6ImJhZDkxMTJhLTYwNjItNDM1OS04MzMxLWRhNjc0Y2EwYTgxMSJ9.Y2yEK5p8gmysYnYOMYAHT5fkekHL5Cb4Bgv5apXawMmmTHkoiIHvMAZHQOYWDFS44vka9fvYaw_V9e3u65lqzw'
        # }

    def do_request(self, url, label):
        """
        :param url:
        :param label:
        :return:
        """
        response = requests.get(url=url)
        response.raise_for_status()
        response = response.json()
        if response['code'] != 200:
            raise Exception(f"{label}结果获取失败：{response['msg']}")
        return response['data']

    def get_scene_data(self, scene_id):
        """场景结果获取"""
        url = f'{self.host}/api/scene/result/{scene_id}'
        data = self.do_request(url, '场景')
        return self.parse_output(data)

    def get_task_data(self, task_id):
        """任务结果获取"""
        url = f'{self.host}/api/scene/task/result/{task_id}'
        data = self.do_request(url, '任务')
        return self.parse_output(data)

    def get_flow_data(self, flow_id):
        """流程结果数据获取"""
        url = f'{self.host}/api/flow/result/{flow_id}'
        data = self.do_request(url, '流程')
        print(data)
        return self.parse_output(data)

    def trans_result(self, result):
        """任务结果转换
        1. 字符串原样输出
        2. base64转化输出
        3. url, 下载输出
        """
        if Utils.is_url(result):
            response = requests.get(url=result)
            response.raise_for_status()
            with open('result.png', 'wb') as f:
                f.write(response.content)
            return docxtpl.InlineImage(self.doc, 'result.png', width=shared.Mm(150))
        if Utils.is_base64(result):
            # 部分组件列表不合规 [[], {}, {}]转换为 [[], [,,,]]形式
            result = json.loads(base64.b64decode(result).decode('utf-8'))
            data = list()
            for index, values in enumerate(result):
                if index == 0:
                    data.append(values)
                    continue
                if isinstance(values, dict):
                    data.append(list(values.values())[:len(result[0])])
                else:
                    data.append(values[:len(result[0])])
            # 结果中含有空列表，过滤
            return [i for i in data if i]
        else:
            return result

    @staticmethod
    def action_map(action):
        _map = {
            'click': "(点击)",
            'input': "(输入)",
            'login': "(登录)",
            'captcha': "(验证码)",
            'popUp': "(弹窗)",
            'dropdownSelect': "(下拉选择)",
            'delay': "(延时)",
            'inIframe': "(进入Iframe)",
            'outIframe': "(退出Iframe)",
            'dateFilter': "(输入日期)"
        }
        return _map.get(action, '')

    def trans_xpath(self, ele_arr):
        for kv in ele_arr:
            result = list()
            name = kv.get('name')
            result.append(name)
            action_type = kv.get('elementType')
            result.append(self.action_map(action_type))
            if action_type == 'dropdownSelect':
                result.append(
                    f"XPath路径:【***】，选择元素名称：【{kv.get('xPathRemark', '')}】，"
                    f"等待时间:【{kv.get('webTimeOut', 0)}】秒;"
                )
            elif action_type == 'dateFilter':
                result.append(
                    f"XPath路径:【***】，日期阈值:【{kv.get('webValue', '')}】，"
                    f"输入天数:【{kv.get('webDateOffset', 0)}】，"
                    f"等待时间:【{kv.get('webTimeOut', 0)}】秒;"
                )
            elif action_type == 'delay':
                result.append(f"延时时间:【{kv.get('webTimeOut', 0)}】秒;")
            else:
                if name.find('密码') > -1:
                    xpath_remark = '***'
                else:
                    xpath_remark = kv.get('xPathRemark', '')
                result.append(
                    f"XPath路径:【***】，XPath内容:【{xpath_remark}】，"
                    f"等待时间:【{kv.get('webTimeOut', 0)}】秒;"
                )
            return ','.join(result)

    def parse_output(self, output):
        data = list()
        for step in output:
            result = dict()
            dynamic_property = json.loads(step['dynamicProperty'])
            result['title'] = dynamic_property['title']
            result['label'] = step['label']
            result['output_result'] = self.trans_result(step['outputResult'])
            """
            1. deviceName
            2. 有paramValue时不要deviceName
            3. 其他
            """
            component_id = step.get('componentType', -1)
            if component_id in ['1', '2']:
                result['action'] = f"-> ip:【{dynamic_property.get('host', '')}】 账号:【{dynamic_property.get('username', '')}】"
            elif component_id == '3':
                result['action'] = f"-> 命令行:【{dynamic_property.get('CommandValue', '')}】"
            elif component_id == '4':
                result['action'] = self.trans_xpath(dynamic_property.get('elementArry'))
            elif component_id == '5':
                result['action'] = f"-> URL:【{dynamic_property.get('host', '')}】"
            elif component_id == '6':
                result['action'] = (f"-> XPath路径：【***】 "
                                    f"等待时间：【{dynamic_property.get('webTimeOut', 0)}】秒")
            elif component_id == '7':
                result['action'] = (f"-> XPath路径：【***】 "
                                    f"等待时间：【{dynamic_property.get('webTimeOut', 0)}】秒")
            elif component_id == '9':
                result['action'] = (f"-> XPath路径:【***】 "
                                    f"采集字段名:【{dynamic_property.get('gatherField', '')}】 "
                                    f"等待时间:【{dynamic_property.get('webTimeOut', 0)}】")
            elif component_id == '10':
                result['action'] = (f"-> XPath路径：【***】 "
                                    f"单元格行号：【{dynamic_property.get('webRow', 0)}】 "
                                    f"单元格列号：【{dynamic_property.get('webColumn', 0)}】 "
                                    f"采集字段：【{dynamic_property.get('gatherField', '')}】 "
                                    f"等待时间：【{dynamic_property.get('webTimeOut', 0)}】秒")
            elif component_id in ['11', '14']:
                result['action'] = f"-> 采集设备:【{dynamic_property.get('deviceName', '')}】"
            elif component_id in ['12', '13', '15', '16']:
                for k, v in dynamic_property.get('paramValue', {}).items():
                    result['action'] = f"{k}: 【{v}】 "
                    break
            elif component_id == '17':
                string = ''
                for k, v in dynamic_property.get('paramValue', {}).items():
                    string += f"{k}: 【{v}】 "
                result['action'] = string
            elif component_id == '19':
                result['action'] = f"-> 收集字段信息:【{dynamic_property.get('collectFields', '')}】"
            elif component_id == '20':
                result['action'] = (f"-> 前缀命令：【{dynamic_property.get('PrefixCommand', '')}】 "
                                    f"命令值：【{dynamic_property.get('CommandValue', '')}】 "
                                    f"后缀命令：【{dynamic_property.get('SuffixCommand', 0)}】 ")
            elif component_id == '21':
                result['action'] = f"-> 终端：【服务端】"
            elif component_id in ['25', '26']:
                recv_type = dynamic_property.get('receivingType')
                msg_content = json.loads(dynamic_property.get('messageContent'))
                msg_content.pop('id')
                if recv_type == '2':
                    # TODO
                    string = "指定接收人()"
                else:
                    string = "任务执行人"
                result['action'] = f"-> 接收人：【{string}】 正文：【{msg_content}】"
            elif component_id == '28':
                result['action'] = f"-> 登录设备：【{dynamic_property.get('deviceName', '')}】"
            elif component_id == '29':
                result['action'] = (f"-> XPath路径：【***】 "
                                    f"采集字段：【{dynamic_property.get('gatherField', '')}】 "
                                    f"筛选字段：【{dynamic_property.get('queryStr', '')}】 "
                                    f"输出变量：【{dynamic_property.get('variable', '')}】 ")
            elif component_id in ['30', '33']:
                result['action'] = f"-> 遍历变量：【{dynamic_property.get('varIterator', '')}】"
            elif component_id == '35':
                result['action'] = f"-> python脚本:【{dynamic_property.get('scriptCode', '')}】"
            else:
                pass
            data.append(result)
        return data

    def render_doc(self, context_data):
        context = {
            "step": context_data
        }
        env = Environment(loader=BaseLoader())
        env.filters['is_string'] = Utils.is_string
        env.filters['is_obj'] = Utils.is_obj
        env.filters['is_list'] = Utils.is_list
        self.doc.render(context, jinja_env=env)
        self.doc.save("result.docx")
        try:
            os.remove('result.png')
        except FileNotFoundError:
            pass

    def main(self, _id, _type):
        """
        :param _id: 任务/流程/场景id
        :param _type: scene/task/flow
        :return:
        """
        if _type == 'flow':
            self.render_doc(self.get_flow_data(_id))
        elif _type == 'scene':
            self.render_doc(self.get_scene_data(_id))
        elif _type == 'task':
            self.render_doc(self.get_task_data(_id))
        else:
            raise Exception(f"不支持的类型: {_type}")


if __name__ == '__main__':
    Report('http://172.16.13.129:8062').main('202405301104320423', 'flow')