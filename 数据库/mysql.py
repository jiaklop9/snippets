#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
import json

import pymysql
import requests


class MySQL(object):
    def __init__(self, host, port, user, password, db='zhangx'):
        self.host = host
        self.port = port
        self.user = user
        self.pwd = password
        self.db = db
        self.conn = None
        self.cursor = None
        self.initialized()

    def initialized(self):
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.pwd,
            port=3306,  # 端口，默认为3306
            db=self.db,  # 数据库名称
            charset='utf8'  # 字符编码
        )
        self.cursor = self.conn.cursor()

    @staticmethod
    def get_domain_data(domain):
        url = "https://api.threatbook.cn/v3/domain/query"
        query = {
            "apikey": "1b4d5e075a1241428cc2f164e69f58989434b22958734ac7a1c93bf5e7996086",
            "resource": domain
        }

        response = requests.request("GET", url, params=query)
        response.raise_for_status()
        response = response.json()
        if response['response_code']:
            raise Exception(f"请求异常: {response['verbose_msg']}")
        print(f"获取域名：{domain} 相关信息：{response['verbose_msg']}")
        return response['data']

    @staticmethod
    def get_ip_data(ip):
        url = "https://api.threatbook.cn/v3/ip/query"
        query = {
            "apikey": "1b4d5e075a1241428cc2f164e69f58989434b22958734ac7a1c93bf5e7996086",
            "resource": ip
        }

        response = requests.request("GET", url, params=query)
        response.raise_for_status()
        return response.json()['data']

    def insert_domain_data(self, data, domain='baidu.com'):
        data = data.get(domain)
        samples = json.dumps(data['samples']).strip()
        tags_classes = json.dumps(data['tags_classes']).strip()
        judgments = json.dumps(data['judgments']).strip()
        intelligences = json.dumps(data['intelligences']).strip()
        cas = json.dumps(data['cas']).strip()
        rank = json.dumps(data['rank']).strip()
        categories = json.dumps(data['categories']).strip()
        cur_whois = json.dumps(data['cur_whois']).strip()
        cur_ips = json.dumps(data['cur_ips']).strip()
        sum_sub_domains = data['sum_sub_domains']
        sum_cur_ips = data['sum_cur_ips']
        sql = f"""INSERT INTO `zhangx`.`微步在线` (
        `域名`,`样本`, `安全事件信息`, `威胁类型`, `威胁情报`, `域名的SSL相关证书信息`,
        `域名的排名信息`,`域名的分类数据`,`域名的whois信息`,`域名对应IP信息`,`子域名数量`,`当前解析IP数量`
        ) Values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

        self.cursor.execute(sql, (domain, samples, tags_classes, judgments, intelligences, cas, rank, categories,
        cur_whois, cur_ips, sum_sub_domains, sum_cur_ips))
        self.conn.commit()
        print('插入数据库...')

    def insert_ip_data(self, data, ip):
        sql = """INSERT INTO `zhangx`.`微步在线_ip_query`
                (`ip`, `样本`, `安全事件信息`, `威胁类型`, `威胁情报`, `应用场景`, `基础信息`, `asn信息`,
                `IP开放的相关端口`, `域名的SSL相关证书信息`,`更新时间`, `Rdns记录`, `反查当前域名数量`)
                VALUES
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"""
        data = data[ip]
        samples = json.dumps(data['samples']).strip()
        tags_classes = json.dumps(data['tags_classes']).strip()
        judgments = json.dumps(data['judgments']).strip()
        intelligences = json.dumps(data['intelligences']).strip()
        scene = json.dumps(data['scene']).strip()
        basic = json.dumps(data['basic']).strip()
        asn = json.dumps(data['asn']).strip()
        ports = json.dumps(data['ports']).strip()
        cas = json.dumps(data['cas']).strip()
        update_time = data['update_time']
        rdns_list = json.dumps(data['rdns_list'])
        sum_cur_domains = data['sum_cur_domains']
        self.cursor.execute(sql, (ip, samples, tags_classes, judgments, intelligences, scene, basic,asn,
                                  ports, cas, update_time, rdns_list, sum_cur_domains))
        self.conn.commit()
        print('插入数据库...')

    def quit(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn is not None:
            self.conn.close()

    def main(self):
        # domain = 'zhihu.com'
        # data = self.get_domain_data(domain)
        # self.insert_domain_data(data=data, domain=domain)
        ip = '118.9.5.141'
        data = self.get_ip_data(ip)
        self.insert_ip_data(data, ip)
        self.quit()


if __name__ == '__main__':
    mysql = MySQL(host='172.16.13.129', port=3306, user='zhangx', password='zhangx')
    mysql.main()
