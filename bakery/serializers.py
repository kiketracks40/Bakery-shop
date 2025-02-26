from rest_framework import serializers
from .models import Customer, Product, Sale, SaleItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    
    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price']

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True, read_only=True)
    cashier_name = serializers.ReadOnlyField(source='cashier.username')
    
    class Meta:
        model = Sale
        fields = ['id', 'date_time', 'cashier', 'cashier_name', 'payment_method', 'total', 'items']
        read_only_fields = ['date_time']
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__' 

class SaleCreateSerializer(serializers.ModelSerializer):
    items = serializers.ListField(
        child=serializers.DictField(), 
        write_only=True
    )
    
    class Meta:
        model = Sale
        fields = ['payment_method', 'items']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        # Set cashier to current user
        validated_data['cashier'] = self.context['request'].user
        # Calculate total from items
        total = 0
        
        # Create the sale with initial total
        validated_data['total'] = total
        sale = Sale.objects.create(**validated_data)
        
        # Create each sale item and update total
        for item_data in items_data:
            product = Product.objects.get(pk=item_data['product_id'])
            quantity = item_data['quantity']
            price = product.price
            
            SaleItem.objects.create(
                sale=sale,
                product=product,
                quantity=quantity,
                price=price
            )
            
            # Update product quantity
            product.quantity -= quantity
            product.save()
            
            # Add to total
            total += price * quantity
        
        # Update sale with correct total
        sale.total = total
        sale.save()
        
        return sale
    
