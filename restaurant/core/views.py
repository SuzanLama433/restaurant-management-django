from django.shortcuts import render
from .models import *

# Create your views here.

def index(request):
    return render(request,'core/index.html')

def about(request):
    return render(request,'core/about.html')

def menu(request):
    category = MenuCategory.objects.prefetch_related('items__tags').all()
    gallery = Gallery.objects.all()
    
    context = {
        'categories': category,
        'gallery': gallery,
    }
    return render(request,'core/menu.html',context)

def chefs(request):
    chefs = Chefs.objects.filter(is_active = True)
    
    return render(request,'core/chefs.html',{'chefs':chefs})

def reservation(request):
    return render(request,'core/reservation.html')

def reviewes(request):
    return render(request,'core/reviews.html')

def contact(request):
    return render(request,'core/contact.html')