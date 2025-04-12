from django.db import models
from django.utils import timezone

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name

class Order(models.Model):
    PAYMENT_CHOICES = [
        ('cod', 'Cash on Delivery'),
        ('qr', 'QR Code'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    first_name = models.CharField(max_length=50, default="Unknown")
    last_name = models.CharField(max_length=50, default="Unknown")
    phone = models.CharField(max_length=15, default="0000000000")
    email = models.EmailField(default="unknown@example.com")
    address = models.TextField(default="Unknown")

    payment_mode = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default="qr")
    payment_screenshot = models.ImageField(upload_to='payment_screenshots/', null=True, blank=True)

    payment_status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"
class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=100, blank=True, null=True)  # For guest users

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def total_price(self):
        return self.product.price * self.quantity
    


class WebsiteUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    email = models.EmailField()

    def __str__(self):
        return self.username
