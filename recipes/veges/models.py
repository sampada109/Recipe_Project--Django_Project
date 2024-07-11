from django.db import models
from django.contrib.auth.models import User      #for user data
from django.utils import timezone
from django.db.models.signals import post_save     #A signal provided by Django that is sent at the end of the save method of a model.
from django.dispatch import receiver               # A decorator that connects the create_user_profile function to the post_save signal of the User model.

# Create your models here.

class Tags(models.Model):    #21
    tag = models.CharField(max_length=50)



class recp_category(models.Model):    #23
    category = models.CharField(max_length=50)



class recipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)     #14th commit
    recp_name = models.CharField(max_length=100)
    recp_desp = models.TextField()
    recp_img = models.ImageField(upload_to='recipe_img')
    recp_create_date = models.DateTimeField(default=timezone.now)     #21
    recp_last_modified_date = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(Tags) 
    category = models.ForeignKey(recp_category, on_delete=models.SET_NULL, null=True, blank=True)
    ratings = models.IntegerField(default=0)   
    views = models.PositiveIntegerField(default=0)
    favourites = models.PositiveIntegerField(default=0)



class comments(models.Model):      #22
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(recipes, on_delete=models.CASCADE)
    com_text = models.TextField()
    com_date = models.DateTimeField(default=timezone.now)


class Profile(models.Model):     #28
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_img = models.ImageField(upload_to='profile_img', default='profile_img/default_profile_img.png', blank=True, null=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)