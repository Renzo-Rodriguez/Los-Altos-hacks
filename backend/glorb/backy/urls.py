from django.urls import path
from . import views

urlpatterns = [
    path('/request', views.wants, name='members'),
    path('/ai', views.ai)
    path('',views.home)
    path('/login', views.log)
    path('/upload', views.upload)
]

