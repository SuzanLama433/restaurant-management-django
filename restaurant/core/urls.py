from django.urls import path
from .views import *
urlpatterns = [
     path('',index,name='index'),
     path('about/',about,name='about'),
     path('menu/',menu,name='menu'),
     path('chefs/',chefs,name='chefs'),
     path('reservation/',reservation,name='reservation'),
     path('reviewes/',reviewes,name='reviewes'),
     path('contact/',contact,name='contact')
    
]
