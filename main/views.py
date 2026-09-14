from django.contrib import messages
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from main.models import Experience, Education, Project
from main.forms import ProjectForm


def show_main(request):
    context = {
        "name": "Rona Mahira",
        "npm": "2506657314",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Hi! I'm an Information Systems student at Universitas Indonesia "
            "passionate aboout Game Development and Animation."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Rona",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)

def show_education(request):
    context = {
        "name": "Rona",
        "education_list": Education.objects.all(),
    }
    return render(request, "education.html", context)

def create_project(request):
    form = ProjectForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Proyek baru berhasil ditambahkan!")
        return redirect("main:show_projects")

    context = {
        "name": "Rona",
        "form": form,
    }
    return render(request, "projects_form.html", context)

def show_projects(request):
    context = {
        "name": "Rona",
        "project_list": Project.objects.all(),
    }
    return render(request, "project.html", context)

def get_projects_json(request):
    title_query = request.GET.get("title", "").strip()
    projects = Project.objects.all()

    if title_query:
        projects = projects.filter(title__icontains=title_query)

    projects_json = serializers.serialize("json", projects)
    return HttpResponse(projects_json, content_type="application/json")

def delete_project(request, project_id):
    project = get_object_or_404(Project, pk=project_id)

    if request.method == "POST":
        project.delete()
        messages.success(request, "Project berhasil dihapus!")
        return redirect("main:show_projects")

    return redirect("main:show_projects")