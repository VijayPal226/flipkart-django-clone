from django.contrib import admin
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        'name',
        'category',
        'price',
        'stock',
        'is_featured',
        'created_at',
    )

    list_filter = (
        'category',
        'is_featured',
    )

    search_fields = (
        'name',
        'description',
    )