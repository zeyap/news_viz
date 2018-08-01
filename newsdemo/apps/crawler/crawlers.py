import logging

from django.utils import timezone

from newsdemo.apps.crawler.newspiece import StandardNewsPiece

class BaseCrawler(object):
    def __init__(self, service):
        self.service = service
    
    def run(self):
        print('crawler run')
        info = {
            "author":'somebody33',
            "posted_date":'20180801',
            "title":'title of the news',
            "text":'fake content139407187801'
        }
        news = self.service(info)
        try:
            print('a record is saving to es')
            news.save()
        except Exception as err:
            print('attempt to save a record in es failed. ',self.service, err)
            pass

class TestCrawler(BaseCrawler):
    def __init__(self):
        print('test crawler init')
        super(TestCrawler,self).__init__(StandardNewsPiece)
        
