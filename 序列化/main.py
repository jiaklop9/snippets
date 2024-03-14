#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

import person_pb2

# 创建一个Person对象并设置字段值
person = person_pb2.Person()
person.name = "张三"
person.age = 30
person.email = "zhangsan@example.com"

# 序列化Person对象为二进制字符串
serialized_person = person.SerializeToString()
print(f"序列化后的数据：{serialized_person}")

# 反序列化二进制字符串为一个新的Person对象
new_person = person_pb2.Person()
new_person.ParseFromString(serialized_person)

# 输出新的Person对象的字段值
print(f"反序列化后的数据：姓名={new_person.name}, 年龄={new_person.age}, 邮箱={new_person.email}")