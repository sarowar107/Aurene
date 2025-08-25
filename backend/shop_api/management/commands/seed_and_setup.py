import os
import json
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from shop_api.models import Product

class Command(BaseCommand):
    help = 'Creates a superuser and seeds the database with product data.'

    def handle(self, *args, **options):
        # 1. Create a Superuser non-interactively
        User = get_user_model()
        # Correctly retrieving environment variables by their key names
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

        if not all([username, email, password]):
            self.stdout.write(self.style.ERROR('Superuser environment variables are not set. Skipping superuser creation.'))
        else:
            if not User.objects.filter(username=username).exists():
                try:
                    User.objects.create_superuser(username=username, email=email, password=password)
                    self.stdout.write(self.style.SUCCESS(f'Superuser {username} created successfully.'))
                except IntegrityError:
                    self.stdout.write(self.style.WARNING('Superuser might already be created in a parallel process.'))
            else:
                self.stdout.write(self.style.SUCCESS('Superuser already exists. Skipping creation.'))
        
        self.stdout.write("-" * 20)
        
        # 2. Delete All Existing Products
        self.stdout.write(self.style.NOTICE('Deleting all existing products from the database...'))
        Product.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All existing products deleted.'))
        self.stdout.write("-" * 20)

        # 3. Seed Data from JSON
        # Path to your JSON fixture file
        json_file_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'products_data.json')

        if not os.path.exists(json_file_path):
            self.stdout.write(self.style.ERROR(f'JSON file not found at {json_file_path}. Skipping data seeding.'))
            return
            
        with open(json_file_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
            
        self.stdout.write(self.style.NOTICE('Starting to seed the database...'))
        
        for product_item in products_data:
            product, created = Product.objects.update_or_create(
                name=product_item['name'],
                defaults={
                    'description': product_item['description'],
                    'price': product_item['price'],
                    'discount': product_item.get('discount', 0.0),
                    'is_trending': product_item.get('is_trending', False),
                    'is_new_arrival': product_item.get('is_new_arrival', False),
                    'product_type': product_item['product_type'],
                    'image_url': product_item['image_url']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Successfully updated product: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))