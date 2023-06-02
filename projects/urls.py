from django.urls import path 
from . import views

# any url pattern that has anything to do with projects
urlpatterns = [
    # going into views folder to get func
    path('', views.projects, name="projects"),
    # passing in data
    path('project/<str:pk>/', views.project, name="project"),
    path('create-project/',views.createProject, name="create-project"),
]
