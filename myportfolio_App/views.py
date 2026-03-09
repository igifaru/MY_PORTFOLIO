from django.shortcuts import render,redirect
from .models import Category
from .models import *

def home(request):
    projects = Project.objects.all()
    bio = Bio.objects.first()
    return render(request, 'home.html', {'projects': projects, 'bio': bio})

# def about(request):
#     skills = Skill.objects.all().order_by('category')
#     return render(request, 'about.html', {'skills': skills})
# myportfolio_App/views.py


# myportfolio_App/views.py
from django.db.models import Count

def about(request):
    # Only pull categories that have at least one skill linked to them
    categories = Category.objects.annotate(n_skills=Count('skills')).filter(n_skills__gt=0)
    bio = Bio.objects.first()  # Fetch the dynamic bio data
    return render(request, 'about.html', {'categories': categories, 'bio': bio})





from django.contrib import messages

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    return render(request, 'contact.html')
def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})

from django.shortcuts import render, redirect, get_object_or_404

def portfolio(request):
    projects = Project.objects.all()
    return render(request, 'portfolio.html', {'projects': projects})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return render(request, 'project_detail.html', {'project': project})
