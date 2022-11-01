# -*- coding: utf-8 -*-
# @Time    : 2022/11/1 20:00
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : main.py
# @Software: PyCharm
# @Project : CSDN_Hotter

from src.src import runner
import os

def main():
    username = os.environ.get("USERNAME")
    mode = os.environ.get("MODE")

    if username == '':
        raise Exception("Sorry <( _ _ )> ！Reachable username should be provided")

    if mode == 'explore':
        mode = True
    else:
        mode = False

    runner(username, mode)


if __name__=='__main__':
    main()
