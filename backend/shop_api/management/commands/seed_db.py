import json
from django.core.management.base import BaseCommand
from shop_api.models import Product

class Command(BaseCommand):
    help = 'Seeds the database with product data from a JSON file.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='The path to the JSON file to load.')

    def handle(self, *args, **options):
        json_file_path = options['json_file']
        
        with open(json_file_path, 'r', encoding='utf-8') as f:
            products_data = json.load(f)
        
        self.stdout.write(self.style.NOTICE('Starting to seed the database...'))
        
        for product_item in products_data:
            # Determine is_trending and is_new_arrival from the JSON data
            is_trending = product_item.get('is_trending', False)
            is_new_arrival = product_item.get('is_new_arrival', False)
            
            product, created = Product.objects.update_or_create(
                name=product_item['name'],
                defaults={
                    'description': product_item['description'],
                    'price': product_item['price'],
                    'discount': product_item.get('discount', 0.0),
                    'is_trending': is_trending,
                    'is_new_arrival': is_new_arrival,
                    'product_type': product_item['product_type'],
                    'image_url': product_item['image_url']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Successfully created product: {product.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'Successfully updated product: {product.name}'))
        
        self.stdout.write(self.style.SUCCESS('Database seeding complete.'))