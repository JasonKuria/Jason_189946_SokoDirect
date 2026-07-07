import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .mpesa import stk_push
from .models import Payment
#from products.models import Order
from orders.models import Order        

from django.utils import timezone

from django.core.mail import send_mail
from django.conf import settings



import csv
from django.http import HttpResponse
from django.db.models import Sum, Count, Avg, Q
from django.contrib.admin.views.decorators import staff_member_required
from datetime import timedelta



@login_required
def payment_page(request, order_id):
    """Show the payment page — payment/add page."""
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
    """Waiting page — payment/validate page."""
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

    print("========== CALLBACK RECEIVED ==========")

    if request.method == 'POST':

        data = json.loads(request.body)
        print(json.dumps(data, indent=4))
        
        result = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = result.get('CheckoutRequestID')
        result_code = result.get('ResultCode')

        try:
            payment = Payment.objects.get(checkout_request_id=checkout_request_id)
            order = payment.order

            if result_code == 0:

                # Extract the Mpesa receipt and Save it into order model
                # ------------------------------------------------------ 
                # -- Extract Metadata --
                metadata = result.get('CallbackMetadata', {}).get('Item', [])
                receipt = next((i['Value'] for i in metadata if i['Name'] == 'MpesaReceiptNumber'), None)
                payment_time = timezone.now()

                # -- Update Payment Model --
                payment.mpesa_receipt = receipt
                payment.paid_at = payment_time
                payment.status = 'success'
                payment.save()

                # -- Update Order Model --
                if order:
                    order.mpesa_receipt = receipt
                    order.paid_at = payment_time
                    order.complete = True
                    order.save()                
                # ------------------------------------------------------ 

                # -== SEND EMAIL TO THE BUYER TO CONFIRM THE PURCHASE Add this Email Logic ==-

                # Create the HTML message
                html_content = f"""
                <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #e2e8f0; border-radius: 10px; padding: 20px;">
                    <h2 style="color: #0e6e36;">Payment Successful!</h2>
                    <p>Hello {order.customer.first_name},</p>
                    <p>Thank you for shopping with <strong>SokoDirect</strong>! Your order <strong>#{order.id}</strong> has been confirmed and is now being processed.</p>
                    
                    <div style="background: #f0faf4; padding: 15px; border-radius: 5px; border: 1px solid #a8d5b5;">
                        <p style="margin: 5px 0;"><strong>M-Pesa Receipt:</strong> {receipt}</p>
                        <p style="margin: 5px 0;"><strong>Amount Paid:</strong> {payment.amount}</p>
                        <p style="margin: 5px 0;"><strong>Payment Date:</strong> {payment_time.strftime('%d %b %Y, %H:%M')}</p>
                         <p style="margin: 5px 0;">---------------------------------------</p>
                    </div>
                    
                    <p>The farmer has been notified and your produce will be delivered shortly.</p>
                    <p>Thank you for choosing SokoDirect..</p>
                    <p>Best regards,<br><strong>The SokoDirect Team</strong></p>
                </div>
                """      
                buyer_email = order.customer.profile.email          
                send_mail(
                        subject=f"[SokoDirect] Payment Confirmation - Order #{order.id}",
                        message=f"Hello {order.customer.first_name}, your order #{order.id} is confirmed.", # Fallback text
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        #recipient_list=[order.customer.email],
                        recipient_list=[buyer_email],

                        html_message=html_content, # This sends the nice HTML
                        fail_silently=True,
                    )               
                # -===========================================================================-


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
    # This view renders the page after a successful transaction

    # Retrieve the payment ID from the session
    payment_id = request.session.get('payment_id')

    # Get the payment object; if it doesn't exist or isn't successful, it will 404
    payment = get_object_or_404(Payment, id=payment_id, status='success')

    #payment = get_object_or_404(Payment, id=payment_id, status='success')
    #return render(request, 'payment/order_success.html', {'payment': payment})    
    return render(request, 'payment/order_success.html', {'payment': payment})











