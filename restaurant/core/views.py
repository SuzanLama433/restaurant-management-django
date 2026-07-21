from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
import json

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
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()
        phone = request.POST.get("phone", "").strip()
        subject = request.POST.get("subject", "").strip()
        message = request.POST.get("message", "").strip()
        
        # 1. Check required fields
        if not name or not email or not subject or not message:
            messages.error(request, "Please fill in all required fields.")
            return redirect("contact")
        
        # 2. Validate email format
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request,"Enter a valid email")
            return render('contact')
        #check duplicate email
        if Contact.objects.filter(email=email).exists():
            messages.warning(request,'this email is already exist')
            return render('contact')

        Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
        )

        messages.success(request, "Your message has been sent successfully!")
        return redirect("contact")

    return render(request, "core/contact.html")


# ==================== CART VIEWS ====================

def get_or_create_cart(request):
    """Get or create a cart for the current session/user"""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_id = request.session.session_key
        if not session_id:
            request.session.create()
            session_id = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart


@require_POST
def add_to_cart(request):
    """Add item to cart via AJAX"""
    try:
        data = json.loads(request.body)
        menu_item_id = data.get('menu_item_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            quantity = 1
        
        menu_item = MenuItem.objects.get(id=menu_item_id)
        cart = get_or_create_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            menu_item=menu_item,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        cart.save()  # Update the updated_at timestamp
        
        return JsonResponse({
            'success': True,
            'message': f'{menu_item.title} added to cart!',
            'cart_count': cart.get_total_items(),
            'total': str(cart.get_total())
        })
    except MenuItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Menu item not found'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid data'}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@require_GET
def view_cart(request):
    """Display cart page"""
    from decimal import Decimal
    
    cart = get_or_create_cart(request)
    total = cart.get_total()
    delivery = Decimal('100')  # Rs 100
    grand_total = total + delivery
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total': total,
        'delivery': delivery,
        'grand_total': grand_total,
        'total_items': cart.get_total_items(),
    }
    return render(request, 'core/cart.html', context)


@require_POST
def update_cart_item(request):
    """Update quantity of cart item"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        quantity = int(data.get('quantity', 1))
        
        if quantity < 1:
            quantity = 1
        
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart = get_or_create_cart(request)
        
        if cart_item.cart != cart:
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
        
        cart_item.quantity = quantity
        cart_item.save()
        cart.save()
        
        return JsonResponse({
            'success': True,
            'subtotal': str(cart_item.get_subtotal()),
            'cart_total': str(cart.get_total()),
            'cart_count': cart.get_total_items(),
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


@require_POST
def remove_from_cart(request):
    """Remove item from cart"""
    try:
        data = json.loads(request.body)
        cart_item_id = data.get('cart_item_id')
        
        cart_item = CartItem.objects.get(id=cart_item_id)
        cart = get_or_create_cart(request)
        
        if cart_item.cart != cart:
            return JsonResponse({'success': False, 'message': 'Unauthorized'}, status=403)
        
        cart_item.delete()
        cart.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Item removed from cart',
            'cart_total': str(cart.get_total()),
            'cart_count': cart.get_total_items(),
        })
    except CartItem.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Cart item not found'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)


def clear_cart(request):
    """Clear all items from cart"""
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    cart.save()
    
    messages.success(request, 'Cart cleared')
    return redirect('cart')

def log_in(request):
    return render(request, 'account/login.html')