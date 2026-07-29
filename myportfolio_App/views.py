import logging

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import FileResponse, Http404
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Project, Bio, Skill, ContactMessage, Certificate
from django.db.models import Count
from django.contrib import messages

logger = logging.getLogger(__name__)

def home(request):
    projects = Project.objects.all()
    bio = Bio.objects.first()
    categories = Category.objects.annotate(n_skills=Count('skills')).filter(n_skills__gt=0).order_by('order')
    certificates = Certificate.objects.all()
    return render(request, 'home.html', {
        'projects': projects,
        'bio': bio,
        'categories': categories,
        'certificates': certificates,
    })

def about(request):
    # Only pull categories that have at least one skill linked to them
    categories = Category.objects.annotate(n_skills=Count('skills')).filter(n_skills__gt=0).order_by('order')
    bio = Bio.objects.first()
    certificates = Certificate.objects.all()
    return render(request, 'about.html', {'categories': categories, 'bio': bio, 'certificates': certificates})

def contact(request):
    bio = Bio.objects.first()
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        ContactMessage.objects.create(name=name, email=email, subject=subject, message=message)

        try:
            send_mail(
                subject=f"Portfolio Contact: {subject}",
                message=f"From: {name} <{email}>\n\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_RECIPIENT_EMAIL],
                fail_silently=False,
            )
        except Exception:
            logger.exception("Failed to send contact form email")

        messages.success(request, "Your message has been sent successfully!")
        return redirect(reverse('home') + '#contact')
    return render(request, 'contact.html', {'bio': bio})

@xframe_options_sameorigin
def cv_preview(request):
    bio = Bio.objects.first()
    if not bio or not bio.cv:
        raise Http404
    return FileResponse(bio.cv.open('rb'), content_type='application/pdf')

def portfolio(request):
    projects = Project.objects.all()
    bio = Bio.objects.first()
    return render(request, 'portfolio.html', {'projects': projects, 'bio': bio})

def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)
    bio = Bio.objects.first()
    return render(request, 'project_detail.html', {'project': project, 'bio': bio})
