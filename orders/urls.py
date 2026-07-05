from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_view, name="cart"),
    #path('checkout/', views.checkout_view, name="checkout"),
    path('checkout/', views.checkout, name="checkout"),

    # NEW ASYNC TRANSACTION PATHWAY ENDPOINT
    path('update_item/', views.update_item_view, name="update_item"),

        
    path('success/', views.payment_success_view, name="payment_success"),

    # Add this to orders/urls.py urlpatterns list:
    path('dashboard/', views.orders_dashboard_view, name='orders_dashboard'),

    #path('api/cart-count/', views.get_cart_count_api, name='cart_count_api'),    
]
