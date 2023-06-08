from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.urls import conf 
from django.db.models import Q
from .models import Profile, Skill
from .forms import CustomUserCreationForm, ProfileForm, SkillForm


def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('profiles')


    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try: 
            #check if user exist in DB
            user = User.objects.get(username=username)
        except:
          messages.error(request, "Username does not exist.")

        # take in user name and password; make sure password matches user name 
        user = authenticate(request, username=username, password=password)

        # create a session for user in DB if the user exist 
        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request,'User OR password is incorrect')

    return render(request, 'users/login_register.html')


def logoutUser(request):
    logout(request)
    messages.info(request,'User was  logged out')
    return redirect('login')


def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # hold a temp instance before saving
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created!')

            login(request, user)
            return redirect('edit-account')
        else:
              messages.error(request, 'An error has occurred during registration')

    context = {
        'page':page,
        'form':form
    }
    return render(request, 'users/login_register.html', context)


# Create your views here.
def profiles(request):
    # return all profiles as default
    search_query, profiles = sea

    #  getting user input for search filter 
    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')


    # search filter 
    skills = Skill.objects.filter(name__iexact=search_query)
    profiles = Profile.objects.filter(Q(name__icontains=search_query)| Q(short_intro__icontains = search_query) | Q(skill__in=skills))

    context = {
        'profiles':profiles,
        'search_query': search_query
    }
    return render(request, 'users/profiles.html', context)

def userProfile(request,pk):
    profile = Profile.objects.get(id=pk)

    # if skill doesnt have desc filter out 
    topSkills = profile.skill_set.exclude(description__exact="")
    otherSkills = profile.skill_set.filter(description="")

    context = {
        'profile':profile, 
        'topSkills':topSkills,
        'otherSkills': otherSkills,
    }
    return render(request, 'users/user-profile.html', context)

@login_required(login_url='login')
def userAccount(request): 
    profile = request.user.profile 
    skills = profile.skill_set.all()
    projects = profile.project_set.all()


    context = {

        'profile':profile,
        'skills':skills,
        'projects':projects
       
    }
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()


            return redirect('account')


    context = {
        'form':form
    }
    return render(request, 'users/profile_form.html', context)



@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()


    #process form 
    if request.method == "POST":
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "Skill was added successfully!")
            return redirect('account')

    context = { 
        'form': form
    }
    return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)


    #process form 
    if request.method == "POST":
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill was updated successfully!")
            return redirect('account')

    context = { 
        'form': form
    }
    return render(request, 'users/skill_form.html', context)



def deleteSkill(request, pk):
    profile = request.user.profile 
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "Skill was deleted successfully!")
        return redirect('account')
    

    context = { 
        'object':skill
    }
    return render(request, 'delete_template.html', context)