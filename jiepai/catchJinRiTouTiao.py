import json
from urllib.parse import urlencode
from requests.exceptions import RequestException
import requests
from bs4 import BeautifulSoup
import os, time, re
from hashlib import md5
from multiprocessing import Pool
from config import *
def get_page_index(offset,keyword):
    data={
        "offset": offset,
        "format": "json",
        "keyword": keyword,
        "autoload": "true",
        "count": 20,
        "cur_tab": 1
    }
    url = "http://www.toutiao.com/search_content/?" + urlencode(data)
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print("请求索引页出错")
        return None

def parse_page_index(html):
    data= json.loads(html)
    if data and "data" in data.keys():
        for item in data.get("data"):
            yield item.get("article_url")

def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print("请求详情页出错",url)
        return None

def parse_page_detail(html,url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select("title")[0].get_text()
    print("title:",title)
    images_pattern = re.compile("gallery: (.*?),\n",re.S)
    result = re.search(images_pattern,html)
    if result:
        print("匹配结果;",result)
        print("匹配结果;", result.group(1))
        data= json.loads(result.group(1))
        if data and "sub_images" in data.keys():
            sub_images = data.get("sub_images")
            images = [item.get('url') for item in sub_images]
            for img in images :
                download_image(img)
            return {
                "title":title,
                "url":url,
                "images":images
            }
    else:
        print("no find gallery:")
        reg = r'src=\&quot;(.*?)\&quot;'
        imgre = re.compile(reg)
        imglist = imgre.findall(html)  # 表示在整个网页中过滤出所有图片的地址，放在imglist中
        for img in imglist:
            download_image(img)
        return {
            "title": title,
            "url": url,
            "images": imglist
        }
def download_image(url):
    print("正在下载图片",url)
    try:
        response = requests.get(url)
        if response.status_code==200:
            save_images(response.content)
            #return response.text
        return None
    except RequestException:
        print("请求图片出错",url)
        return None

# 递归创建文件夹
def mkdir(path):
    # 将图片保存到./文件夹中
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path + '/'  #保存在./{time}/路径下
    return paths

def save_images(content):
    today = time.strftime('%Y%m%d%H%M', time.localtime())
    file_path = mkdir("./jinritoutiao/"+ today )
    file_path = file_path + "{1}.{2}".format(os.getcwd(),md5(content).hexdigest(),"jpg")
    with open(file_path,"wb") as f:
        f.write(content)
        f.close()
def main(offset):
    html = get_page_index(offset,KEYWORD)
    print("索引页",html)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        print("详情页url", url)
        if html:
            print("解析详情页:"+html)
            result = parse_page_detail(html, url)
if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [x*20 for x in range(0,10+1)])