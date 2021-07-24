from django.urls import path
from . import views


urlpatterns = [
    path("", views.projects, name="projects"),
    path("products/<str:pk>", views.products, name="products"),
]
