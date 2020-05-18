from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.register),
    path('send_code/', views.get_code),
    path('login_vaild/', views.login_vaild),
    path('login_pwd/', views.login_pwd),
    path('logout/', views.logout),
    path('set_pwd', views.set_pwd)
]