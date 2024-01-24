# myapp/urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('books/', book_list, name='book_list'),
    path('leaderboards/', leaderboards, name='leaderboards'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact')
]
