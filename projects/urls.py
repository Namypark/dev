from django.urls import path
from . import views


urlpatterns = [
    path("", views.projects, name="project"),
    path("products/<str:pk>", views.products, name="products"),
    path("create-project/welcome-to-creating-a-new-project",views.createProject, name="create-project"),
    path("update-project/welcome-to-updating-a-new-project/<str:pk>",views.updateProject, name="update-project"),
    path("delete-project/<str:pk>",views.deleteProject, name='delete-project'),
]
