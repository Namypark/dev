from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Project
from .forms import ProjectForm

# Create your views here.

# READ---------------------------------------------------------->
def projects(request):

    projects = Project.objects.all()
    context = {"projects": projects}
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
def createProject(request):

    form = ProjectForm()
    if request.method == "POST":

        form = ProjectForm(request.POST,request.FILES)
        form.save()
        return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)
#CREATE-------------------------------------------------------------------->

#UPDATE-------------------------------------------------------------------->
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        form = ProjectForm(request.POST,request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect("projects")

    context = {"form": form}
    return render(request, "projects/project_form.html", context)
#UPDATE-------------------------------------------------------------------->

#DELETE-------------------------------------------------------------------->
def deleteProject(request, pk):
    project=  Project.objects.get(id=pk)
    context = {"project": project}
    if request.method == "POST":
        project.delete()
        return redirect("projects")
    return render(request, "projects/delete.html",context)
#DELETE-------------------------------------------------------------------->
