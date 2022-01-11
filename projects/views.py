from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from .utils import searchProjects, paginateProject
# Create your views here

# READ---------------------------------------------------------->
def projects(request):

    projects, search_query = searchProjects(request)
    custom_range, projects = paginateProject(request, projects, 6)


    context = {"projects": projects,'search_query': search_query, "custom_range": custom_range}
    return render(request, "projects/projects.html", context)

def products(request, pk):

    projectObj = Project.objects.get(id=pk)
    tags = projectObj.tags.all()
    
    return render(
        request,
        "projects/single-projects.html",
        {"projectObj": projectObj, "tags": tags},
    )
#READ--------------------------------------------------------------------->

#CREATE-------------------------------------------------------------------->
@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()
    if request.method == "POST":

        form = ProjectForm(request.POST,request.FILES)
        project = form.save(commit=False)
        project.owner = profile
        project.save() 
        return redirect("user-account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)
#CREATE-------------------------------------------------------------------->

#UPDATE-------------------------------------------------------------------->
@login_required(login_url='login')
def updateProject(request, pk):
    profile =request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("user-account")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)
#UPDATE-------------------------------------------------------------------->

#DELETE-------------------------------------------------------------------->
@login_required(login_url='login')
def deleteProject(request, pk):
    profile =request.user.profile
    projects=  profile.project_set.get(id=pk)
    if request.method == "POST":
        projects.delete()
        return redirect("user-account")

    context = {"object": projects}
    return render(request, "delete.html",context)
#DELETE-------------------------------------------------------------------->
