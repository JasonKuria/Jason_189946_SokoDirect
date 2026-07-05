import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .mpesa import stk_push
from .models import Payment
#from products.models import Order
from orders.models import Order        

@login_required
def payment_page(request, order_id):
    """Show the payment page — like Jumia's payment/add page."""
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    error = request.session.pop('payment_error', None)
    context = {
        'order': order,
        'error': error,
    }
    return render(request, 'payment/payment_page.html', context)

@login_required
def initiate_payment(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, customer=request.user)
        phone  = request.POST.get('phone_number', '').strip()
        amount = order.get_cart_total

        # ── Clean the phone number — handle all formats ──
        # Remove spaces, dashes, brackets, plus sign
        phone = phone.replace(' ', '').replace('-', '').replace('+', '').replace('(', '').replace(')', '')

        # Convert to 254 format
        if phone.startswith('0'):
            phone = '254' + phone[1:]       # 0712345678 → 254712345678
        elif phone.startswith('254'):
            phone = phone                   # 254712345678 → 254712345678 (already correct)
        elif phone.startswith('7') or phone.startswith('1'):
            phone = '254' + phone           # 712345678 → 254712345678

        # Add debug print so you can see what's being sent
        print(f"DEBUG → Phone sent to Safaricom: {phone}")
        print(f"DEBUG → Amount: {amount}")
        print(f"DEBUG → Order ID: {order.id}")

        response = stk_push(phone, amount, order.id)

        # Add debug print to see full Safaricom response
        print(f"DEBUG → Safaricom response: {response}")

        if response.get('ResponseCode') == '0':
            payment = Payment.objects.create(
                user=request.user,
                order=order,
                phone_number=phone,
                amount=amount,
                merchant_request_id=response.get('MerchantRequestID', ''),
                checkout_request_id=response.get('CheckoutRequestID', ''),
                status='pending',
            )
            request.session['payment_id'] = payment.id
            return redirect('payment-validate')
        else:
            request.session['payment_error'] = (
                'Sorry, we are unable to complete your transaction. '
                'Please try again or choose a different payment method.'
            )
            return redirect('payment-page', order_id=order_id)

    return redirect('payment-page', order_id=order_id)

@login_required
def payment_validate(request):
    """Waiting page — like Jumia's payment/validate page."""
    payment_id = request.session.get('payment_id')
    payment = get_object_or_404(Payment, id=payment_id)
    return render(request, 'payment/payment_validate.html', {'payment': payment})

@login_required
def check_payment_status(request):
    """AJAX endpoint — frontend polls this every 3 seconds."""
    payment_id = request.session.get('payment_id')
    if not payment_id:
        return JsonResponse({'status': 'not_found'})
    payment = Payment.objects.get(id=payment_id)
    return JsonResponse({'status': payment.status})

@csrf_exempt
def mpesa_callback(request):
    """
    Safaricom calls this URL after the user enters their PIN.
    We update the Payment record accordingly.
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        result = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = result.get('CheckoutRequestID')
        result_code = result.get('ResultCode')

        try:
            payment = Payment.objects.get(checkout_request_id=checkout_request_id)
            if result_code == 0:
                # Payment successful
                items = result.get('CallbackMetadata', {}).get('Item', [])
                for item in items:
                    if item['Name'] == 'MpesaReceiptNumber':
                        payment.mpesa_receipt = item['Value']
                payment.status = 'success'
                # Mark the order as complete
                payment.order.complete = True
                payment.order.save()
            else:
                payment.status = 'failed'
            payment.save()
        except Payment.DoesNotExist:
            pass

    return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})



@login_required
def order_success(request):
    payment_id = request.session.get('payment_id')
    payment = get_object_or_404(Payment, id=payment_id, status='success')
    return render(request, 'payment/order_success.html', {'payment': payment})

