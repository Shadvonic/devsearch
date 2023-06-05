from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile


def loginUser(request):

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
    messages.error(request,'User was  logged out')
    return redirect('login')


# Create your views here.
def profiles(request):
    profiles = Profile.objects.all()
    context = {
        'profiles':profiles
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