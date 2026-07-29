# myportfolio_App/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This maps the root of the app to the home view
    path('about/', views.about, name='about'),
    path('cv-preview/', views.cv_preview, name='cv_preview'),
    path('project/', views.portfolio, name='portfolio'),
    path('project/<int:pk>/', views.project_detail, name='project_detail'),
    path('contact/', views.contact, name='contact'),
    
]
