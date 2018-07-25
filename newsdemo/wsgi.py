"""
WSGI config for newsdemo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

import threading
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "newsdemo.settings")
application = get_wsgi_application()

from time import sleep
import time
import asyncio

from newsdemo.apps.vis import crawlers

FIVE_MINUTES = 5
news_crawlers = (
    crawlers.TestCrawler(),
)

async def crawl():
    print('1')
    for crawler in news_crawlers:
        
        crawler.run()
        asyncio.sleep(FIVE_MINUTES)

    print('2')
    await asyncio.sleep(FIVE_MINUTES)

def schedule_crawler():
    print('a new crawler is scheduled')
    def do_create_task():
        loop.call_soon(crawl)
    loop.call_soon_threadsafe(do_create_task)
    threading.Timer(FIVE_MINUTES, schedule_crawler).start()

global loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
# loop.run_forever()
# print('a')

threads = [];
threads.append(threading.Thread(target=schedule_crawler,args=()))

def thread_run(threads):
    for t in threads:
        t.setDaemon(False)
        t.start()
        t.join()
    
    print("all over")

thread_run(threads)