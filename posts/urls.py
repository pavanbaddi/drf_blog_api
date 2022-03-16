import imp
from django.urls import path
from posts import views

urlpatterns = [
    path('', views.ListApi.as_view()),
    path('create', views.CreateApi.as_view()),
    path('<int:pk>', views.EditApi.as_view()),
    path('update', views.CreateApi.as_view()),
    path('remove/<int:pk>', views.DeleteApi.as_view()),
]