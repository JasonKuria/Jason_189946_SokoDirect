from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import JsonResponse, HttpResponse
import json
import datetime  
import csv
from .models import Order, OrderItem, ShippingAddress
from products.models import Product
from orders.utils import cartData 
from django.contrib.auth.decorators import login_required

from django.db.models import Sum, Count, Q
from django.utils import timezone

def cart_view(request):
    data = cartData(request)
    #cart_items_count = data['cartItems']

    context = {
        'items': data['items'], 
        'order': data['order'],
        #'cartItems': cart_items_count #       
    }
    return render(request, 'orders/cart.html', context)


@login_required(login_url='login')  
def checkout_view(request):
    data = cartData(request)

    # If no active order exists, nothing to check out — send back to cart
    if not data['items']:
        return redirect('cart')

    order = data['order']
    
    # 1. Handle Form Submission
    if request.method == 'POST':
        # Update order status
        order.complete = True
        order.transaction_id = str(datetime.datetime.now().timestamp())
        order.save()

        # Save the shipping details
        ShippingAddress.objects.create(
            customer=request.user,
            order=order,
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            county=request.POST.get('county'),
            phone_number=request.POST.get('phone')
        )
        
        # Redirect to a success page
        return redirect('payment_success')

    # 2. Handle GET request (Displaying the page)
    latest_address = ShippingAddress.objects.filter(customer=request.user).order_by('-date_added').first()

    context = {
        'items': data['items'], 
        'order': order,
        'shipping_address': latest_address,
    }
    return render(request, 'orders/checkout.html', context)





@login_required
def checkout(request):
    # Get or create the current open order for this user
    order, created = Order.objects.get_or_create(
        customer=request.user,
        complete=False
    )
    items = order.orderitem_set.all()

    # Get existing shipping address if any
    shipping_address = ShippingAddress.objects.filter(
        customer=request.user,
        order=order
    ).first()

    if request.method == 'POST':
        # Collect form data
        address  = request.POST.get('address', '').strip()
        city     = request.POST.get('city', '').strip()
        county   = request.POST.get('county', '').strip()
        phone    = request.POST.get('phone', '').strip()

        # Validate — make sure nothing is empty
        if not all([address, city, county, phone]):
            messages.error(request, 'Please fill in all delivery details.')
            return render(request, 'orders/checkout.html', {
                'order': order,
                'items': items,
                'shipping_address': shipping_address,
            })

        # Save or update the shipping address
        ShippingAddress.objects.update_or_create(
            customer=request.user,
            order=order,
            defaults={
                'address':      address,
                'city':         city,
                'county':       county,
                'phone_number': phone,
            }
        )

        # ✅ Redirect to the payment page passing the order id
        return redirect('payment-page', order_id=order.id)

    # GET request — just show the checkout page
    context = {
        'order':            order,
        'items':            items,
        'shipping_address': shipping_address,
    }
    return render(request, 'orders/checkout.html', context)

def payment_success_view(request):
    return render(request, 'orders/success.html')


def update_item_view(request):

    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    data = json.loads(request.body)

    product_id = data.get('productId')
    action = data.get('action')

    # Guest users
    if not request.user.is_authenticated:
        return JsonResponse({'status': 'Guest handled'}, safe=False)

    customer = request.user
    product = get_object_or_404(Product, id=product_id)

    order, created = Order.objects.get_or_create(
        customer=customer,
        complete=False
    )

    order_item, created = OrderItem.objects.get_or_create(
        order=order,
        product=product
    )

    if action == 'add':
        order_item.quantity += 1

    elif action == 'remove':
        order_item.quantity -= 1

    elif action == 'delete_item':
        order_item.quantity = 0

    if order_item.quantity <= 0:
        order_item.delete()
        current_quantity = 0
    else:
        order_item.save()
        current_quantity = order_item.quantity

    return JsonResponse({
        'cartItems': order.get_cart_items,
        'item_quantity': current_quantity,
    })






@login_required(login_url='login')  
def orders_dashboard_view(request):

    status_filter = request.GET.get('status', 'all')
    search_query  = request.GET.get('search', '').strip()
    export        = request.GET.get('export', '')

    orders = Order.objects.select_related('customer').prefetch_related(
        'orderitem_set__product', 'shippingaddress_set'
    ).order_by('-date_ordered')

    if status_filter == 'pending':
        orders = orders.filter(complete=False)
    elif status_filter == 'complete':
        orders = orders.filter(complete=True)

    if search_query:
        orders = orders.filter(
            Q(customer__username__icontains=search_query) |
            Q(customer__first_name__icontains=search_query) |
            Q(customer__last_name__icontains=search_query)  |
            Q(transaction_id__icontains=search_query)
        )

    # ── CSV Export ──────────────────────────────────────────────────────────
    if export == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sokodirect_orders.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Order ID', 'Customer', 'Username', 'Email',
            'Items', 'Total (KES)', 'County', 'City', 'Address',
            'Phone', 'Status', 'Transaction ID', 'Date'
        ])

        for order in orders:
            shipping = order.shippingaddress_set.first()
            writer.writerow([
                order.id,
                order.customer.get_full_name() or order.customer.username,
                order.customer.username,
                order.customer.email,
                order.get_cart_items,
                order.get_cart_total,
                shipping.county       if shipping else '',
                shipping.city         if shipping else '',
                shipping.address      if shipping else '',
                shipping.phone_number if shipping else '',
                'Complete' if order.complete else 'Pending',
                order.transaction_id or '',
                order.date_ordered.strftime('%d/%m/%Y %H:%M'),
            ])

        return response
    # ────────────────────────────────────────────────────────────────────────

    all_orders     = Order.objects.all()
    total_orders   = all_orders.count()
    complete_count = all_orders.filter(complete=True).count()
    pending_count  = all_orders.filter(complete=False).count()
    total_revenue  = sum(o.get_cart_total for o in all_orders.filter(complete=True))
    today          = timezone.now().date()
    today_count    = all_orders.filter(date_ordered__date=today).count()

    context = {
        'orders':         orders,
        'status_filter':  status_filter,
        'search_query':   search_query,
        'total_orders':   total_orders,
        'complete_count': complete_count,
        'pending_count':  pending_count,
        'total_revenue':  total_revenue,
        'today_count':    today_count,
    }
    return render(request, 'orders/orders_dashboard.html', context)
    #return render(request, 'orders/orders_dashboard_v2.html', context)
