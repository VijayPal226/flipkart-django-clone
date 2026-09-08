
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.models import Profile
from orders.models import Order
from wishlist.models import Wishlist
from cart.models import Cart


@login_required(login_url='login')
def user_dashboard(request):


    # ==============================
    # USER PROFILE
    # ==============================

    profile, created = Profile.objects.get_or_create(
        user=request.user
    )


    # ==============================
    # USER ORDERS
    # ==============================

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    total_orders = orders.count()

    recent_orders = orders[:5]


    # ==============================
    # USER WISHLIST
    # ==============================

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()


    # ==============================
    # USER CART
    # ==============================

    cart_id = request.session.get('cart_id')

    cart = None
    cart_count = 0

    if cart_id:

        cart = Cart.objects.filter(
            id=cart_id
        ).first()

        if cart:

            cart_count = sum(
                item.quantity
                for item in cart.items.all()
            )


    # ==============================
    # DASHBOARD
    # ==============================

    context = {

        'profile':profile,

        'total_orders': total_orders,

        'wishlist_count': wishlist_count,

        'cart_count': cart_count,

        'recent_orders': recent_orders,

    }

    return render(
        request,
        'userpanel/dashboard.html',
        context
    )

