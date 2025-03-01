from django.db import models
from django.contrib.auth.models import User
 

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    alert_threshold = models.PositiveIntegerField(default=5)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'cash'),
        ('CARD', 'card'),
    ]
    
    date_time = models.DateTimeField(auto_now_add=True)
    cashier = models.ForeignKey(User, on_delete=models.PROTECT)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    
    def __str__(self):
        return f"Sale #{self.id} - {self.date_time.strftime('%Y-%m-%d %H:%M')}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    


class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    
    def __str__(self):
        return self.name