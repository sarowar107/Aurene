# shop_api/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from django.db import IntegrityError
from decimal import Decimal

# Import your own Product model
from .models import Product

# Your existing ProductSerializer and UserSerializer
class ProductSerializer(serializers.ModelSerializer):
    discountPrice = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'discountPrice', 'image_url', 
                  'product_type', 'is_trending', 'is_new_arrival']

    def get_discountPrice(self, obj):
        if obj.discount > 0:
            discount_percentage = obj.discount / Decimal('100.0')
            discount_amount = discount_percentage * obj.price
            discounted_price = obj.price - discount_amount
            return float(discounted_price)
        return None
