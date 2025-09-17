from twilio.rest import Client
from django.http import JsonResponse

# Your Twilio credentials
account_sid = 'your_account_sid'
auth_token = 'your_auth_token'
twilio_phone_number = 'your_twilio_number'

client = Client(account_sid, auth_token)

def send_sms(request, ngo_contact, user_contact, message_type):
    """
    Sends an SMS based on message_type (volunteer/donate) to the NGO.
    """
    if message_type == 'volunteer':
        message = f"Hello, I'm interested in volunteering. Contact me at {user_contact}."
    elif message_type == 'donate':
        message = f"Hello, I want to donate resources (not money). Contact me at {user_contact}."
    else:
        return JsonResponse({"error": "Invalid message type"}, status=400)

    try:
        # Send the SMS
        response = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=ngo_contact
        )

        return JsonResponse({"status": "Message sent successfully", "sid": response.sid})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
