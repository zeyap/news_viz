from celery import task

from time import sleep
import time

from newsdemo.settings.base import CELERY_RESULT_BACKEND,BROKER_URL
from celery import Celery
app = Celery('tasks', backend=CELERY_RESULT_BACKEND, broker=BROKER_URL,include=['newsdemo.apps.crawler.tasks'])

# from newsdemo.settings.base import CELERY_RESULT_BACKEND,BROKER_URL
# from celery import Celery
# app = Celery('tasks', backend='amqp://localhost', broker='amqp://localhost')

from newsdemo.apps.crawler import crawlers
from newsdemo.apps.crawler import link_grabber

INTERVAL = 10
news_crawlers = {
    'netease':crawlers.neteaseCrawler(),
    'sina':crawlers.sinaCrawler(),
    'qq':None,
    'weibo':None
}

websites = [
    {'name':'netease','url':'news.163.com'},
    {'name':'sina','url':'sina.com.cn'},
    {'name':'qq','url':'news.qq.com'},
    {'name':'weibo','url':'weibo.com'}]

def get_headlines():
    return ['harry potter','高考']

def crawl(headline):
    pages = link_grabber.getlink(headline)

    for page in pages:
        for website in websites:
            crawler = news_crawlers[website['name']]
            if page['link'].find(website['url'])>-1 and crawler:
                crawler.run(page['link'])
                time.sleep(INTERVAL)

@app.task
def schedule_crawler():
    while(True):
        headlines = get_headlines()
        for headline in headlines:
            print(headline)
            crawl(headline)
            time.sleep(INTERVAL)
        