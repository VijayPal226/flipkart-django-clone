import json
from django.contrib import messages
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Count,Q
from django.db.models.functions import TruncMonth
from products.models import Product, Category
from .models import StoreSettings, NotificationSettings, PaymentSettings,WebsiteSettings
from orders.models import Order, OrderItem
from wishlist.models import Wishlist


def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin, login_url='login')
def admin_settings(request):
    return render(request, 'adminpanel/settings.html')


@user_passes_test(is_admin, login_url='login')
def admin_order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order,
        }
    )


@user_passes_test(is_admin, login_url='login')
def dashboard(request):

    # =========================================
    # BASIC STATISTICS
    # =========================================

    total_users = User.objects.filter(
        is_staff=False
    ).count()

    total_products = Product.objects.count()

    total_categories = Category.objects.count()

    total_orders = Order.objects.count()

    total_wishlist = Wishlist.objects.count()


    featured_products = Product.objects.filter(
        is_featured=True
    ).count()


    # =========================================
    # REVENUE
    # =========================================

    total_revenue = Order.objects.filter(
        status__in=[
            'processing',
            'shipped',
            'Delivered'
        ]
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0


    # =========================================
    # ORDER STATUS
    # =========================================

    pending_orders = Order.objects.filter(
        status='pending'
    ).count()

    processing_orders = Order.objects.filter(
        status='processing'
    ).count()

    shipped_orders = Order.objects.filter(
        status='shipped'
    ).count()

    delivered_orders = Order.objects.filter(
        status='Delivered'
    ).count()


    # =========================================
    # OUT OF STOCK
    # =========================================

    out_of_stock = Product.objects.filter(
        stock=0
    ).count()


    # =========================================
    # LOW STOCK PRODUCTS
    # =========================================

    low_stock_products = Product.objects.filter(
        stock__gt=0,
        stock__lte=5
    ).order_by('stock')[:5]


    # =========================================
    # RECENT ORDERS
    # =========================================

    recent_orders = Order.objects.select_related(
        'user'
    ).order_by(
        '-created_at'
    )[:6]


    # =========================================
    # RECENT CUSTOMERS
    # =========================================

    recent_customers = User.objects.filter(
        is_staff=False
    ).order_by(
        '-date_joined'
    )[:5]


    # =========================================
    # TOP SELLING PRODUCTS
    # =========================================

    top_products = Product.objects.annotate(
        total_sold=Sum('orderitem__quantity')
    ).order_by(
        '-total_sold'
    )[:5]


    # =========================================
    # MONTHLY SALES
    # =========================================

    monthly_sales = Order.objects.filter(
        status__in=[
            'processing',
            'shipped',
            'Delivered'
        ]
    ).annotate(
        month=TruncMonth('created_at')
    ).values(
        'month'
    ).annotate(
        revenue=Sum('total_amount')
    ).order_by('month')


    chart_labels = []
    chart_data = []

    for sale in monthly_sales:

        chart_labels.append(
            sale['month'].strftime('%b')
        )

        chart_data.append(
            float(sale['revenue'] or 0)
        )


    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'total_users': total_users,

        'total_products': total_products,

        'total_categories': total_categories,

        'total_orders': total_orders,

        'total_wishlist': total_wishlist,

        'featured_products': featured_products,

        'total_revenue': total_revenue,

        'pending_orders': pending_orders,

        'processing_orders': processing_orders,

        'shipped_orders': shipped_orders,

        'delivered_orders': delivered_orders,

        'out_of_stock': out_of_stock,

        'low_stock_products': low_stock_products,

        'recent_orders': recent_orders,

        'recent_customers': recent_customers,

        'top_products': top_products,

        'chart_labels': json.dumps(chart_labels),

        'chart_data': json.dumps(chart_data),

    }

    return render(
        request,
        'adminpanel/dashboard.html',
        context
    )


# =========================================
# ADMIN PRODUCTS
# =========================================

