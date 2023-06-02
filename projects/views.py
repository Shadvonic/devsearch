from django.shortcuts import render
from django.http import HttpResponse
from .models import Project # import project model
from .forms import ProjectForm




# func get tiggers when one of the routes gets trigger
def projects(request):
    # give all the objects in the db table
    projects = Project.objects.all()
    context = { 
        'projects':projects
        }
    return render(request, 'projects/projects.html', context)

def project(request, pk):
    projectObj = Project.objects.get(id=pk)
    print('projectObj:', projectObj)
    tags = projectObj.tags.all()
  
    return render(request, 'projects/single-project.html', {'project':projectObj})


def createProject(request):
    form = ProjectForm()
    context = {
        'form':form
    }
    return render (request, "projects/project_form.html", context)