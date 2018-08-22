import logging

from urllib import request
from bs4 import BeautifulSoup
import xlrd
import jieba
import time

from django.utils import timezone

from newsdemo.apps.crawler.newspiece import StandardNewsPiece

from bs4 import BeautifulSoup

from urllib import request

class BaseCrawler(object):
    def __init__(self, service):
        self.service = service
    
    def run(self):
        example_data_crawled = {
            "author":'somebody',
            "posted_date":'20180801',
            "title":'title of the news',
            "text":'fake content139407187801'
        }
        self.save(example_data_crawled)

    def save(self,info):
        print('crawler run')
        news = self.service(info)
        try:
            print('a record is saving to es')
            news.save()
        except Exception as err:
            print('attempt to save a record in es failed. ',self.service, err)
            pass

# example
class TestCrawler(BaseCrawler):
    def __init__(self):
        print('test crawler init')
        super(TestCrawler,self).__init__(StandardNewsPiece)
    
    def run(self):
        res = self.myCrawlingMethod(); # write your own method to crawl some specific websites
        # self.save(res);# uncomment this line to save result in elasticsearch
        
    def myCrawlingMethod(self):
        example_data_crawled = {
            "author":'somebody33',
            "posted_date":'20180801',
            "title":'title of the news',
            "text":'fake content139407187801'
        }
        print('result',example_data_crawled)
        return example_data_crawled

# crawler for news.163.com
class neteaseCrawler(BaseCrawler):
    def __init__(self):
        print('netease crawler init')
        super(neteaseCrawler,self).__init__(StandardNewsPiece)
    
    test_link = 'http://news.163.com/14/0928/08/A77DFRRT00014JB6.html'

    def run(self,link = test_link):
        self.link = link
        res = self.myCrawlingMethod();
        
    def myCrawlingMethod(self):
        #example page
        #link = "http://news.163.com/14/0928/08/A77DFRRT00014JB6.html" 
        data_crawled = self.get_news_text()
        # print('result of neteaseCrawler',data_crawled)
        return data_crawled
        
    def get_news_text(self):
        download_url = self.link
        head = {}
        head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        download_req = request.Request(url = download_url, headers = head)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('GBK','ignore')
        soupTexts = BeautifulSoup(download_html, 'lxml')     
        news_text = {
            "author":'',
            "posted_date":'',
            "title":'',
            "text":''
        }
        #title        
        divs = soupTexts.find_all(class_ = 'post_content_main')
        for div in divs:
            title = div.h1.get_text()
        news_text["title"] = title
        #author      
        source = soupTexts.find_all(class_ = 'post_time_source')
        for div in source:
            author = div.a.get_text()
        news_text["author"] = author       
        #time       
        for div in source:
            source = div.get_text()
        public_time = []
        for char in source:
            if ((char == "\n") or (char == "\t") or (char == "\r") or (char == " ")):
                source = source.replace(char,"")
            else:
                break
        for num in source:
            if (num != "\u3000"):
                public_time.append(num)
            else:
                break
        time_str = ''.join(public_time)
        print (time_str)
        time_tuple = time.strptime(time_str, '%Y-%m-%d%H:%M:%S')
        news_text["posted_date"] = time_tuple
        #text
        source = soupTexts.find_all(class_ = 'post_text')
        text = ''
        for div in source:
            para = soupTexts.find_all("p")
            for p in para:
                if p.find_all(class_= "f_center"):
                    continue
                text += p.get_text()

        text = text.replace("\n","")
        news_text["text"] = text
        # print (news_text)
        return news_text

# crawler for http://news.sina.com.cn/
class sinaCrawler(BaseCrawler):
    def __init__(self):
        print('sina crawler init')
        super(sinaCrawler,self).__init__(StandardNewsPiece)
    
    test_link = "http://edu.sina.com.cn/gaokao/2018-08-13/doc-ihhqtawy1746376.shtml"
    
    def run(self,link = test_link):
        self.link = link
        res = self.myCrawlingMethod();
        
    def myCrawlingMethod(self):
        #example page
        #link = "http://edu.sina.com.cn/gaokao/2018-08-13/doc-ihhqtawy1746376.shtml" 
        data_crawled = self.get_news_text()
        print('result of sinaCrawler',data_crawled)
        return data_crawled
        
    def get_news_text(self):
        download_url = self.link
        head = {}
        head['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        download_req = request.Request(url = download_url, headers = head)
        download_response = request.urlopen(download_req)
        download_html = download_response.read().decode('UTF-8','ignore')
        soupTexts = BeautifulSoup(download_html, 'lxml')
        news_text = {
            "author":'',
            "posted_date":'',
            "title":'',
            "text":''
        }
        #title
        divs = soupTexts.find_all(class_ = 'main-content w1240')
        for div in divs:
            title = div.h1.get_text()
        news_text["title"] = title      
        #time
        div = soupTexts.find(class_ = 'date-source')
        span = div.find_all('span')
        source = span[0].get_text()
        try:
            author = span[1].get_text()
        except IndexError:
            author = div.a.get_text()
        public_time = []
        for char in source:
            if ((char == "\n") or (char == "年") or (char == "月") or (char == "日")or (char == " ")):
                source = source.replace(char,"")
        for num in source:
            if (num != "\u3000"):
                public_time.append(num)
            else:
                break
        time_str = ''.join(public_time)
        print (time_str)
        time_tuple = time.strptime(time_str, '%Y%m%d%H:%M')
        news_text["posted_date"] = time_tuple        
        #author
        news_text["author"] = author        
        #text
        text_source = soupTexts.find(class_ = 'article')
        text = ''
        para = text_source.find_all("p")
        for p in para:
            text += p.get_text()
        text = text.replace("\u3000","")
        news_text["text"] = text             
        # print (news_text)
        return news_text