@user_passes_test(is_admin, login_url='login')
def products(request):

    # =========================================
    # SEARCH
    # =========================================

    search = request.GET.get(
        'search',
        ''
    ).strip()


    # =========================================
    # CATEGORY FILTER
    # =========================================

    category = request.GET.get(
        'category',
        ''
    ).strip()


    # =========================================
    # STOCK FILTER
    # =========================================

    stock_status = request.GET.get(
        'stock',
        ''
    ).strip()


    # =========================================
    # ALL PRODUCTS
    # =========================================

    products = Product.objects.select_related(
        'category'
    ).all().order_by(
        '-created_at'
    )


    # =========================================
    # SEARCH FILTER
    # =========================================

    if search:

        products = products.filter(

            Q(name__icontains=search) |

            Q(description__icontains=search)

        )


    # =========================================
    # CATEGORY FILTER
    # =========================================

    if category:

        products = products.filter(
            category_id=category
        )


    # =========================================
    # STOCK FILTER
    # =========================================

    if stock_status == 'in_stock':

        products = products.filter(
            stock__gt=5
        )

    elif stock_status == 'low_stock':

        products = products.filter(
            stock__gt=0,
            stock__lte=5
        )

    elif stock_status == 'out_of_stock':

        products = products.filter(
            stock=0
        )


    # =========================================
    # CATEGORIES
    # =========================================

    categories = Category.objects.all().order_by(
        'name'
    )


    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'products': products,

        'categories': categories,

        'search': search,

        'category': category,

        'stock_status': stock_status,

    }


    return render(
        request,
        'adminpanel/products.html',
        context
    )

# =========================================
# PRODUCT DETAIL
# =========================================

