from django.contrib import admin
from .models import Product, Order
from .models import ContactMessage

admin.site.register(ContactMessage)

admin.site.register(Product)
admin.site.register(Order)