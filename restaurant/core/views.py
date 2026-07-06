from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request,'core/index.html')

def about(request):
    return render(request,'core/about.html')

def menu(request):
    return render(request,'core/menu.html')

def chefs(request):
    return render(request,'core/chefs.html')

def reservation(request):
    return render(request,'core/reservation.html')

def reviewes(request):
    return render(request,'core/reviews.html')

def contact(request):
    return render(request,'core/contact.html')