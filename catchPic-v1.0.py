#用Python3的语法写了一个简单抓取网页图片的实例
## -*- coding:utf-8 -*-
__author__ = 'zhs'

import urllib.request
import os, time,re
import urllib

#根据给定的网址来获取网页详细信息，得到的html就是网页的源代码  
def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html.decode('UTF-8')

def getImg(html,paths):
    reg = r'src="(.+?\.jpg)" pic_ext'
    imgre = re.compile(reg)
    imglist = imgre.findall(html)#表示在整个网页中过滤出所有图片的地址，放在imglist中
    x = 1      
    
    for imgurl in imglist:  
        urllib.request.urlretrieve(imgurl,'{}{}.jpg'.format(paths,x))  #打开imglist中保存的图片网址，并下载图片保存在本地，format格式化字符串
        print("正在抓取第%d张图片..."% (x))
        x = x + 1
    if x==1 :
      print("没有抓到图片")
    else:
      print("抓取完毕!!!")
    return imglist


# 递归创建文件夹
def mkdir(path):     
   # 将图片保存到./文件夹中
    if not os.path.isdir(path):  
       os.makedirs(path)  
    paths = path+'/'      #保存在./{time}/路径下
    return paths

if __name__ == '__main__':
  url=input("请输入被抓取URL,例如:http://tieba.baidu.com/p/2460150866\n")
  urlArr= url.split('/')
  today=time.strftime('%Y%m%d%H%M', time.localtime())
  path = "./"+urlArr[2]+today
       
  paths = mkdir(path)
  
  html = getHtml(url)#获取该网址网页详细信息，得到的html就是网页的源代码
  print("抓取的页面:",html)
  getImg(html,paths) #从网页源代码中分析并下载保存图片
