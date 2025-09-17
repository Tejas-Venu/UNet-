from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password

from UNet import settings
from .models import NGO
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NGO
from .utils import get_recommendations
from django.core.mail import send_mail





@csrf_exempt
def login_ngo(request):
    """Logs in the NGO."""
    if request.method == "POST":
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        try:
            ngo = NGO.objects.get(email=email)
            if ngo.password == password:  # Replace this with secure password hashing in production
                request.session['ngo_id'] = ngo.id
                return JsonResponse({"message": "Login successful", "ngo_id": ngo.id}, status=200)
            return JsonResponse({"error": "Invalid password"}, status=401)
        except NGO.DoesNotExist:
            return JsonResponse({"error": "NGO not found"}, status=404)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@login_required
def logout_ngo(request):
    """Logs out the NGO."""
    if request.session.get('ngo_id'):
        del request.session['ngo_id']
        return JsonResponse({"message": "Logged out successfully"}, status=200)
    return JsonResponse({"error": "No NGO logged in"}, status=400)


@csrf_exempt
@login_required
def update_ngo(request):
    """Updates the profile of the logged-in NGO."""
    if request.method == "PUT":
        ngo_id = request.session.get('ngo_id')
        if not ngo_id:
            return JsonResponse({"error": "No NGO logged in"}, status=400)

        try:
            ngo = NGO.objects.get(id=ngo_id)
            data = json.loads(request.body)
            ngo.name = data.get("name", ngo.name)
            ngo.mobile_number = data.get("mobile_number", ngo.mobile_number)
            ngo.email = data.get("email", ngo.email)
            ngo.address = data.get("address", ngo.address)
            ngo.contact_person = data.get("contact_person", ngo.contact_person)
            ngo.purpose = data.get("purpose", ngo.purpose)
            ngo.save()
            return JsonResponse({"message": "NGO profile updated successfully"}, status=200)
        except NGO.DoesNotExist:
            return JsonResponse({"error": "NGO not found"}, status=404)
    return JsonResponse({"error": "Only PUT requests are allowed"}, status=405)


