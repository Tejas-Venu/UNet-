from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from requests import Response
from rest_framework.decorators import api_view
import json
from ngos.models import NGO
from donations.models import Donation
from users.models import User

import requests

import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from django.conf import settings

@csrf_exempt
@api_view(['POST'])
def initiate_payment(request):

    print("Received a request")
    print("Handling POST request")
    body = json.loads(request.body)
    card_number = body.get('card_number')
    cvv = body.get('cvv')
    amount = body.get('amount')
    expiry_date = body.get('expiry_date')
    name = body.get('name')
    ngo_id = body.get('ngo_id')
    user_email = body.get('user_email')

    print(ngo_id)
    print(user_email)

    processor_response = {}

    try:

        ngos = NGO.objects.filter(id=ngo_id)
        for ngo in ngos:
            account_number = ngo.account_number
        print(account_number)
        
        if card_number and cvv and amount and expiry_date and name and account_number:
            # Send the payment data to the mock payment processor
            
            try:
                processor_response = requests.post(
                    "http://localhost:5000/api/processor/initiate-payment/",
                    json={
                        'card_number': card_number,
                        'cvv': cvv,
                        'amount': amount,
                        'name' : name,
                        'expiry_date': expiry_date,
                        'ngo_account_number' : account_number
                    },
                    timeout=10  # Set a timeout for the request
                )

                # Log the response from the payment processor
                print(f"Payment Processor Response: {processor_response.json()}")

                if processor_response.status_code == 200:
                    # record the donation
                    user = User.objects.filter(email = user_email).first()
                    ngo = NGO.objects.filter(id = ngo_id).first()
                    Donation(ngo_id = ngo, user_id = user, amount = amount).save()

                    return JsonResponse(
                        {
                            'message': 'Payment successful!',
                            'details': processor_response.json()
                        },
                        status=200
                    )
                else:
                    return JsonResponse(
                        {
                            'message': 'Payment failed!',
                            'details': processor_response.json()
                        },
                        status=processor_response.status_code
                    )

            except requests.RequestException as e:
                print(f"Error communicating with the payment processor: {e}")
                return JsonResponse({'message': 'Payment processor error', 'error': str(e)}, status=500)

        else:
            return JsonResponse({'message': 'Invalid payment details'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'message': 'Invalid JSON format'}, status=400)
    

def load_public_key():
    # Read publickeys.json
    with open('publickeys.json', 'r') as f:
        keys_data = json.load(f)
    
    # Choose the public key (keypair_1, keypair_2, etc.)
    public_key_str = keys_data.get("payment processor")
    
    # Load the public key into an object
    public_key = serialization.load_pem_public_key(public_key_str.encode('utf-8'))

    print(public_key)
    return public_key


def encrypt_message(message, public_key):
    # Encrypt the message using RSA and the public key
    encrypted = public_key.encrypt(
        message.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    print(encrypted)
    return encrypted
