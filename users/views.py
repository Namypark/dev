from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Profile, Skill, Message
from django.db.models import Q
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.core.mail import send_mail
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, MessageForm
from .utils import searchProfiles, paginateProfiles

 # Create your views here.


@csrf_protect
def loginUser(request):
    page = "login"

    if request.user.is_authenticated:
        return redirect("profiles")

    if request.method == "POST":
        username = request.POST["username"].lower()
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username does not exist")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'user-account')
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

    profiles, search_query = searchProfiles(request)
    custom_range, profiles = paginateProfiles(request,profiles, 3)
    context = {"profiles": profiles, "search_query": search_query, 'custom_range': custom_range}
    return render(request, "users/profile.html", context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topskills = profile.skill_set.exclude(description__exact="")
    otherskills = profile.skill_set.filter(description="")

    context = {"profile": profile, "topskills": topskills, "otherskills": otherskills}
    return render(request, "users/user-profiles.html", context)


@login_required(login_url="login")
def userAccount(request):

    profile = request.user.profile
    topskills = profile.skill_set.all()
    projects = profile.project_set.all()
    context = {"profile": profile, "topskills": topskills, "projects": projects}
    return render(request, "users/user-account.html", context)


@login_required(login_url="login")
def editAccount(request):
    profile = request.user.profile
    forms = ProfileForm(instance=profile)

    if request.method == "POST":
        forms = ProfileForm(request.POST, request.FILES, instance=profile)
        if forms.is_valid():
            forms.save()
            messages.success(request, "profile updated successfully")
            return redirect("user-account")

    context = {"forms": forms}
    return render(request, "users/profile-form.html", context)


# * performing CRUD operations on the skills
# --------------------------------------------> C
@login_required(login_url="login")
def createSkill(request):
    profile = request.user.profile
    forms = SkillForm
    if request.method == "POST":
        forms = SkillForm(request.POST)
        if forms.is_valid():
            skill = forms.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, "skill added successfully")
            return redirect("user-account")

    context = {"forms": forms}
    return render(request, "users/skill-form.html", context)


# --------------------------------------------> U


@login_required(login_url="login")
def updateSkill(request, pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    forms = SkillForm(instance=skill)
    if request.method == "POST":
        forms = SkillForm(request.POST, instance=skill)
        if forms.is_valid():
            skill = forms.save(commit=False)
            messages.success(request, "skill updated successfully")
            return redirect("user-account")

    context = {"forms": forms}
    return render(request, "users/skill-form.html", context)


# --------------------------------------------> D
@login_required(login_url="login")
def deleteSkill(request, pk):

    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == "POST":
        skill.delete()
        messages.success(request, "skill was deleted successfully")
        return redirect("user-account")
    context = {"object": skill}
    return render(request, "delete.html", context)

@login_required(login_url="login")
def inbox(request):
    profile = request.user.profile
    message_requests = profile.messages.all()
    unreadCount = message_requests.filter(is_read=False).count()
    context = {'message_requests': message_requests, 'unreadCount': unreadCount}
    return render(request, "users/inbox.html",context)


@login_required(login_url="login")
def viewMessage(request, pk):
    
    profile = request.user.profile
    message_received = profile.messages.get(id=pk)
    if message_received.is_read == False:
        message_received.is_read = True 
        message_received.save()
    context = {'message_received': message_received}
    
    return render(request, "users/message.html", context)


def createMessage(request, pk):
    
    recipient = Profile.objects.get(id=pk)
    form = MessageForm() 
    
    try:
        sender = request.user.profile
        
    except:
        sender = None
        
    if request.method == "POST":
        form =  MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            
            messages.success(request, "Message successfully sent!")
            return redirect("user-profile", pk=recipient.id )
                
    context = {'recipient':recipient, 'form':form}
    return render(request, "users/message_form.html",context)