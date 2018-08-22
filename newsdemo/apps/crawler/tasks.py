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

import pprint
from googleapiclient.discovery import build

INTERVAL = 100
news_crawlers = (
    # crawlers.TestCrawler(),
    crawlers.neteaseCrawler(),
    crawlers.sinaCrawler()
)

def getlink():
    service = build("news viz", "v1",
            developerKey="AIzaSyBth5uhNWogGsZT9LbT6pvXaUkSR1BwwWM")

    res = service.cse().list(
        q= "keyword",
        cx="017050252471438770433:cygqcpwrs7c",
        num=3
     ).execute()
    pprint.pprint(res)

def crawl():
    print('crawl()')
    for crawler in news_crawlers:
        crawler.run()
        time.sleep(INTERVAL)

@app.task
def schedule_crawler():
    while(True):
        crawl()
        time.sleep(INTERVAL)