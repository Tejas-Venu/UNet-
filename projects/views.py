from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Project
from ngos.models import NGO
import json


@csrf_exempt
@login_required
def update_project(request, project_id):
    """Edits a project of an NGO if they are logged in."""
    if request.method == "PUT":
        ngo_id = request.session.get("ngo_id")
        if not ngo_id:
            return JsonResponse({"error": "NGO not logged in"}, status=400)

        try:
            project = Project.objects.get(id=project_id, ngo_id=ngo_id)
            data = json.loads(request.body)
            project.title = data.get("title", project.title)
            project.desc = data.get("desc", project.desc)
            project.start_date = data.get("start_date", project.start_date)
            project.end_date = data.get("end_date", project.end_date)
            project.status = data.get("status", project.status)
            project.save()
            return JsonResponse({"message": "Project updated successfully"}, status=200)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found or unauthorized"}, status=404)
    return JsonResponse({"error": "Only PUT requests are allowed"}, status=405)


@csrf_exempt
@login_required
def create_project(request):
    """Creates a new project for an NGO if they are logged in."""
    if request.method == "POST":
        ngo_id = request.session.get("ngo_id")
        if not ngo_id:
            return JsonResponse({"error": "NGO not logged in"}, status=400)

        data = json.loads(request.body)
        title = data.get("title")
        desc = data.get("desc")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        status = data.get("status")

        if not all([title, desc, start_date, end_date, status]):
            return JsonResponse({"error": "All fields are required"}, status=400)

        Project.objects.create(
            title=title,
            desc=desc,
            start_date=start_date,
            end_date=end_date,
            status=status,
            ngo_id=ngo_id,
        )
        return JsonResponse({"message": "Project created successfully"}, status=201)
    return JsonResponse({"error": "Only POST requests are allowed"}, status=405)


def view_details(request, project_id):
    """View details of a specific project."""
    if request.method == "GET":
        try:
            project = Project.objects.get(id=project_id)
            project_details = {
                "id": project.id,
                "title": project.title,
                "desc": project.desc,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "status": project.status,
                "ngo_name": project.ngo.name,
            }
            return JsonResponse(project_details, status=200)
        except Project.DoesNotExist:
            return JsonResponse({"error": "Project not found"}, status=404)
    return JsonResponse({"error": "Only GET requests are allowed"}, status=405)


def list_projects(request, ngo_id):
    """Lists all projects of a particular NGO."""
    if request.method == "GET":
        try:
            ngo = NGO.objects.get(id=ngo_id)
            projects = Project.objects.filter(ngo_id=ngo.id)
            project_list = [
                {
                    "id": project.id,
                    "title": project.title,
                    "desc": project.desc,
                    "start_date": project.start_date,
                    "end_date": project.end_date,
                    "status": project.status,
                }
                for project in projects
            ]
            return JsonResponse({"ngo_name": ngo.name, "projects": project_list}, status=200)
        except NGO.DoesNotExist:
            return JsonResponse({"error": "NGO not found"}, status=404)
    return JsonResponse({"error": "Only GET requests are allowed"}, status=405)
