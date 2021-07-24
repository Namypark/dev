from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


details = [
    {
        "id": "1",
        "name": "Namy",
        "title": "Socials",
        "description": "this is a little something about the owner of the text",
    },
    {
        "id": "2",
        "name": "unknown",
        "title": "Legend of the Northern Blade",
        "description": "the description for name is unknown",
    },
]


def projects(request):
    context = {"details": details}
    return render(request, "projects/projects.html", context)


def products(request, pk):
    projectObj = None
    for i in details:
        if i["id"] == pk:
            projectObj = i
    return render(request, "projects/single-projects.html", {"projectObj": projectObj})
