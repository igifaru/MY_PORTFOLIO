from django.shortcuts import render,redirect
from .models import *

def home(request):
    projects = Project.objects.all()
    return render(request, 'home.html', {'projects': projects})

def about(request):
    skills = Skill.objects.all().order_by('category')
    return render(request, 'about.html', {'skills': skills})

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)
        return redirect('home') # Redirect after success
    return render(request, 'contact.html')
