# -*- coding: utf-8 -*-
# @Time    : 2022/10/31 16:42
# @Author  : CYX
# @Email   : im.cyx@foxmail.com
# @File    : src.py
# @Software: PyCharm
# @Project : CSDN_Hotter


import requests
import time
import random
import urllib.request as ur
import selenium.webdriver.chrome.webdriver
import requests
import lxml
import os
from time import sleep
from lxml import etree

import user_agent
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import chrome
from selenium.webdriver import firefox
# from selenium.webdriver.firefox.service import Service
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.chrome.service import Service

from multiprocessing import Process, Manager
from multiprocessing.pool import ThreadPool

import json
import random

thread_num = 30
ip_num = 4
now_ip = 0
useful_ip = []


def getRequest(url):
    """
    Http Request    网站请求
    :return:
    """
    return ur.Request(
        url=url,
        headers={'User-Agent': user_agent.get_user_agent_pc(), },
    )


# 设置代理
def ChromeSetOptions(proxy_address):
    options = webdriver.ChromeOptions()  # 设置浏览器参数
    options.add_argument('--user-agent="%s"' % user_agent.get_user_agent_pc())  # 设置请求头的User-Agent
    # options.add_argument('--proxy-server=http://' + proxy_address)  # 选择动态IP地址
    options.add_argument('--incognito')  # 隐身模式（无痕模式）
    # op.add_argument('--disable-gpu')  # 禁用GPU加速
    options.page_load_strategy = "normal"
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-automation'])

    driver = webdriver.Chrome(
        service=chrome.service.Service('F:\Program Files\Google\Chrome\Application\chromedriver.exe'),
        options=options
    )

    return driver

def FirefoxSetOptions(proxy_address=None, load_normal=False):
    profile = webdriver.FirefoxOptions()
    if proxy_address is not None:
        ip, port = proxy_address.split(":")
        # 不使用代理的协议，注释掉对应的选项即可
        settings = {
            'network.proxy.type': 1,  # 0: 不使用代理；1: 手动配置代理
            'network.proxy.http': ip,
            'network.proxy.http_port': int(port),
            'network.proxy.ssl': ip,  # https的网站,
            'network.proxy.ssl_port': int(port),
        }
        # 更新配置文件
        for key, value in settings.items():
            profile.set_preference(key, value)

    if load_normal is False:
        profile.page_load_strategy = 'none'
        profile.set_preference('permissions.default.image', 2)
        profile.set_preference("permissions.default.stylesheet", 2)  # css禁止
        # profile.set_preference("permissions.default.stylesheet", 2)  # css禁止
    # profile.headless = True

    driver = webdriver.Firefox(
        service=firefox.service.Service('.\geckodriver.exe'),
        options=profile
    )

    return driver

# def spider(ips, pages):
#     # driver = ChromeSetOptions(ips)
#     driver = FirefoxSetOptions(ips)
#     try:
#         driver.get(pages[0])  # 先打开第一个页面
#         # WebDriverWait(driver, 30, 0.5, ignored_exceptions=TimeoutException).until(
#         #     lambda x: x.find_element(By.XPATH, "//h1[@id='articleContentId']/text()").is_displayed())
#         # res = driver.find_element(By.XPATH, "//div[@class='aside-box']/div[2]/dl[4]/@title")
#         for script in pages[1:]:  # 在这个页面里打开剩下的标签
#             js = " window.open('" + script + "')"
#             driver.execute_script(js)
#             time.sleep(0.3)
#         t0 = time.time()
#         while True:
#             try:
#                 WebDriverWait(driver, 3, 0.5, ignored_exceptions=TimeoutException).until(
#                     lambda x: x.find_element(By.XPATH, "//h1[@id='articleContentId']/text()").is_displayed())
#                 driver.quit()
#             except Exception as err:
#                 t1 = time.time()
#                 if t1 - t0 > 30:
#                     driver.quit()
#                     break
#                 else:
#                     continue
#
#         print('Section - once over!')
#     except Exception as err:
#         print('error', err)
#     finally:
#         driver.quit()

def spider(ips, pages):
    proxies = {'http': 'http://'+ips, 'https': 'http://'+ips}
    head = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'user-agent':  user_agent.get_user_agent_pc()
    }
    cookies = {
        'hide_login': '1',
        'log_Id_view': '1',
        'firstDie': '1',
        'log_Id_pv': '1',
        'dc_tos': 'rkmguu',
        'c_page_id': 'default',
        'c_segment': '14',
        'c_first_ref': 'default',
        'c_ref': 'default',
        'c_pref': 'default',
    }
    p = ThreadPool(len(pages))
    for url in pages:
        p.apply_async(requests.get, args=(url, ), kwds={'headers':head, 'allow_redirects':True, 'proxies':proxies, 'timeout': 15})
        # res = requests.get(url, headers=head, allow_redirects=True)#, proxies=proxies)
        sleep(0.3)
    res = requests.get(url, headers=head, allow_redirects=True, proxies=proxies, cookies=cookies)
    res = etree.HTML(res.content).xpath('//dl[@class="text-center"]/@title')
    grab_res = f"周排名：{res[1]}，总排名：{res[2]}，访问量：{res[3]}，积分：{res[5]}，粉丝：{res[6]}，获赞：{res[7]}，收藏：{res[8]}，"
    print(grab_res)

