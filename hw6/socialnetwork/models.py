from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    text = models.CharField(max_length=10000)
    user = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    date_time = models.DateTimeField()

class Profile(models.Model):
    user_bio = models.CharField(max_length=10000)
    user = models.OneToOneField(User, default=None, on_delete=models.PROTECT)
    picture = models.FileField(blank=True)
    follow = models.ManyToManyField(User, related_name="followers")
    content_type = models.CharField(max_length=50)

class Comment(models.Model):
    text = models.CharField(max_length=10000)
    creator = models.ForeignKey(User, default=None, on_delete=models.PROTECT)
    creation_time = models.DateTimeField()
    post = models.ForeignKey(Post, default=None, on_delete=models.PROTECT)
    



