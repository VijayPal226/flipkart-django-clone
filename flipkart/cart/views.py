from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem


def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    # Out of stock check
    if product.stock <= 0:
        return redirect('cart_detail')

    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.filter(
            id=cart_id
        ).first()
    else:
        cart = None

    if cart is None:
        cart = Cart.objects.create()
        request.session['cart_id'] = cart.id

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    # Maximum stock check
    if not created:

        if cart_item.quantity >= product.stock:
            return redirect('cart_detail')

        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

def increase_quantity(request, item_id):

    cart_item = get_object_or_404(
        CartItem,
        id=item_id
    )

    product = cart_item.product

    # Maximum stock limit
    if cart_item.quantity < product.stock:

        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart_detail')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(
        CartItem,
        id = item_id 
    ) 
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart_detail')

def cart_detail(request):

    cart_id = request.session.get('cart_id')

    if cart_id:
        cart = Cart.objects.filter(
            id=cart_id
        ).first()
    else:
        cart = None

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
    })

def remove_from_cart(request,item_id):

    cart_item = get_object_or_404(
        CartItem,
        id = item_id
    )
    cart_item.delete()
    return redirect('cart_detail')

@login_required(login_url='login')
def checkout(request):

    cart_id = request.session.get('cart_id')

    if not cart_id:
        return redirect('cart_detail')

    cart = Cart.objects.filter(
        id=cart_id
    ).first()

    if not cart or not cart.items.exists():
        return redirect('cart_detail')

    if request.method == 'POST':

        from orders.models import Order, OrderItem

        # Step 1: Check stock for all products first
        for item in cart.items.all():

            product = item.product

            if product.stock < item.quantity:

                return redirect('cart_detail')


        # Step 2: Create order only after stock is confirmed
        order = Order.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            mobile=request.POST.get('mobile'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            pincode=request.POST.get('pincode'),
            total_amount=cart.get_total_price()
        )


        # Step 3: Reduce stock and create order items
        for item in cart.items.all():

            product = item.product

            product.stock -= item.quantity
            product.save()

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                price=product.price
            )


        # Step 4: Empty cart
        cart.items.all().delete()

        return redirect('order_success')


    return render(
        request,
        'cart/checkout.html',
        {
            'cart': cart,
        }
    )