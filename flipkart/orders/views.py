from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Order


def order_success(request):
    return render(
        request,
        'orders/order_success.html'
    )


@login_required(login_url='login')
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders,
        }
    )


@login_required(login_url='login')
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
        }
    )


@login_required(login_url='login')
def cancel_order(request, order_id):

    # =========================================
    # GET ORDER
    # =========================================

    if request.user.is_staff:

        # Admin can cancel any user's order
        order = get_object_or_404(
            Order,
            id=order_id
        )

    else:

        # User can cancel only their own order
        order = get_object_or_404(
            Order,
            id=order_id,
            user=request.user
        )


    # =========================================
    # ONLY POST REQUEST
    # =========================================

    if request.method == 'POST':

        # Only pending or processing orders
        # can be cancelled

        if order.status in ['pending', 'processing']:

            # Return products to stock

            for item in order.items.all():

                product = item.product

                product.stock += item.quantity

                product.save()


            # Change order status

            order.status = 'cancelled'

            order.save()


    # =========================================
    # REDIRECT
    # =========================================

    if request.user.is_staff:

        # Admin → Order Detail

        return redirect(
            'admin_order_detail',
            order_id=order.id
        )

    # User → My Orders

    return redirect('my_orders')