from django.shortcuts import render

from main.models import Experience


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