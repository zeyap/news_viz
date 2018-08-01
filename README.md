# configurations

newsdemo: the main project

newsdemo/apps/viz: the app for user interfaces

newsdemo/apps/crawler: all methods of crawlers

# run the project

### STEP 1. Install celery:

$ pip install celery
$ pip install django-celery

Install RabbitMq [here](https://www.rabbitmq.com/download.html) and start it on your computer

$ python manage.py migrate --settings=newsdemo.settings.local

### STEP 2. Open 2 consoles:

Start the user interface process:
$ python manage.py runserver --settings=newsdemo.settings.local

Start the auto-crawler process:
$ python manage.py celery worker --loglevel=info --settings=newsdemo.settings.local

# Write your own crawler and test it

See example in newsdemo/apps/crawler/crawlers.py - **class TestCrawler**
