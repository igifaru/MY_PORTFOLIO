from django.db import models
from django.core.validators import FileExtensionValidator

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology = models.CharField(max_length=100) # e.g., "Django, Tailwind"
    image = models.ImageField(upload_to='projects/')
    github_link = models.URLField(blank=True, help_text="Link to the GitHub repository")
    live_link = models.URLField(blank=True, help_text="Link to the live/deployed site")
    long_description = models.TextField(blank=True, help_text="Detailed description for the project page")

    def __str__(self):
        return self.title

# class Skill(models.Model):
#     CATEGORY_CHOICES = [
#         ('Frontend', 'Frontend'),
#         ('Backend', 'Backend'),
#         ('Tools', 'Tools/DevOps'),
#     ]
#     name = models.CharField(max_length=50)
#     category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
#     proficiency = models.IntegerField(help_text="Enter value 1-100")

#     def __str__(self):
#         return self.name
# myportfolio_App/models.py


class Category(models.Model):
    # This allows the admin to type ANY name they want
    name = models.CharField(max_length=100, unique=True)
    order = models.IntegerField(default=0, help_text="Controls display order in the Technical Arsenal section")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

class Skill(models.Model):
    name = models.CharField(max_length=50, help_text="Enter with correct casing, e.g. 'PostgreSQL', 'REST APIs', 'DNS'")
    # Link to the dynamic Category table
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills')

    def __str__(self):
        return f"{self.name} ({self.category.name})"

    

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name}"

class Certificate(models.Model):
    title = models.CharField(max_length=200, help_text="e.g. 'Certified Django Developer'")
    institution = models.CharField(max_length=200, help_text="e.g. 'Coursera', 'AWS', 'University of Rwanda'")
    file = models.FileField(upload_to='certificates/', help_text="Upload the certificate as a PDF")
    order = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} - {self.institution}"

    class Meta:
        ordering = ['order']

class Bio(models.Model):
    full_name = models.CharField(max_length=200, default="David Kendric")
    roles_list = models.CharField(max_length=500, default="Frontend Developer, Backend Enthusiast", help_text="Comma-separated roles for the typewriter effect")
    hero_title = models.CharField(max_length=200, default="Hello, It's Me")
    hero_subtitle = models.TextField(default="Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusantium, ab autem repellat reiciendis ipsam perspiciatis.")
    about_title_main = models.CharField(max_length=200, default="About")
    about_title_accent = models.CharField(max_length=200, default="Me")
    about_role = models.CharField(max_length=200, default="Django & Python Architect!")
    title = models.CharField(max_length=200, default="The Developer Behind the Code")
    bio_text = models.TextField(default="I am a specialized Django & Python Architect focused on building high-performance backend systems. I turn complex business requirements into elegant, scalable digital solutions with a focus on security and efficiency.")
    extra_bio_text = models.TextField(
        blank=True,
        help_text="Short personal paragraph revealed when a visitor clicks 'Read More' on the About section."
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        help_text="Shown in Google search results and when the site is shared on social media. "
                   "Keep it under ~160 characters. Falls back to the hero subtitle if left blank."
    )
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    whatsapp_link = models.URLField(blank=True, help_text="Full WhatsApp link, e.g. https://wa.me/250781234567")
    cv = models.FileField(
        upload_to='cv/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        help_text="Upload your CV/Résumé (PDF format only)"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Bio / About Section"


