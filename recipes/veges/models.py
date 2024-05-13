from django.db import models
from django.contrib.auth.models import User      #for user data
from django.utils import timezone

# Create your models here.

class tags(models.Model):    #21
    tag = models.CharField(max_length=50)

class recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)     #14th commit
    recp_name = models.CharField(max_length=100)
    recp_desp = models.TextField()
    recp_img = models.ImageField(upload_to='recipe_img')
    recp_create_date = models.DateTimeField(default=timezone.now)     #21
    recp_last_modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(tags)    