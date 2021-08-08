from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm

# Create your views here.  


@csrf_protect
def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            messages.success(request, f"Welcome {user}!")

            login(request, user)
            return redirect("profiles")
        else:
            messages.error(
                request, "username or password is not correct please try again"
            )
    return render(request, "users/login-register.html")


@csrf_protect
def logoutUser(request):
    logout(request)
    messages.info(request, "user logout successful!")
    return redirect("login")


@csrf_protect
def registerUser(request):
    page = "register"
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            # saving but holding a temporary instance of it
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request, "Account created successfully!")
            login(request, user)
            return redirect("edit-account")

        else:
            messages.error(request, "An error has occured during registration")

    context = {"page": page, "form": form}
    return render(request, "users/login-register.html", context)


def profiles(request):
    profiles = Profile.objects.all()
    context = {"profiles": profiles}

    return render(request, "users/profile.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(username=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topskills": topskills, "otherskills": otherskills}
    return render(request, "users/user-profiles.html", context)


@login_required(login_url="login")
def userAccount(request):

    profile = request.user.profile
    topskills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile,'topskills':topskills,'projects':projects}
    return render(request, "users/user-account.html", context)

@login_required(login_url='login')
def editAccount(request):
    profile = request.user.profile
    forms  = ProfileForm(instance= profile)

    if request.method == 'POST':
        forms = ProfileForm(request.POST,request.FILES, instance=profile)
        if forms.is_valid():
            forms.save()   
            messages.success(request,"profile updated successfully")
            return redirect('user-account')

    context = {'forms':forms}
    return render(request, "users/profile-form.html",context)