@csrf_exempt
def create_ngo(request):
    """Registers a new NGO."""
    if request.method == "POST":
        data = json.loads(request.body)
        name = data.get("name")
        mobile_number = data.get("mobile_number")
        email = data.get("email")
        address = data.get("address")
        contact_person = data.get("contact_person")
        purpose = data.get("purpose")
        password = data.get("password")

        if not all([name, mobile_number, email, address, contact_person, purpose, password]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        if NGO.objects.filter(email=email).exists():
            return JsonResponse({"error": "Email already exists"}, status=400)

        ngo = NGO.objects.create(
            name=name,
            mobile_number=mobile_number,
            email=email,
            address=address,
            contact_person=contact_person,
            purpose=purpose,
            password=password  # Replace this with secure password hashing in production
        )
        return JsonResponse({"message": "NGO created successfully", "ngo_id": ngo.id}, status=201)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


@login_required
def view_ngo(request):
    """Returns all details of the logged-in NGO."""
    if request.method == "GET":
        ngo_id = request.session.get('ngo_id')
        if not ngo_id:
            return JsonResponse({"error": "No NGO logged in"}, status=400)

        try:
            ngo = NGO.objects.get(id=ngo_id)
            ngo_data = {
                "id": ngo.id,
                "name": ngo.name,
                "mobile_number": ngo.mobile_number,
                "email": ngo.email,
                "address": ngo.address,
                "contact_person": ngo.contact_person,
                "purpose": ngo.purpose,
            }
            return JsonResponse(ngo_data, status=200)
        except NGO.DoesNotExist:
            return JsonResponse({"error": "NGO not found"}, status=404)
    return JsonResponse({"error": "Only GET requests are allowed"}, status=405)


@api_view(['GET'])
def recommend_ngos(request):
    ngo_name = request.query_params.get('ngo_name', None)
    total_ngos = NGO.objects.count()
    print(ngo_name)
    if ngo_name==None:
        ngos = NGO.objects.all()[:total_ngos]
        top_ngos = [{'id': ngo.id, 'name': ngo.name} for ngo in ngos]
        return Response(top_ngos)

    recommendations = get_recommendations(ngo_name)
    
    if not recommendations:
        ngos = NGO.objects.all()[:total_ngos]
        top_ngos = [{'id': ngo.id, 'name': ngo.name} for ngo in ngos]
        return Response(top_ngos)

    return Response(recommendations)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import NGO

@api_view(['GET'])
def ngo_details(request, ngo_id):
    try:
        ngo = NGO.objects.get(id=ngo_id)
        return Response({
            'name': ngo.name,
            'purpose': ngo.purpose,
            'address': ngo.address,
            'contact_person': ngo.contact_person,
            'email': ngo.email,
            'mobile_number': ngo.mobile_number,
            'completed_project': ngo.completed_project,
            'ongoing_project': ngo.ongoing_project,
        })
    except NGO.DoesNotExist:
        return Response({"error": "NGO not found."}, status=404)
    
@csrf_exempt
def email_service(request):
    print("send_email view called")
    if request.method == 'POST':
        print("POST request received")
        try:
            data = json.loads(request.body)
            user_name = data.get('user_name')
            user_email = data.get('user_email')
            ngo_name = data.get('ngo_name')
            ngo_email = data.get('ngo_email')
            action = data.get('action')  # "volunteer" or "donate"

            # Log the details for debugging
            print(f"Action: {action}")
            print(f"User Name: {user_name}")
            print(f"User Email: {user_email}")
            print(f"NGO Name: {ngo_name}")
            print(f"NGO Email: {ngo_email}")

            message =""
            if action == 'volunteer':
                message = message = f"Hey {ngo_name}, {user_name} ({user_email}) wants to {action} at {ngo_name}! Please reach out to them at {user_email}"
            if action == 'donate':
                message = f"Hey {ngo_name}, {user_name} ({user_email}) wants to {action} to {ngo_name}! Please reach out to them at {user_email}"
    
            print(f"Email Message: {message}")

            send_mail(
                subject="Notification from UNet: New Request",
                message=message,  # Email body
                from_email= settings.EMAIL_HOST_USER,  # Use EMAIL_HOST_USER
                recipient_list=['connectforimpact.project@gmail.com'],  # Dummy recipient for testing
                fail_silently=False,  # Raise errors if email sending fails
            )

            return JsonResponse({'message': 'Email processed successfully!'}, status=200)
        except Exception as e:
            print(str(e))
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from .models import NGO

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register_ngo(request):
    """
    Register a new NGO with the provided details.
    """
    try:
        # Extract data from the request
        data = request.data
        name = data.get('name')
        mobile_number = data.get('mobile_number')
        email = data.get('email')
        address = data.get('address')
        contact_person = data.get('contact_person')
        purpose = data.get('purpose')
        completed_project = data.get('completed_project', 'No Completed Projects')
        ongoing_project = data.get('ongoing_project', 'Not Applicable')
        account_number = data.get('account_number', '0000000000000000')

        # Validation
        if not all([name, mobile_number, email, address, contact_person, purpose]):
            return JsonResponse({"error": "All fields except 'completed_project' and 'ongoing_project' are required."}, status=HTTP_400_BAD_REQUEST)

        if NGO.objects.filter(email=email).exists():
            return JsonResponse({"error": "An NGO with this email already exists."}, status=HTTP_400_BAD_REQUEST)

        if NGO.objects.filter(account_number=account_number).exists():
            return JsonResponse({"error": "This account number is already associated with an NGO."}, status=HTTP_400_BAD_REQUEST)

        # Save the NGO to the database
        ngo = NGO.objects.create(
            name=name,
            mobile_number=mobile_number,
            email=email,
            address=address,
            contact_person=contact_person,
            purpose=purpose,
            completed_project=completed_project,
            ongoing_project=ongoing_project,
            account_number=account_number
        )

        return JsonResponse(
            {"message": "NGO registered successfully", "ngo_id": ngo.id},
            status=HTTP_201_CREATED
        )

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=HTTP_400_BAD_REQUEST)

