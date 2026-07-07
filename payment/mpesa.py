import requests
import base64
from datetime import datetime
from django.conf import settings


def get_mpesa_access_token():
    """Get OAuth token from Safaricom."""
    if settings.MPESA_ENV == 'sandbox':
        url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    else:
        url = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    response = requests.get(
        url,
        auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
    )
    return response.json().get('access_token')


def generate_password():
    """Generate the M-Pesa password (base64 of shortcode+passkey+timestamp)."""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    raw = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(raw.encode()).decode()
    return password, timestamp

# Temporarily add this at the top of stk_push() to verify
print(f"DEBUG → PASSKEY length: {len(settings.MPESA_PASSKEY)}")
print(f"DEBUG → PASSKEY starts with: {settings.MPESA_PASSKEY[:10]}")

def stk_push(phone_number, amount, order_id):
    """
    Send STK Push request to Safaricom.
    phone_number: format 254712345678
    amount: integer KES amount
    order_id: your order reference
    """
    access_token = get_mpesa_access_token()
    password, timestamp = generate_password()

    if settings.MPESA_ENV == 'sandbox':
        url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    else:
        url = 'https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest'

    headers = {'Authorization': f'Bearer {access_token}'}

    payload = {
        'BusinessShortCode': settings.MPESA_SHORTCODE,
        'Password':          password,
        'Timestamp':         timestamp,
        'TransactionType':   'CustomerPayBillOnline',
        'Amount':            int(amount),
        'PartyA':            phone_number,
        'PartyB':            settings.MPESA_SHORTCODE,
        'PhoneNumber':       phone_number,
        'CallBackURL':       settings.MPESA_CALLBACK_URL,
        'AccountReference':  f'SokoDirect-Order-{order_id}',
        'TransactionDesc':   f'SokoDirect Payment for Order {order_id}',
    }

    # Debug — print the full payload before sending
    print(f"DEBUG → STK Push payload: {payload}")

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

    # Debug — print the full Safaricom response
    print(f"DEBUG → Safaricom raw response: {result}")

    return result