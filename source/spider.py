# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 16:39:42 2018

@author: hasee
"""

from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from newspaper import Article
import requests
import time
t=0.5

def get_news_pool():
    news_pool = []
    for i in range(200,243):
        temp=442-i
        target = 'http://news.nankai.edu.cn/nkyw/system/more/32000000/0002/32000000_00000'+str(temp)+'.shtml'
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('a', class_ = 'news')
        for i in range(len(texts)):
            url=str(texts[i])
            start=url.find('http')
            end=url.find('shtml')+5
            url=url[start:end]
            news_pool.append(url)
        time.sleep(t)
            
    for i in range(100,200):
        temp=299-i
        target = 'http://news.nankai.edu.cn/nkyw/system/more/32000000/0001/32000000_00000'+str(temp)+'.shtml'
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('a', class_ = 'news')
        for i in range(len(texts)):
            url=str(texts[i])
            start=url.find('http')
            end=url.find('shtml')+5
            url=url[start:end]
            news_pool.append(url)
        time.sleep(t)
            
    for i in range(0,99):
        temp=99-i
        if temp<10:
            temp='00'+str(temp)
        else: 
            temp='0'+str(temp)
        target = 'http://news.nankai.edu.cn/nkyw/system/more/32000000/0000/32000000_00000'+str(temp)+'.shtml'
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html)
        texts = bf.find_all('a', class_ = 'news')
        for i in range(len(texts)):
            url=str(texts[i])
            start=url.find('http')
            end=url.find('shtml')+5
            url=url[start:end]
            news_pool.append(url)
        time.sleep(t)
    return(news_pool)
    
def get_news():
    news=get_news_pool()
    return news
    
def crawl_news(news_pool,min_body_len,doc_dir_path,doc_encoding):
    i=1
    for news in news_pool:
        article=Article(news,language='zh')
        try:
            article.download()
            article.parse()
        except Exception as e:
            print("-----%s: %s-----"%(type(e), news))
            continue
        doc=ET.Element("doc")
        ET.SubElement(doc, "id").text = "%d"%(i)
        ET.SubElement(doc, "url").text = news
        ET.SubElement(doc, "title").text = article.title
        ET.SubElement(doc, "datetime").text = str(article.publish_date)
        ET.SubElement(doc, "body").text = article.text
        tree = ET.ElementTree(doc)
        tree.write(doc_dir_path + "%d.xml"%(i), encoding = doc_encoding, xml_declaration = True)
        i += 1
        
if __name__ == '__main__':
    news=get_news()
    crawl_news(news,50,'..\\data\\news\\','utf-8')