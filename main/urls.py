from django.urls import path

from main.views import (create_education_ajax, create_experience_ajax, create_project_ajax,
                        delete_education_ajax, delete_experience_ajax, delete_project_ajax,
                        update_education_ajax, update_experience_ajax, update_project_ajax,
                        get_education_json, get_experience_json, get_projects_json,
                        login_user, logout_user, register, show_main,
                        show_experience, show_education, show_projects,
                        toggle_star, toggle_star_education, toggle_star_experience,)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("register/", register, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),

    path("projects/", show_projects, name="show_projects"),
    path("api/projects/", get_projects_json, name="get_projects_json"),
    path("projects/add-ajax/", create_project_ajax, name="create_project_ajax"),
    path("projects/update-ajax/<uuid:project_id>/", update_project_ajax, name="update_project_ajax"),
    path("projects/<uuid:project_id>/delete-ajax/", delete_project_ajax, name="delete_project_ajax"),
    path("projects/<uuid:project_id>/star/", toggle_star, name="toggle_star"),

    path("experience/", show_experience, name="show_experience"),
    path("api/experience/", get_experience_json, name="get_experience_json"),
    path("experience/add-ajax/", create_experience_ajax, name="create_experience_ajax"),
    path("experience/update-ajax/<uuid:experience_id>/", update_experience_ajax, name="update_experience_ajax"),
    path("experience/<uuid:experience_id>/delete-ajax/", delete_experience_ajax, name="delete_experience_ajax"),
    path("experience/<uuid:experience_id>/star/", toggle_star_experience, name="toggle_star_experience"),

    path("education/", show_education, name="show_education"),
    path("api/education/", get_education_json, name="get_education_json"),
    path("education/add-ajax/", create_education_ajax, name="create_education_ajax"),
    path("education/update-ajax/<uuid:education_id>/", update_education_ajax, name="update_education_ajax"),
    path("education/<uuid:education_id>/delete-ajax/", delete_education_ajax, name="delete_education_ajax"),
    path("education/<uuid:education_id>/star/", toggle_star_education, name="toggle_star_education"),
]