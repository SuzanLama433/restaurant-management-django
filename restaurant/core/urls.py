from django.urls import path
from .views import *
urlpatterns = [
     path('',index,name='index'),
     path('about/',about,name='about'),
     path('menu/',menu,name='menu'),
     path('chefs/',chefs,name='chefs'),
     path('reservation/',reservation,name='reservation'),
     path('reviewes/',reviewes,name='reviewes'),
     path('contact/',contact,name='contact'),
     
     # Cart URLs
     path('cart/', view_cart, name='cart'),
     path('add-to-cart/', add_to_cart, name='add_to_cart'),
     path('update-cart-item/', update_cart_item, name='update_cart_item'),
     path('remove-from-cart/', remove_from_cart, name='remove_from_cart'),
     path('clear-cart/', clear_cart, name='clear_cart'),
]
