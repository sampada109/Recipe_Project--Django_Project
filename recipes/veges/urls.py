from django.urls import path
from . import views


urlpatterns = [
    path('', views.home , name='home'),
    path('user/', views.users , name='users'),
    path('delete_recp/<id>', views.delete_recp , name='delete_recp'),
]