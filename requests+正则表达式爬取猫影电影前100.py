# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:14:41 2020

@author: REGGIE
"""

#首先要进行对目标站点的网页分析
#1.抓取单页的内容，利用request请求目标站点，得到单个页面HTML代码，返回结果。
#2.正则表达式分析，根据HTML分析得到电影的名称，主演，上映时间，评分，图片链接等信息。
#3.保存至文件，通过文件的形式保存，每一部电影一个结果，一行json字符串。
#4.开启循环以及多线程。对多网页内容遍历，开启多线程提取，提高抓取速度。

import requests
from requests.exceptions import RequestException
import re
import json
#多进程爬取
from multiprocessing import Pool

headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
    }

#页面的请求
def get_one_page(url):
    try:
        res = requests.get(url,headers = headers)
        if res.status_code == 200:
            return res.text
        return None
    except RequestException:
        return None
    
#网页的解析
def parse_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(\d+)</i>.*?data-src="(.*?)".*?name"><a.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>.*?</dd>',re.S)
    items = re.findall(pattern,html)
    
    #对得到的信息进行格式化
    for item in items:
        yield{
            'index':item[0],
            'name':item[1],
            'title':item[2],
            'actor':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5] + item[6]
        }

#把抓取到的信息直接存储为文件,使用json.dumps把数据转为json格式(ensure_ascii= False 输出中文)
def write_to_file(content):
    with open('result.txt','a') as f:
        f.write(json.dumps(content, ensure_ascii= False)+ '\n')
        f.close()

     
def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    for item in parse_page(html):
        print(item)
        write_to_file(item)
        
if __name__ == '__main__':
    for i in range(10):
        main(i*10)
    #pool = Pool()
    #pool.map(main, [i*10 for i in range(10)])