from django.urls import path
from . import views


urlpatterns = [

    path(
        'dashboard/',
        views.dashboard,
        name='admin_dashboard'
    ),

    path(
        'products/',
        views.products,
        name='admin_products'
    ),

    path(
        'products/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    path(
        'products/<int:product_id>/edit/',
        views.edit_product,
        name='edit_product'
    ),

    path(
        'order/<int:order_id>/',
        views.admin_order_detail,
        name='admin_order_detail'
    ),

    path(
    'products/<int:product_id>/delete/',
    views.delete_product,
    name='delete_product'
),


    path(
    'wishlist/',
    views.admin_wishlist,
    name='admin_wishlist'
),

path(
    'orders/',
    views.admin_orders,
    name='admin_orders'
),

path(
    'orders/<int:order_id>/update-status/',
    views.update_order_status,
    name='update_order_status'
),

path(
    'categories/',
    views.admin_categories,
    name='admin_categories'
),

path(
    'categories/add/',
    views.add_category,
    name='add_category'
),

path(
    'categories/<int:category_id>/edit/',
    views.edit_category,
    name='edit_category'
),

path(
    'categories/<int:category_id>/delete/',
    views.delete_category,
    name='delete_category'
),
path(
    'customers/',
    views.admin_customers,
    name='admin_customers'
),

path(
    'reports/',
    views.admin_reports,
    name='admin_reports'
),

path(
    'products/add/',
    views.add_product,
    name='add_product'
),

path('settings/',
    views.admin_settings, 
    name='admin_settings'
),

path(
    'settings/admin-profile/',
    views.admin_profile_settings,
    name='admin_profile_settings'
),

path( 'settings/store/',
    views.store_settings,
    name='store_settings' ),


path(
    'settings/security/',
    views.admin_security_settings,
    name='admin_security_settings'
),

path( 'settings/notifications/',
    views.admin_notification_settings,
    name='admin_notification_settings'
),

path(
    'settings/payment/',
    views.admin_payment_settings,
    name='admin_payment_settings'
),



path(
    'settings/website/',
    views.admin_website_settings,
    name='admin_website_settings'
),



]