@login_required(login_url='login')
@staff_member_required(login_url='login')
def payment_report(request):
    """
    SokoDirect Payment Reports Dashboard.
    Accessible only to staff users.
    Matches your Payment model fields exactly:
      user, order, phone_number, amount, mpesa_receipt,
      paid_at, status, created, updated
    """

    # ── CSV Export ─────────────────────────────────────────────
    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sokodirect_payments.csv"'
        writer = csv.writer(response)
        writer.writerow([
            '#', 'Buyer Name', 'Username', 'Email',
            'Phone Number', 'Amount (KES)', 'M-Pesa Receipt',
            'Order ID', 'Status', 'Paid At', 'Created'
        ])
        for i, p in enumerate(Payment.objects.select_related('user', 'order').order_by('-created'), 1):
            writer.writerow([
                i,
                p.user.get_full_name() if p.user else '—',
                p.user.username if p.user else '—',
                p.user.email if p.user else '—',
                p.phone_number,
                p.amount,
                p.mpesa_receipt or '—',
                str(p.order.id)[:8] if p.order else '—',
                p.status,
                p.paid_at.strftime('%d %b %Y %H:%M') if p.paid_at else '—',
                p.created.strftime('%d %b %Y %H:%M'),
            ])
        return response

    # ── All Payments Queryset ──────────────────────────────────
    search_query = request.GET.get('search', '').strip()
    status_filter = request.GET.get('status', 'all')

    payments = Payment.objects.select_related('user', 'order').order_by('-created')

    if status_filter != 'all':
        payments = payments.filter(status=status_filter)

    if search_query:
        payments = payments.filter(
            Q(phone_number__icontains=search_query) |
            Q(mpesa_receipt__icontains=search_query) |
            Q(user__username__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    # ── KPI Aggregates ─────────────────────────────────────────
    all_payments    = Payment.objects.all()
    total_payments  = all_payments.count()
    success_count   = all_payments.filter(status='success').count()
    pending_count   = all_payments.filter(status='pending').count()
    failed_count    = all_payments.filter(status='failed').count()
    cancelled_count = all_payments.filter(status='cancelled').count()

    total_revenue = all_payments.filter(status='success').aggregate(
        t=Sum('amount'))['t'] or 0
    avg_amount = all_payments.filter(status='success').aggregate(
        a=Avg('amount'))['a'] or 0
    success_rate = round(success_count / total_payments * 100, 1) if total_payments > 0 else 0

    # ── Today's stats ──────────────────────────────────────────
    today = timezone.now().date()
    today_payments = all_payments.filter(created__date=today)
    today_count    = today_payments.count()
    today_revenue  = today_payments.filter(status='success').aggregate(
        t=Sum('amount'))['t'] or 0

    # ── Top Buyers by Spend ────────────────────────────────────
    top_buyers_qs = (
        all_payments.filter(status='success')
        .values('user__first_name', 'user__last_name', 'user__username')
        .annotate(total=Sum('amount'), count=Count('id'))
        .order_by('-total')[:5]
    )
    max_spend = max((b['total'] for b in top_buyers_qs), default=1) or 1
    top_buyers = [
        {
            'name': (
                f"{b['user__first_name']} {b['user__last_name']}".strip()
                or b['user__username'] or 'Unknown'
            ),
            'total': b['total'],
            'count': b['count'],
            'pct': round(float(b['total']) / float(max_spend) * 100),
        }
        for b in top_buyers_qs
    ]

    # ── Daily Revenue — Last 7 Days ────────────────────────────
    daily_revenue = []
    day_totals = []
    for i in range(6, -1, -1):
        day = today - timedelta(days=i)
        total = all_payments.filter(
            status='success', created__date=day
        ).aggregate(t=Sum('amount'))['t'] or 0
        day_totals.append({'label': day.strftime('%a'), 'total': float(total)})

    max_day = max((d['total'] for d in day_totals), default=1) or 1
    for d in day_totals:
        daily_revenue.append({
            'label': d['label'],
            'total': d['total'],
            'pct': max(round(d['total'] / max_day * 100), 5),
        })

    # ── Donut percentages ──────────────────────────────────────
    if total_payments > 0:
        success_deg = round(success_count / total_payments * 360)
        pending_deg = round(pending_count / total_payments * 360)
        failed_deg  = round((failed_count + cancelled_count) / total_payments * 360)
    else:
        success_deg = pending_deg = failed_deg = 0

    context = {
        # Payments list (filtered)
        'payments':       payments,
        'search_query':   search_query,
        'status_filter':  status_filter,
        # KPIs
        'total_payments':  total_payments,
        'success_count':   success_count,
        'pending_count':   pending_count,
        'failed_count':    failed_count,
        'cancelled_count': cancelled_count,
        'total_revenue':   total_revenue,
        'avg_amount':      avg_amount,
        'success_rate':    success_rate,
        # Today
        'today_count':   today_count,
        'today_revenue': today_revenue,
        # Charts
        'top_buyers':     top_buyers,
        'daily_revenue':  daily_revenue,
        'success_deg':    success_deg,
        'pending_deg':    pending_deg,
        'failed_deg':     failed_deg,
        # Meta
        'now': timezone.now(),
    }
    return render(request, 'payment/payment_report.html', context)
