import logging

from django.utils import timezone

from newsdemo.apps.crawler.newspiece import StandardNewsPiece

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
        
        
