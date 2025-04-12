from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('products/', views.products, name='products'),
    path('payment/<int:product_id>/', views.payment, name='payment'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('contact/', views.contact, name='contact'),
    path('contact_done/', views.contact_done, name='contact_done'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('cart-checkout/', views.cart_checkout, name='cart_checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),


]
