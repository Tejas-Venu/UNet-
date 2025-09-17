from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from ngos.models import NGO
from users.models import User
from .models import Donation
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from donations.models import Donation
from django.contrib.auth import get_user_model
import json

@csrf_exempt
def show_form(request):
    """Returns a JSON response containing donation form details or Razorpay integration."""
    if request.method == "GET":
        # Example structure for a donation form. Modify as per Razorpay integration or requirements.
        form_details = {
            "fields": {
                "user_id": "integer",
                "ngo_id": "integer",
                "amount": "decimal",
            },
            "payment_gateway": "Razorpay",
            "instructions": "Fill out the form and proceed to payment.",
        }
        return JsonResponse(form_details, status=200)
    return JsonResponse({"error": "Only GET requests are allowed"}, status=405)

@csrf_exempt
def list_user_donations(request):
    """Returns all donations made by the user identified by their email in the request."""
    if request.method == "POST":
        try:
            # Parse the request body
            body = json.loads(request.body)
            email = body.get("email")

            if not email:
                return JsonResponse({"error": "Email is required"}, status=400)
            print(email)
            # Fetch user based on the email
            User = get_user_model()
            user = User.objects.filter(email = email).first()
            print(user)  # Use `filter` with `.first()` to avoid exceptions
            if not user:
                return JsonResponse({"error": "User with this email does not exist"}, status=404)

            # Fetch donations for the user
            donations = Donation.objects.filter(user_id=user.id)
            print(donations)
            donation_list = [
                {
                    "id": donation.id,
                    "ngo_id": donation.ngo_id.id,
                    "ngo_name": NGO.objects.filter(id = donation.ngo_id.id).first().name,  # Assuming Donation has a ForeignKey to the NGO model
                    "date": donation.date.strftime("%B %Y"),  # Format the date for better readability
                    "amount": donation.amount,
                }
                for donation in donations
            ]

            print(donation_list)

            return JsonResponse({"donations": donation_list}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON in request body"}, status=400)

        except Exception as e:
            print('hello' + str(e))
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)



@login_required
def list_ngo_donations(request, ngo_id):
    """Returns all donations made to a particular NGO."""
    if request.method == "GET":
        try:
            ngo = NGO.objects.get(id=ngo_id)
            donations = Donation.objects.filter(ngo_id=ngo.id)
            donation_list = [
                {
                    "id": donation.id,
                    "user_id": donation.user_id,
                    "user_name": donation.user.name,
                    "date": donation.date,
                    "amount": donation.amount,
                }
                for donation in donations
            ]
            return JsonResponse(
                {"ngo_name": ngo.name, "donations": donation_list}, status=200
            )
        except NGO.DoesNotExist:
            return JsonResponse({"error": "NGO not found"}, status=404)
    return JsonResponse({"error": "Only GET requests are allowed"}, status=405)


def get_donations_of_user():
    pass