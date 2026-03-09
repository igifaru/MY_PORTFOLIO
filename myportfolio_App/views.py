from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Project, Bio, Skill, ContactMessage, Service
from django.db.models import Count
from django.contrib import messages

def home(request):
    projects = Project.objects.all()
    bio = Bio.objects.first()
    return render(request, 'home.html', {'projects': projects, 'bio': bio})

def about(request):
    # Only pull categories that have at least one skill linked to them
    categories = Category.objects.annotate(n_skills=Count('skills')).filter(n_skills__gt=0)
    bio = Bio.objects.first()
    return render(request, 'about.html', {'categories': categories, 'bio': bio})

def contact(request):
    bio = Bio.objects.first()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        ContactMessage.objects.create(name=name, email=email, phone=phone, subject=subject, message=message)
        messages.success(request, "Your message has been sent successfully!")
        return redirect('contact')
    return render(request, 'contact.html', {'bio': bio})

def services(request):
    services_list = Service.objects.all()
    bio = Bio.objects.first()
    return render(request, 'services.html', {'services': services_list, 'bio': bio})

def portfolio(request):
    projects = Project.objects.all()
    bio = Bio.objects.first()
    return render(request, 'portfolio.html', {'projects': projects, 'bio': bio})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bio = Bio.objects.first()
    return render(request, 'project_detail.html', {'project': project, 'bio': bio})