@user_passes_test(is_admin, login_url='login')
def product_detail(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    return render(
        request,
        'adminpanel/product_detail.html',
        {
            'product': product,
        }
    )

# =========================================
# EDIT PRODUCT
# =========================================

@user_passes_test(is_admin, login_url='login')
def edit_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':

        product.name = request.POST.get('name', '').strip()

        product.description = request.POST.get(
            'description',
            ''
        ).strip()

        product.category_id = request.POST.get(
            'category'
        ) or None

        product.price = request.POST.get(
            'price'
        ) or 0

        product.stock = request.POST.get(
            'stock'
        ) or 0

        product.is_featured = (
            request.POST.get('is_featured') == 'on'
        )

        if request.FILES.get('image'):

            product.image = request.FILES['image']

        product.save()

        return redirect(
            'product_detail',
            product_id=product.id
        )

    return render(
        request,
        'adminpanel/product_edit.html',
        {
            'product': product,
            'categories': categories,
        }
    )

# =========================================
# DELETE PRODUCT
# =========================================

@user_passes_test(is_admin, login_url='login')
def delete_product(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.method == 'POST':

        product.delete()

        return redirect(
            'admin_products'
        )

    return redirect(
        'product_detail',
        product_id=product.id
    )


# =========================================
# ADD PRODUCT
# =========================================

@user_passes_test(is_admin, login_url='login')
def add_product(request):

    categories = Category.objects.all().order_by('name')

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        description = request.POST.get(
            'description',
            ''
        ).strip()

        category_id = request.POST.get(
            'category'
        )

        price = request.POST.get(
            'price'
        ) or 0

        stock = request.POST.get(
            'stock'
        ) or 0

        is_featured = (
            request.POST.get('is_featured') == 'on'
        )

        image = request.FILES.get('image')

        Product.objects.create(
            name=name,
            description=description,
            category_id=category_id,
            price=price,
            stock=stock,
            is_featured=is_featured,
            image=image
        )

        return redirect(
            'admin_products'
        )

    return render(
        request,
        'adminpanel/add_product.html',
        {
            'categories': categories,
        }
    )


# =========================================
# ADMIN WISHLIST
# =========================================

@user_passes_test(is_admin, login_url='login')
def admin_wishlist(request):

    wishlist_items = Wishlist.objects.select_related(
        'user',
        'product'
    ).order_by('-id')

    return render(
        request,
        'adminpanel/wishlist.html',
        {
            'wishlist_items': wishlist_items,
        }
    )

# =========================================
# ADMIN CATEGORIES
# =========================================

@user_passes_test(is_admin, login_url='login')
def admin_categories(request):

    categories = Category.objects.all().order_by('name')

    return render(
        request,
        'adminpanel/categories.html',
        {
            'categories': categories,
        }
    )

@user_passes_test(is_admin, login_url='login')
def add_category(request):

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        if name:

            if Category.objects.filter(
                name__iexact=name
            ).exists():

                return render(
                    request,
                    'adminpanel/add_category.html',
                    {
                        'error': 'This category already exists.'
                    }
                )

            Category.objects.create(
                name=name
            )

            return redirect(
                'admin_categories'
            )

    return render(
        request,
        'adminpanel/add_category.html'
    )

@user_passes_test(is_admin, login_url='login')
def edit_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':

        name = request.POST.get(
            'name',
            ''
        ).strip()

        if name:

            if Category.objects.filter(
                name__iexact=name
            ).exclude(
                id=category.id
            ).exists():

                return render(
                    request,
                    'adminpanel/edit_category.html',
                    {
                        'category': category,
                        'error': 'This category already exists.'
                    }
                )

            category.name = name
            category.save()

            return redirect(
                'admin_categories'
            )

    return render(
        request,
        'adminpanel/edit_category.html',
        {
            'category': category,
        }
    )

@user_passes_test(is_admin, login_url='login')
def delete_category(request, category_id):

    category = get_object_or_404(
        Category,
        id=category_id
    )

    if request.method == 'POST':

        # Check if products are connected
        product_count = Product.objects.filter(
            category=category
        ).count()

        # Do not delete category if products exist
        if product_count > 0:

            return render(
                request,
                'adminpanel/categories.html',
                {
                    'categories': Category.objects.all(),
                    'error': (
                        f'Cannot delete "{category.name}". '
                        f'{product_count} product(s) are connected '
                        'to this category.'
                    )
                }
            )

        # Delete only when no products are connected
        category.delete()

    return redirect(
        'admin_categories'
    )

@user_passes_test(is_admin, login_url='login')
def admin_orders(request):

    # =========================================
    # SEARCH
    # =========================================

    search = request.GET.get(
        'search',
        ''
    ).strip()


    # =========================================
    # STATUS FILTER
    # =========================================

    status = request.GET.get(
        'status',
        ''
    ).strip()


    # =========================================
    # ALL ORDERS
    # =========================================

    orders = Order.objects.select_related(
        'user'
    ).all().order_by(
        '-created_at'
    )


    # =========================================
    # SEARCH FILTER
    # =========================================

    if search:

        from django.db.models import Q

        orders = orders.filter(

            Q(id__icontains=search) |

            Q(full_name__icontains=search) |

            Q(email__icontains=search) |

            Q(user__username__icontains=search) |

            Q(user__email__icontains=search)

        )


    # =========================================
    # STATUS FILTER
    # =========================================

    if status:

        valid_statuses = [
            'pending',
            'processing',
            'shipped',
            'Delivered',
            'cancelled',
        ]

        if status in valid_statuses:

            orders = orders.filter(
                status=status
            )


    # =========================================
    # CONTEXT
    # =========================================

    context = {

        'orders': orders,

        'search': search,

        'status': status,

    }


    return render(
        request,
        'adminpanel/orders.html',
        context
    )

@user_passes_test(is_admin, login_url='login')
def update_order_status(request, order_id):  

    order = get_object_or_404(
        Order,
        id=order_id
    )

    if request.method == 'POST':

        new_status = request.POST.get('status')

        valid_statuses = [
            'pending',
            'processing',
            'shipped',
            'Delivered',
            'cancelled',
        ]

        if new_status in valid_statuses:

            order.status = new_status
            order.save()

    return redirect('admin_orders')

# =========================================
# ADMIN CUSTOMERS
# =========================================

@user_passes_test(is_admin, login_url='login')
def admin_customers(request):

    search = request.GET.get(
        'search',
        ''
    ).strip()

    customers = User.objects.filter(
        is_staff=False
    ).order_by(
        '-date_joined'
    )

    # ==============================
    # CUSTOMER SEARCH
    # ==============================

    if search:

        customers = customers.filter(

            Q(username__icontains=search) |

            Q(first_name__icontains=search) |

            Q(last_name__icontains=search) |

            Q(email__icontains=search)

        )

    return render(
        request,
        'adminpanel/customers.html',
        {
            'customers': customers,
            'search': search,
        }
    )

# =========================================
# ADMIN REVENUE / REPORTS
# =========================================

@user_passes_test(is_admin, login_url='login')
def admin_reports(request):

    total_revenue = Order.objects.filter(
        status__in=[
            'processing',
            'shipped',
            'Delivered'
        ]
    ).aggregate(
        total=Sum('total_amount')
    )['total'] or 0

    total_orders = Order.objects.filter(
        status__in=[
            'processing',
            'shipped',
            'Delivered'
        ]
    ).count()

    return render(
        request,
        'adminpanel/reports.html',
        {
            'total_revenue': total_revenue,
            'total_orders': total_orders,
        }
    )


# =========================================
# ADMIN PROFILE / SETTINGS
# =========================================
@user_passes_test(is_admin, login_url='login')
def admin_profile_settings(request):

    user = request.user

    if request.method == 'POST':

        first_name = request.POST.get(
            'first_name',
            ''
        ).strip()

        last_name = request.POST.get(
            'last_name',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        if not email:
            messages.error(
                request,
                'Email cannot be empty.'
            )

            return redirect(
                'admin_profile_settings'
            )

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        messages.success(
            request,
            'Admin profile updated successfully.'
        )

        return redirect(
            'admin_profile_settings'
        )

    return render(
        request,
        'adminpanel/admin_profile_settings.html',
        {
            'admin_user': user,
        }
    )


# =========================================
# STORE INFORMATION SETTINGS
# =========================================

@user_passes_test(is_admin, login_url='login')
def store_settings(request):

    store, created = StoreSettings.objects.get_or_create(
        id=1
    )

    if request.method == 'POST':

        store.store_name = request.POST.get(
            'store_name',
            ''
        ).strip()

        store.store_email = request.POST.get(
            'store_email',
            ''
        ).strip()

        store.phone = request.POST.get(
            'phone',
            ''
        ).strip()

        store.address = request.POST.get(
            'address',
            ''
        ).strip()

        store.city = request.POST.get(
            'city',
            ''
        ).strip()

        store.state = request.POST.get(
            'state',
            ''
        ).strip()

        store.pincode = request.POST.get(
            'pincode',
            ''
        ).strip()

        store.save()

        messages.success(
            request,
            'Store information updated successfully.'
        )

        return redirect(
            'store_settings'
        )

    return render(
        request,
        'adminpanel/store_settings.html',
        {
            'store': store,
        }
    )

# =========================================
# ADMIN SECURITY SETTINGS
# =========================================

@user_passes_test(is_admin, login_url='login')
def admin_security_settings(request):
    return render(
        request,
        'adminpanel/security_settings.html',
        {
            'admin_user': request.user
        }
    )


# =========================================
# ADMIN NOTIFICATION SETTINGS
# =========================================

@user_passes_test(is_admin, login_url='login')
def admin_notification_settings(request):

    notification, created = NotificationSettings.objects.get_or_create(
        id=1
    )

    if request.method == 'POST':

        notification.new_order = 'new_order' in request.POST
        notification.new_customer = 'new_customer' in request.POST
        notification.low_stock = 'low_stock' in request.POST
        notification.payment_notification = (
            'payment_notification' in request.POST
        )
        notification.email_notifications = (
            'email_notifications' in request.POST
        )
        notification.dashboard_alerts = (
            'dashboard_alerts' in request.POST
        )

        notification.save()

        messages.success(
            request,
            'Notification settings updated successfully.'
        )

        return redirect('admin_notification_settings')

    return render(
        request,
        'adminpanel/notification_settings.html',
        {
            'notification': notification
        }
    )


# =========================================
# ADMIN PAYMENT SETTINGS
# =========================================


@user_passes_test(is_admin, login_url='login')
def admin_payment_settings(request):

    payment, created = PaymentSettings.objects.get_or_create(
        id=1
    )

    if request.method == 'POST':

        payment.payment_enabled = (
            'payment_enabled' in request.POST
        )

        payment.payment_mode = request.POST.get(
            'payment_mode',
            'test'
        )

        payment.currency = request.POST.get(
            'currency',
            'INR'
        )

        payment.stripe_enabled = (
            'stripe_enabled' in request.POST
        )

        payment.cod_enabled = (
            'cod_enabled' in request.POST
        )

        payment.save()

        messages.success(
            request,
            'Payment settings updated successfully.'
        )

        return redirect('admin_payment_settings')

    return render(
        request,
        'adminpanel/payment_settings.html',
        {
            'payment': payment
        }
    )



# =========================================
# ADMIN WEBSITE SETTINGS
# =========================================


@user_passes_test(is_admin, login_url='login')
def admin_website_settings(request):

    website, created = WebsiteSettings.objects.get_or_create(
        id=1
    )

    if request.method == 'POST':

        website.website_name = request.POST.get(
            'website_name',
            ''
        ).strip()

        website.description = request.POST.get(
            'description',
            ''
        ).strip()

        website.contact_email = request.POST.get(
            'contact_email',
            ''
        ).strip()

        website.contact_phone = request.POST.get(
            'contact_phone',
            ''
        ).strip()

        website.address = request.POST.get(
            'address',
            ''
        ).strip()

        website.website_active = (
            'website_active' in request.POST
        )

        website.customer_registration = (
            'customer_registration' in request.POST
        )

        website.orders_enabled = (
            'orders_enabled' in request.POST
        )

        website.save()

        messages.success(
            request,
            'Website settings updated successfully.'
        )

        return redirect('admin_website_settings')

    return render(
        request,
        'adminpanel/website_settings.html',
        {
            'website': website
        }
    )

