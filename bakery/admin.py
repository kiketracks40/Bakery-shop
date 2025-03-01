from django.contrib import admin
from .models import Product, Sale, SaleItem, Customer

# Register your models with the admin site
admin.site.register(Product)
admin.site.register(Sale)
admin.site.register(SaleItem)
admin.site.register(Customer)