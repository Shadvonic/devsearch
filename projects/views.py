from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project # import project model
from django.contrib.auth.decorators import login_required
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

@login_required(login_url="login")  # user has to be login to view this 
def createProject(request):
    form = ProjectForm()
    profile =request.user.profile

    # check method
    if request.method == 'POST':
        # create new instance of form
        form = ProjectForm(request.POST, request.FILES)
        # check data in valid 
        if form.is_valid():
            #save it
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            # redirect user
            return redirect('account')
       
    context = {
        'form':form
    }
    return render (request, "projects/project_form.html", context)

@login_required(login_url="login")  # user has to be login to view this 
def updateProject(request,pk):
    profile = request.user.profile
    # get project id 
    project = Project.project_set.get(id=pk)
    # prefill project data  on form
    form = ProjectForm(instance=project)

    # check method
    if request.method == 'POST':
        # what project its updating 
        form = ProjectForm(request.POST, request.FILES, instance=project)
        # check data in valid 
        if form.is_valid():
            # save it 
            form.save()
            # redirect user
            return redirect('account')
       
    context = {
        'form':form
    }
    return render (request, "projects/project_form.html", context)

@login_required(login_url="login")  # user has to be login to view this 
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('projects')
    
    context = {
        'object': project
    }

    return render(request,"delete_template.html", context)