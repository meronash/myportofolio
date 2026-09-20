from django.urls import path

from main.views import delete_education, delete_project, get_education_json, get_projects_json, show_main, show_experience, show_education, show_projects, create_education, create_project

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("education/add/", create_education, name="create_education"),
    path("education/", show_education, name="show_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("projects/<uuid:education_id>/delete/",delete_education,name="delete_project"),
    path("projects/add/", create_project, name="create_project"),
    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/<uuid:project_id>/delete/",delete_project,name="delete_project"),
]