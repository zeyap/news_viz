# configurations

newsdemo: the main project
> wsgi.py: create a second thread with a crawler coroutine running every 5 minutes

apps/viz: the app that provide data to user interfaces and for data visualization purpose

apps/NewsPiece: the app where NewsPiece model(for database) is declared. [Django Model](http://www.runoob.com/django/django-model.html)

# run the project

Run with local setting:

$ python manage.py runserver --settings=newsdemo.settings.local

# interact with database

Reference: [Use elasticsearch as database in Django](https://github.com/sabricot/django-elasticsearch-dsl)


