from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from projects.models import Project, Review
from .serializers import ProjectSerializer


@api_view(["GET"])
def getRoutes(request):

    routes = [
        {"GET": "/api/projects"},
        {"GET": "/api/projects/id"},
        {"POST": "/api/projects/id/vote"},  # for when people vote
        {"POST": "/api/users/token"},
        # This is how we log in our user
        {"POST": "/api/users/token/refresh"},
        # this helps ensure users stay logged in after initial token expires
    ]
    """
    setting safe = False tells us we can return more than just a python dictionary 
    we're setting safe = False because we're returning a list.
    """
    return Response(routes)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProjects(request):
    print("USER:", request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )

    review.value = data["value"]
    review.save()
    project.getVoteCount

    Serializer = ProjectSerializer(project, many=False)

    return Response(Serializer.data)
