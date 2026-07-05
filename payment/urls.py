from django.urls import path
from . import views

urlpatterns = [
    path('payment/<int:order_id>/',      views.payment_page,         name='payment-page'),
    path('pay/<int:order_id>/',          views.initiate_payment,     name='initiate-payment'),
    path('payment/validate/',            views.payment_validate,     name='payment-validate'),
    path('payment/status/',              views.check_payment_status, name='payment-status'),
    path('payment/callback/',            views.mpesa_callback,       name='mpesa-callback'),
    path('order/success/',               views.order_success,        name='order-success'),
    

]
