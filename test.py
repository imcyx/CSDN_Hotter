# -*- coding: utf-8 -*-
# @Time    : 2022/11/1 11:51
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : test.py
# @Software: PyCharm
# @Project : CSDN_Hotter

import requests

ips = requests.get('http://localhost:5555/random').text
print(ips)