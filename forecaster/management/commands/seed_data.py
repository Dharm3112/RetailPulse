import random
from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from forecaster.models import Product, Sale


class Command(BaseCommand):
    help = 'Populate database with dummy retail data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Clean old data
        Sale.objects.all().delete()
        Product.objects.all().delete()

        # 2. Create Products
        categories = ['Electronics', 'Clothing', 'Home', 'Books', 'Toys']
        products = []

        for i in range(1, 51):
            prod = Product.objects.create(
                name=f"Product {i}",
                category=random.choice(categories),
                current_stock_level=random.randint(0, 100),
                reorder_point=random.randint(5, 20),
                price=random.uniform(10.0, 500.0)
            )
            products.append(prod)

        # 3. Create Sales (Last 365 days)
        sales_to_create = []
        end_date = timezone.now()
        start_date = end_date - timedelta(days=365)

        for _ in range(600):
            product = random.choice(products)
            qty = random.randint(1, 5)

            # Random timestamp logic
            random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            sale_date = start_date + timedelta(seconds=random_seconds)

            revenue = product.price * qty

            sales_to_create.append(Sale(
                product=product,
                quantity_sold=qty,
                sale_date=sale_date,
                total_revenue=revenue
            ))

        # Bulk create is much faster than looping .save()
        Sale.objects.bulk_create(sales_to_create)

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(products)} products and {len(sales_to_create)} sales.'))