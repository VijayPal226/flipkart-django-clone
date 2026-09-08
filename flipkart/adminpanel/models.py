from django.db import models

# Create your models here.


class StoreSettings(models.Model):

    store_name = models.CharField(
        max_length=200,
        default='My Store'
    )

    store_email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.store_name



class NotificationSettings(models.Model):
    new_order = models.BooleanField(default=True)
    new_customer = models.BooleanField(default=True)
    low_stock = models.BooleanField(default=True)
    payment_notification = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    dashboard_alerts = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Notification Settings"

class PaymentSettings(models.Model):
    PAYMENT_MODE_CHOICES = [
        ('test', 'Test Mode'),
        ('live', 'Live Mode'),
    ]

    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee (INR)'),
        ('USD', 'US Dollar (USD)'),
        ('EUR', 'Euro (EUR)'),
        ('GBP', 'British Pound (GBP)'),
    ]

    payment_enabled = models.BooleanField(default=True)

    payment_mode = models.CharField(
        max_length=10,
        choices=PAYMENT_MODE_CHOICES,
        default='test'
    )

    currency = models.CharField(
        max_length=10,
        choices=CURRENCY_CHOICES,
        default='INR'
    )

    stripe_enabled = models.BooleanField(default=True)

    cod_enabled = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Payment Settings"

class WebsiteSettings(models.Model):
    website_name = models.CharField(
        max_length=200,
        default='My Store'
    )

    description = models.TextField(
        blank=True
    )

    contact_email = models.EmailField(
        blank=True
    )

    contact_phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    website_active = models.BooleanField(
        default=True
    )

    customer_registration = models.BooleanField(
        default=True
    )

    orders_enabled = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.website_name




    