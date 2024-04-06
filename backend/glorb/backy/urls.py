from django.urls import path
from . import views

urlpatterns = [
    path('/request', views.wants, name='members'),
    path('/ai', veiws.ai)
    path('',veiws.home)
    path('/login', veiws.log)
]

