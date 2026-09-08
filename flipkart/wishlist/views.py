from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render,redirect
from django.http import JsonResponse
from products.models import Product
from .models import Wishlist


# =========================
# Toggle Wishlist
# =========================

@login_required(login_url='login')
def toggle_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    wishlist_item = Wishlist.objects.filter(
        user=request.user,
        product=product
    ).first()

    if wishlist_item:

        wishlist_item.delete()

        added = False

    else:

        Wishlist.objects.create(
            user=request.user,
            product=product
        )

        added = True

    # Current Wishlist Count
    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    # AJAX request ke liye JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':

        return JsonResponse({
            'success': True,
            'added': added,
            'wishlist_count': wishlist_count
        })

    return redirect('wishlist')
# =========================
# Wishlist Page
# =========================

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('product')

    return render(
        request,
        'wishlist/wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


# =========================
# Remove From Wishlist
# =========================

@login_required
def remove_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    Wishlist.objects.filter(
        user=request.user,
        product=product
    ).delete()

    return redirect('wishlist')