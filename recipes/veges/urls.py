from django.urls import path
from . import views


urlpatterns = [
    path('', views.home , name='home'),
    path('user/', views.users , name='users'),
    path('delete_recp/<id>', views.delete_recp , name='delete_recp'),
    path('update_recp/<id>', views.update_recp , name='update_recp'),
    path('user_login/', views.user_login , name='user_login'),
    path('user_signup/', views.user_signup , name='user_signup'),
]