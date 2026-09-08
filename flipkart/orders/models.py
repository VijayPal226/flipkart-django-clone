from django.db import models
from products.models import Product
from django.contrib.auth.models import User


class Order(models.Model):

    user = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    related_name='orders',
    null= True,
    blank=True
    )

    full_name = models.CharField(
        max_length=200
    )

    mobile = models.CharField(
        max_length=15
    )

    email = models.EmailField()

    address = models.TextField()

    city = models.CharField(
        max_length=100
    )

    pincode = models.CharField(
        max_length=10
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    status = models.CharField(
        max_length=50,
        choices=[
            ('pending','pending'),
            ('processing','processing'),
            ('shipped','shipped'),
            ('Delivered','Delivered'),
            ('cancelled','cancelled'),
        ],
        default='pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )

    quantity = models.PositiveIntegerField(
        default=1
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    def get_total_price(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"