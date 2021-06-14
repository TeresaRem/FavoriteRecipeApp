from django.urls import path
from recipe_app.views import *
from . import views


urlpatterns = [
    path('',views.index),
    path('sign-in', views.sign_in),
    path('register',views.register),
    path('protected', views.protected),
    #this is the homepage
    path('home', views.home),
    #to log out
    path('logout', views.logout),
    #to view uploaded meals
    path('dashboard', views.dashboard),
    #to add new fave
    path('add_to_fave', views.add_to_fave),
    path('create',views.create),
    
    path('back', views.back),
    
    #to edit fave
    path('dashboard/<int:id>/edit',views.edit),
    
    path('dashboard/<int:id>/delete', views.delete),
]