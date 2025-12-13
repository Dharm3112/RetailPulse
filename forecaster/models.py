from django.db import models

class Product(models.Model):
    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Clothing', 'Clothing'),
        ('Home', 'Home'),
        ('Books', 'Books'),
        ('Toys', 'Toys'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    current_stock_level = models.IntegerField(default=0)
    reorder_point = models.IntegerField(default=10, help_text="Stock level at which to alert")
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    quantity_sold = models.IntegerField()
    sale_date = models.DateTimeField()
    total_revenue = models.DecimalField(max_digits=15, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Auto-calculate revenue
        self.total_revenue = self.product.price * self.quantity_sold
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} - {self.quantity_sold}"