def getSrcPages():
    head = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
    }
    index_num = 1
    pages = {}
    proxies = {}
    while True:
        detail_url = 'https://blog.csdn.net/community/home-api/v1/get-business-list?' \
                     'page=%d&size=20&businessType=lately&noMore=false&username=qq_42059060'%index_num
        try:
            results = requests.get(detail_url, headers=head, proxies=proxies).json()
            if results['message'] == 'success':
                res = results['data']['list']
                if res is None:
                    break
                else:
                    for j in res:
                        pages[j['title']] = [j['url'], j['description']]
            index_num += 1
        except:
            ips = requests.get('http://localhost:5555/random').text
            proxies = {'http': 'http://'+ips, 'https': 'http://'+ips}
            continue

    print(pages)
    final_res = {}
    for key, value in zip(pages.keys(), pages.values()):
        final_res[key] = value[0]


    # if os.path.exists('urls.json'):
    #     with open('urls.json', 'r') as fp:
    #         pgs = json.loads(fp.readline())
    #     print(pgs)
    # else:
    #     pgs = {}
    #
    # def page_load(pages, title, final_res):
    #     ips = requests.get('http://localhost:5555/random').text
    #     driver0 = FirefoxSetOptions(ips, load_normal=True)
    #     url = pages[title][0]
    #     description = pages[title][1]
    #     for i in range(2):
    #         while True:
    #             try:
    #                 driver0.get('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&ch=&tn=baidu&bar=&wd=%s&pn=%d'%(title+' '+description, i*10))
    #                 WebDriverWait(driver0, 10, 0.5, ignored_exceptions=TimeoutException).until(
    #                     lambda x: x.find_element(By.XPATH, "//div[@mu]").is_displayed())
    #                 break
    #             except Exception as err:
    #                 driver0.quit()
    #                 ips = requests.get('http://localhost:5555/random').text
    #                 driver0 = FirefoxSetOptions(ips, load_normal=True)
    #                 continue
    #         try:
    #             res_url = driver0.find_element(By.XPATH, "//div[contains(@mu, 'qq_42059060')]").get_attribute('mu')
    #             if res_url == url:
    #                 res = driver0.find_element(By.XPATH, "//div[contains(@mu, 'qq_42059060')]//a").get_attribute('href')
    #                 final_res[title] = res
    #                 break
    #         except Exception as err:
    #             final_res[title] = url
    #             continue
    #     print(title, final_res[title])
    #     driver0.quit()
    #     time.sleep(4)
    #
    # final_res = Manager().dict()
    # p = ThreadPool(5)
    # pool_res = []
    # for title in pages.keys():
    #     if title in pgs.keys():
    #         final_res[title] = pgs[title]
    #     else:
    #         res = p.apply_async(page_load, args=(pages, title, final_res))
    #         pool_res.append(res)
    #         time.sleep(1)
    # while len(pool_res) > 0:
    #     if pool_res[0].ready():
    #         pool_res.pop(0)
    #
    # final_res = dict(final_res)
    # with open('urls.json', 'w+') as fp:
    #     r = json.dumps(final_res, ensure_ascii=False)
    #     fp.write(r)

    return final_res


def main(selenium_flag=False):
    # last_stamp = time.time()
    pages = getSrcPages()
    page_urls = list(pages.values())
    pool_len = 20
    results = []
    index = 0
    p = ThreadPool(pool_len)
    gap = len(pages) // pool_len

    while True:
        # try:
        if len(results) >= pool_len and results[0].ready():
            results.pop(0)
        else:
            sleep(0.1)

        if len(results) < pool_len:
            ips = requests.get('http://localhost:5555/random').text
            print(ips)
            # page_split = random.sample(list(pages.values()), gap)
            if index == pool_len - 1:
                page_split = page_urls[index * gap:] if selenium_flag is True else page_urls[::-1 ** index]
                index = 0
            else:
                page_split = page_urls[index * gap:(index + 1) * gap] if selenium_flag is True else page_urls[::-1 ** index]
                index += 1
            # print(page_split)
            # spider(ips, page_split)
            res = p.apply_async(spider, args=(ips, page_split))
            results.append(res)
            sleep(1)


    # except Exception as err:
    #     print(err)
    #     sleep(1)
    #     continue


if __name__ == '__main__':
   main()