from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
# newspiece to be indexed into ElasticSearch
class NewsPiece(models.Model):
   author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blogpost')
   posted_date = models.DateField(default=timezone.now)
   title = models.CharField(max_length=200)
   text = models.TextField(max_length=1000)

# def indexing(self):
#     obj = NewsPieceIndex(
#         meta={'id':self.id},
#         author=self.author,
#         posted_date=self.posted_date,
#         title=self.title,
#         text=self.text
#     )
#     obj.save()
#     return obj.to_dict(include_meta=True)
