from django.db import models
from django.contrib.auth.models import User      #for user data

# Create your models here.

class recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)     #14th commit
    recp_name = models.CharField(max_length=100)
    recp_desp = models.TextField()
    recp_img = models.ImageField(upload_to='recipe_img')