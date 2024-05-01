from django.db import models

# Create your models here.

class recipes(models.Model):
    recp_name = models.CharField(max_length=100)
    recp_desp = models.TextField()
    recp_img = models.ImageField(upload_to='recipe_img')