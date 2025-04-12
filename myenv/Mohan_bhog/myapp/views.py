from django.shortcuts import render, redirect, get_object_or_404
from .forms import ContactForm, PaymentForm
from .models import Product, Order , CartItem

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def products(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def payment(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == "POST":
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            order = Order.objects.create(
                product=product,
                quantity=form.cleaned_data['quantity'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                address=form.cleaned_data['address'],
                payment_mode=form.cleaned_data['payment_mode'],
                payment_screenshot=form.cleaned_data.get('payment_screenshot'),
                payment_status='Completed'
            )
            return redirect('payment_done')
    else:
        form = PaymentForm(initial={'product_name': product.name})

    return render(request, 'payment.html', {'form': form, 'product': product})

def payment_done(request):
    return render(request, 'payment_done.html')

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact_done')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def contact_done(request):
    return render(request, 'contact_done.html')

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    session_key = request.session.session_key

    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        session_key=session_key,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
    cart_items = CartItem.objects.filter(session_key=session_key)
    total = sum(item.total_price() for item in cart_items)

    # Optional: if you want to redirect after form submission
    if request.method == "POST":
        # You can loop through cart_items and create Orders here if needed
        return redirect('payment_done')  # Or your success page

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })
from django.http import JsonResponse
from .models import CartItem, Product

from django.shortcuts import redirect, get_object_or_404

def update_cart(request, item_id):
    if request.method == 'POST':
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id)

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        cart_item.save()

    return redirect('cart')

from django.views.decorators.csrf import csrf_exempt

from django.shortcuts import render, redirect
from .models import CartItem, Order
from django.utils import timezone

from django.utils import timezone
from django.shortcuts import render, redirect
from .models import CartItem, Order

def cart_checkout(request):
    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        session_key = request.session.session_key

    cart_items = CartItem.objects.filter(session_key=session_key)

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()
        payment_mode = request.POST.get('payment_mode', 'cod').strip()
        payment_screenshot = request.FILES.get('payment_screenshot')

        for item in cart_items:
            Order.objects.create(
                product=item.product,
                quantity=item.quantity,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                address=address,
                payment_mode=payment_mode,
                payment_screenshot=payment_screenshot if payment_mode == 'qr' else None,
                payment_status='Completed',
                created_at=timezone.now()
            )

        cart_items.delete()
        return redirect('payment_done')

    total = sum(item.total_price() for item in cart_items)
    return render(request, 'payment_card.html', {'cart_items': cart_items, 'total': total})

from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from .models import WebsiteUser
from django.contrib import messages

  # Your custom user model

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if user already exists
        if WebsiteUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('signup')  # ✅ stay on signup page to show error

        # Save new user
        WebsiteUser.objects.create(username=username, email=email, password=password)
        
        messages.success(request, 'Signup successful! Please login.')
        return redirect('login')

    return render(request, 'signup.html')



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = WebsiteUser.objects.filter(username=username, password=password).first()
        if user:
            request.session['username'] = user.username
            request.session['email'] = user.email
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')

    return render(request, 'login.html')


def logout_view(request):
    request.session.flush()
    return redirect('home')
