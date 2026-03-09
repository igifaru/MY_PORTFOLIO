from django.db import models

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    technology = models.CharField(max_length=100) # e.g., "Django, Tailwind"
    image = models.ImageField(upload_to='projects/')
    link = models.URLField(blank=True) # Link to GitHub or live site
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

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Skill(models.Model):
    name = models.CharField(max_length=50)
    # Link to the dynamic Category table
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='skills')
    proficiency = models.IntegerField(help_text="Enter value 1-100")

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

class Service(models.Model):
    title = models.CharField(max_length=100)
    icon_class = models.CharField(max_length=50, help_text="FontAwesome class (e.g., 'fas fa-code')")
    description = models.TextField()
    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title

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
    profile_image = models.ImageField(upload_to='profile/', blank=True, null=True)
    github_link = models.URLField(blank=True)
    linkedin_link = models.URLField(blank=True)
    facebook_link = models.URLField(blank=True)
    twitter_link = models.URLField(blank=True)
    instagram_link = models.URLField(blank=True)
    cv = models.FileField(upload_to='cv/', blank=True, null=True, help_text="Upload your CV/Résumé (PDF format)")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Bio / About Section"


