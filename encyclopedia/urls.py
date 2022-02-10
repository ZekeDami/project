from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.open, name = 'open'),
    path('add',views.new, name = 'new'),
    path('random', views.random, name = 'random'),
    path("wiki/edit/<str:title>", views.edit, name = 'edit')
]
