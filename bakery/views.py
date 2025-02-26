from .models import Product, Sale, SaleItem, Customer
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import CustomerSerializer, ProductSerializer, SaleCreateSerializer, SaleSerializer
from .permissions import IsManager
from .serializers import ProductSerializer, SaleSerializer
from bakery import models
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from django.http import HttpResponse
import csv
from datetime import datetime, timedelta, timezone


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsManager()]
        return [IsAuthenticated()]
    
    def get_queryset(self):
        queryset = Product.objects.all()
        category = self.request.query_params.get('category')
        in_stock = self.request.query_params.get('in_stock')
        
        if category:
            queryset = queryset.filter(category=category)
        
        if in_stock and in_stock.lower() == 'true':
            queryset = queryset.filter(quantity__gt=0)
            
        return queryset
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        """Return products with inventory below threshold"""
        low_stock = Product.objects.filter(quantity__lt=models.F('alert_threshold'))
        serializer = self.get_serializer(low_stock, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_inventory(self, request):
        """Bulk update product inventory levels"""
        updates = request.data
        updated_products = []
        
        for item in updates:
            try:
                product = Product.objects.get(pk=item['product_id'])
                product.quantity = item['new_quantity']
                product.save()
                updated_products.append({
                    'id': product.id,
                    'name': product.name,
                    'quantity': product.quantity
                })
            except Product.DoesNotExist:
                pass
                
        return Response({
            'updated': len(updated_products),
            'products': updated_products
        })

class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [IsAuthenticated]

def get_serializer_class(self):
    if self.action == 'create':
        return SaleCreateSerializer
    return SaleSerializer    



class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
       queryset = Customer.objects.all()
       search = self.request.query_params.get('search')
       if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) | 
                models.Q(email__icontains=search) | 
                models.Q(phone__icontains=search)
           )
       return queryset
    
@login_required
def daily_sales_report(request):
    date_str = request.GET.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = timezone.now().date()
    
    # Get sales for the date
    sales = Sale.objects.filter(date_time__date=date)
    
    # Total sales and revenue
    total_sales = sales.count()
    total_revenue = sales.aggregate(Sum('total'))['total__sum'] or 0
    
    # Sales by hour
    sales_by_hour = []
    for hour in range(24):
        hour_sales = sales.filter(date_time__hour=hour)
        sales_by_hour.append({
            'hour': hour,
            'count': hour_sales.count(),
            'revenue': sum(sale.total for sale in hour_sales)
        })
    
    # Sales by payment method
    payment_methods = sales.values('payment_method').annotate(
        count=Count('id'),
        revenue=Sum('total')
    )
    
    context = {
        'date': date,
        'total_sales': total_sales,
        'total_revenue': total_revenue,
        'sales_by_hour': sales_by_hour,
        'payment_methods': payment_methods
    }
    
    return render(request, 'bakery/reports/daily_sales.html', context)

@login_required
def product_popularity_report(request):
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Default to last 30 days if not specified
    if not date_from or not date_to:
        date_to = timezone.now().date()
        date_from = date_to - timedelta(days=30)
    else:
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    
    # Get all sale items in the date range
    sales = Sale.objects.filter(
        date_time__date__gte=date_from,
        date_time__date__lte=date_to
    )
    
    sale_items = SaleItem.objects.filter(sale__in=sales)
    
    # Get product popularity data
    products_data = {}
    total_quantity = 0
    total_revenue = 0
    
    for item in sale_items:
        product_id = item.product.id
        if product_id not in products_data:
            products_data[product_id] = {
                'product_id': product_id,
                'product_name': item.product.name,
                'total_quantity': 0,
                'total_revenue': 0
            }
        
        products_data[product_id]['total_quantity'] += item.quantity
        item_revenue = item.price * item.quantity
        products_data[product_id]['total_revenue'] += item_revenue
        
        total_quantity += item.quantity
        total_revenue += item_revenue
    
    # Calculate percentages
    for product_id, data in products_data.items():
        data['percentage_of_sales'] = (data['total_quantity'] / total_quantity * 100) if total_quantity > 0 else 0
    
    # Sort by quantity sold
    product_list = sorted(
        products_data.values(), 
        key=lambda x: x['total_quantity'], 
        reverse=True
    )
    
    context = {
        'date_from': date_from,
        'date_to': date_to,
        'products': product_list,
        'total_quantity': total_quantity,
        'total_revenue': total_revenue
    }
    
    return render(request, 'bakery/reports/product_popularity.html', context)

@login_required
def export_report(request):
    report_type = request.GET.get('report_type')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    format = request.GET.get('format', 'csv')
    
    # Create the CSV response
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{report_type}_{date_from}_to_{date_to}.csv"'
    
    writer = csv.writer(response)
    
    # Export different reports based on type
    if report_type == 'product_popularity':
        # Header row
        writer.writerow(['Product', 'Quantity Sold', 'Revenue', '% of Sales'])
        
        # Get data (simplified version of the product_popularity_report logic)
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
        
        sales = Sale.objects.filter(
            date_time__date__gte=date_from,
            date_time__date__lte=date_to
        )
        
        # Calculate product data
        # ... (similar to product_popularity_report but writing to CSV)
    
    return response
