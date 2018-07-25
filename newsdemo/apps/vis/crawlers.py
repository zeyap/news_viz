import logging

from django.utils import timezone

from newsdemo.apps import NewsPiece

class AbstractBaseCrawler(object):
    def __init__(self, service):
        self.service = service
    
    def run(self):
        print('crawler run')
        try:
            news = self.service(
                title='title of the news',
                text='fake content139407187801'
            )
            news.save();
            print('a record saved to es')
        except:
            pass

class TestCrawler(AbstractBaseCrawler):
    def __init__(self):
        print('test crawler init')
        super(TestCrawler,self).__init__(NewsPiece)
        
