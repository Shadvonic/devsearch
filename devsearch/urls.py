from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    # route domain
    # go into projects folder and include urls.py file
    path('', include('projects.urls'))
 
]
