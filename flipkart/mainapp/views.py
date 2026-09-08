from django.shortcuts import render
from products.models import Product,Category
from django.shortcuts import get_object_or_404
from wishlist.models import Wishlist
from django.db.models import Q
from django.core.paginator import Paginator

def home(request):

    featured_products = Product.objects.filter(
        is_featured=True
    ).order_by('-created_at')

    latest_products = Product.objects.filter(
        is_featured=False
    ).order_by('-created_at')

    wishlist_product_ids = []

    if request.user.is_authenticated:
        wishlist_product_ids = list(
            Wishlist.objects.filter(
                user=request.user
            ).values_list('product_id', flat=True)
        )

    return render(request, 'mainapp/home.html', {
        'featured_products': featured_products,
        'latest_products': latest_products,
        'wishlist_product_ids': wishlist_product_ids,
    })

def category_products(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    products = Product.objects.filter(
        category=category
    ).order_by('-created_at')

    return render(request, 'mainapp/category_products.html', {
        'category': category,
        'products': products,
    })

def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(request, 'mainapp/product_detail.html', {
        'product': product,
    })

def search_products(request):

    query = request.GET.get('q', '').strip()

    sort = request.GET.get('sort', '').strip()

    price_min = request.GET.get('price_min', '')
    price_max = request.GET.get('price_max', '')

    category_id = request.GET.get('category', '')

    products = Product.objects.none()

    if query:

        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

        # Minimum Price
        if price_min:

            products = products.filter(
                price__gte=price_min
            )

        # Maximum Price
        if price_max:

            products = products.filter(
                price__lte=price_max
            )

        # Category
        if category_id:

            products = products.filter(
                category_id=category_id
            )

        # Sorting
        if sort == 'price_low':

            products = products.order_by('price')

        elif sort == 'price_high':

            products = products.order_by('-price')

        else:

            products = products.order_by('-created_at')

        paginator = Paginator(
            products,8
        )
        page_number =  request.GET.get('page')
        page_obj = paginator.get_page(
            page_number
        )

    return render(
        request,
        'mainapp/search_results.html',
        {
            'products': page_obj,

            'page_obj':page_obj,

            'query': query,

            'sort': sort,

            'price_min': price_min,

            'price_max': price_max,

            'category_id': category_id,
            
            'categories': Category.objects.all(),
        }
    )