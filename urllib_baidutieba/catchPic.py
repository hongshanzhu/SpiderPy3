#用Python3的语法写了一个简单抓取网页图片的实例
## -*- coding:utf-8 -*-
__author__ = 'zhs'

import urllib.request
import urllib.error
import os, time, re
import urllib


#根据给定的网址来获取网页详细信息，得到的html就是网页的源代码
def getHtml(url):
    webheader = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'
    }
    req = urllib.request.Request(url=url, headers=webheader)
    try:
        page = urllib.request.urlopen(req)
        print("geturl打印信息：%s" % (page.geturl()))
        print('**********************************************')
        print("info打印信息：%s" % (page.info()))
        print('**********************************************')
        print("getcode打印信息：%s" % (page.getcode()))
        html = page.read()
        print(page.getcode())
        return html.decode('UTF-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        elif hasattr(e, "reason"):
            print(e.reason)
        return ""


#获取网址下所有页面
def getAllPages(number, url):
    #获取主网址下的共number个页面的源代码，放在pagesHtml中
    pagesHtml = []
    for pageIndex in range(1, number + 1):
        urlnew = url + '?pn=' + str(pageIndex)
        pageHtml = getHtml(urlnew)
        pagesHtml.append(pageHtml)
    return pagesHtml


#获取该网址下共有多少页
def getPageNumber(html):
    #利用正则表达式来从网页源代码中分析得到页面数
    reg = '<span class="red">(.*?)</span>'  #根据正则表达式找到该网址下共有多少个页面
    numre = re.compile(reg)
    number = numre.findall(html)
    return int(number[0])  #可能会找到好几个这个数字，只需取出第一个，并转为整型


#获取网页中某个页面的所有图片的地址
def getAllImg(page):
        #利用正则表达式把源代码中的图片地址过滤出来
        #reg = r'src="(.+?\.jpg)" pic_ext'
        reg = r'src="http(s)?://.+\.(jp(e)?g|png|gif)" pic_ext='
        imgre = re.compile(reg)
        imglist = imgre.findall(page)  #表示在整个页面中过滤出所有图片的地址，放在imglist中
        return imglist


# 输入文件名，保存多张图片
def saveImages(imglist, name, p, totalImg):
    x = 1
    for imgurl in imglist:
        print("imgurl:" + imgurl)
        y = str(p) + str("页") + str(x)
        urllib.request.urlretrieve(imgurl, '{}{}.jpg'.format(
            paths, y))  #打开imglist中保存的图片网址，并下载图片保存在本地，format格式化字符串
        print("正在抓取第%d张图片..." % (totalImg))
        x += 1
        totalImg += 1
    if totalImg == 1:
        print("没有抓到图片")
    return totalImg


def getImg(html, paths):
    #reg = r'src="(.+?\.jpg)" pic_ext'
    reg = r'src="http(s)?://.+\.(jp(e)?g|png)" pic_ext'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)  #表示在整个网页中过滤出所有图片的地址，放在imglist中
    print(imglist)
    return imglist


# 递归创建文件夹
def mkdir(path):
    # 将图片保存到./文件夹中
    if not os.path.isdir(path):
        os.makedirs(path)
    paths = path + '/'  #保存在./{time}/路径下
    return paths


if __name__ == '__main__':
    url = input("请输入被抓取URL,例如:http://tieba.baidu.com/p/2460150866\n")
    urlArr = url.split('/')
    today = time.strftime('%Y%m%d%H%M', time.localtime())
    path = "./" + urlArr[2] + today

    paths = mkdir(path)

    html = getHtml(url)  #获取该网址网页详细信息，得到的html就是网页的源代码
    if html == "":
        print("异常退出")
    else:
        print("抓取的页面:", html)
        filePath = paths + "html.txt"
        f = open(filePath, "w+", encoding='utf-8')
        f.write("抓取的页面:\n")
        f.write(html)
        f.close()
        # 得到该贴吧网址下共有多少个页面
        pageNumber = getPageNumber(html)
        #pageNumber = 2
               
        print("抓取的总页数:", pageNumber)
        # 获取所有的页面的源代码，从中分析出图片
        pagesHtml = getAllPages(pageNumber, url)
        x = 1
        totalImg = 1
        for pageHtml in pagesHtml:
            #获取每个页面下的所有图片地址列表
            imglist = getAllImg(pageHtml)  #获取图片的地址列表
            totalImg = saveImages(imglist, paths, x, totalImg)  #保存图片
            print("已经保存了第%d页的所有图片..." % (x))
            x += 1
