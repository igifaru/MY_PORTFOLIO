# myportfolio_App/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # This maps the root of the app to the home view
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
]
