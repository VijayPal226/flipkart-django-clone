from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<int:category_id>/',views.category_products,name='category_products' ),
    path('product/<int:product_id>/',views.product_detail,name='product_detail'),

    path('search/',views.search_products, name='search_products'),
]