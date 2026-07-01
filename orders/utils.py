
import json
import uuid  
from products.models import Product
from .models import Order, OrderItem

def cookieCart(request):
    try:
        cart = json.loads(request.COOKIES.get('cart', '{}'))
    except Exception:
        cart = {}

    print('Processing Cookie Cart Matrix State:', cart)
    items = []
    order = {'get_cart_total': 0, 'get_cart_items': 0}
    cartItems = order['get_cart_items']

    for i in cart:
        try:
            # --- DEFENSIVE CHECK: If your database expects UUIDs, drop plain integer strings safely ---
            try:
                uuid.UUID(str(i))
            except ValueError:
                print(f"Skipping malformed or legacy cart key index value: {i}")
                continue # Skip directly to the next item instead of crashing the view

            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product': {
                    'id': product.id,
                    'title': product.title,
                    'price': product.price,
                    'imageURL': product.imageURL if hasattr(product, 'imageURL') else (product.image.url if product.image else ''),
                },
                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            items.append(item)
            
        except Product.DoesNotExist:
            # Silently safeguard if a background database entity was wiped out
            pass

    return {'cartItems': cartItems, 'order': order, 'items': items}

def cartData(request):
    """
    Unified entry matrix deciding whether to fetch transaction states
    from the real Database (Authenticated) or Browser Cookies (Guests).
    """
    if request.user.is_authenticated:
        customer = request.user
        #order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        # Change get_or_create to filter
        order = Order.objects.filter(customer=customer, complete=False).first()
        # Now, 'order' will be None if one doesn't exist, instead of creating a new one.
        if order:
            items = order.orderitem_set.all()
            # Ensure your template layout blocks or header variables pull order.get_cart_items safely
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total': 0, 'get_cart_items': 0}
            cartItems = 0
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']

    return {'cartItems': cartItems, 'order': order, 'items': items}
