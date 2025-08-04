import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime
import base64
import os
from dotenv import load_dotenv

load_dotenv()

def lipa_na_mpesa(phone, amount):
    consumer_key = os.getenv("MPESA_CONSUMER_KEY")
    consumer_secret = os.getenv("MPESA_CONSUMER_SECRET")
    shortcode = os.getenv("MPESA_SHORTCODE")
    passkey = os.getenv("MPESA_PASSKEY")

    auth_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    res = requests.get(auth_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = res.json()['access_token']

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode((shortcode + passkey + timestamp).encode()).decode()

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    payload = {
        "BusinessShortCode": shortcode,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": shortcode,
        "PhoneNumber": phone,
        "CallBackURL": "https://yourdomain.com/api/mpesa/callback", 
        "AccountReference": "BeautyShop",
        "TransactionDesc": "Order payment"
    }

    stk_url = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    response = requests.post(stk_url, json=payload, headers=headers)
    return response.json()
