import hashlib
from urllib.parse import urlencode
from django.conf import settings

def generate_payeer_url(merchant_id, secret_key, amount, order_id, currency, description):
    # Base URL for Payeer payment
    base_url = 'https://payeer.com/merchant/?'

    # Parameters for the payment request
    params = {
        'm_shop': merchant_id,
        'm_orderid': order_id,
        'm_amount': f'{amount:.2f}',
        'm_curr': currency,
        'm_desc': description,
        'm_key': secret_key,
    }

    # Generate the signature
    sign_str = ':'.join([
        params['m_shop'],
        str(params['m_orderid']),
        params['m_amount'],
        params['m_curr'],
        params['m_desc'],
        params['m_key']
    ])

    # Calculate SHA256 hash
    sign = hashlib.sha256(sign_str.encode()).hexdigest().upper()
    params['m_sign'] = sign

    # Remove secret key before encoding
    del params['m_key']

    # Return the full URL
    return base_url + urlencode(params)
