from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

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
    if request.method == "POST":
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        person = request.POST.get('person')
        reservation_date = request.POST.get('date')
        reservation_time = request.POST.get('time')
        special_requests = request.POST.get('special_requests')

        Reservation.objects.create(name=name,phone=phone,email=email,guest=person,reservation_date=reservation_date,reservation_time=reservation_time,special_requests=special_requests)
        
        return redirect('reservation')
    
    return render(request,'core/reservation.html')

def reviewes(request):
    return render(request,'core/reviews.html')

def contact(request):
    return render(request,'core/contact.html')