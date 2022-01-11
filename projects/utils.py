from django.db.models import Q
from .models import Project, Tag
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger



def paginateProject(request, projects, results: int):
    page = request.GET.get('page')
    paginator = Paginator(projects, results)
      
    try:
        projects = paginator.page(page)

    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    
    #This logic helps ensure that if we do have a large number of pages, we see a few so the page is not crowded
    leftIndex = (int(page) - 4)
    if leftIndex < 1:
        leftIndex =1
    
    rightIndex = (int(page) + 5)
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1


    custom_range = range(leftIndex,rightIndex)

    return custom_range, projects


def searchProjects(request):
    search_query = ""
    if request.GET.get("search_query"):
        search_query = request.GET.get("search_query")

    tags = Tag.objects.filter(name__icontains=search_query)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query)
        | Q(tags__in=tags)
        | Q(owner__name__icontains=search_query)
    )
    return projects, search_query