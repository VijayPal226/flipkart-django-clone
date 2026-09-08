from django.urls import path
from . import views

urlpatterns = [

    path('success/', views.order_success, name='order_success'),

    path('my-orders/',views.my_orders,name='my_orders'),

    path('detail/<int:order_id>/', views.order_detail,name='order_detail'),

    path('cancel/<int:order_id>/',views.cancel_order, name='cancel_order'),
]