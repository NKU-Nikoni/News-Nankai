# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 17:20:13 2018

@author: hasee
"""

from spider import get_news_pool
from spider import crawl_news
from index import IndexModule
from datetime import *
import configparser


def crawling():
    print('-----start crawling time: %s-----'%(datetime.today()))
    config = configparser.ConfigParser()
    config.read('..\\config.ini', 'utf-8')
    news_pool = get_news_pool()
    crawl_news(news_pool, 140, config['DEFAULT']['doc_dir_path'], config['DEFAULT']['doc_encoding'])
    
if __name__ == "__main__":
    print('-----start time: %s-----'%(datetime.today()))
    
    #抓取新闻数据
    #crawling()
    
    #构建索引
    print('-----start indexing time: %s-----'%(datetime.today()))
    im = IndexModule('..\\config.ini', 'utf-8')
    im.construct_postings_lists()
    