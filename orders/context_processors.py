from .utils import cartData


def cart_counter(request):
    data = cartData(request)

    return {
        'cartItems': data['cartItems']
    }