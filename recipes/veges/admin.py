from django.contrib import admin
from .models import *


# Register your models here.
admin.site.register(tags)
admin.site.register(recp_category)
admin.site.register(recipes)
admin.site.register(comments)
admin.site.register(Profile)