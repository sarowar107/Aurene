from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    # Original price
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Discount percentage (e.g., 10 for 10%)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    
    # Boolean fields for categories
    is_trending = models.BooleanField(default=False)
    is_new_arrival = models.BooleanField(default=False)
    
    # Simple choices for product type
    TYPE_CHOICES = [
        ('saree', 'Saree'),
        ('panjabi', 'Panjabi'),
    ]
    product_type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    image_url = models.URLField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.name