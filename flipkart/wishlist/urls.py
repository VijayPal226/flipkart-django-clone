from django.urls import path
from . import views


urlpatterns = [

    # Wishlist Page
    path(
        '',
        views.wishlist,
        name='wishlist'
    ),

    # Add / Remove Wishlist
    path(
        'toggle/<int:product_id>/',
        views.toggle_wishlist,
        name='toggle_wishlist'
    ),

    # Remove From Wishlist Page
    path(
        'remove/<int:product_id>/',
        views.remove_wishlist,
        name='remove_wishlist'
    ),

]