import random
from datetime import datetime, timedelta
import pytz
from django.core.management.base import BaseCommand
from your_app.models import Product, Sale  # CHANGE 'your_app' to your actual app name


class Command(BaseCommand):
    help = 'Populate database with dummy retail data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # 1. Clear existing data
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

        # 3. Create Sales (Last 12 Months)
        sales_to_create = []
        end_date = datetime.now(pytz.UTC)
        start_date = end_date - timedelta(days=365)

        for _ in range(600):  # Generate 600 sales
            product = random.choice(products)
            qty = random.randint(1, 5)

            # Random time within the year
            random_seconds = random.randint(0, int((end_date - start_date).total_seconds()))
            sale_date = start_date + timedelta(seconds=random_seconds)

            # Logic: Calculate revenue now or let model .save() handle it.
            # Since we use bulk_create for speed, we calculate manually here.
            revenue = product.price * qty

            sales_to_create.append(Sale(
                product=product,
                quantity_sold=qty,
                sale_date=sale_date,
                total_revenue=revenue
            ))

        Sale.objects.bulk_create(sales_to_create)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {len(products)} products and {len(sales_to_create)} sales.'))