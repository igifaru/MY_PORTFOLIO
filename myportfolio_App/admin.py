from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Skill, ContactMessage

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    # Displays these columns in the list view
    list_display = ('title', 'technology', 'display_image')
    search_fields = ('title', 'technology')
    
    # Shows a small preview of the project image in the admin list
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:auto; border-radius:5px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Preview'

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency')
    list_filter = ('category',) # Allows filtering by Frontend/Backend
    search_fields = ('name',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    # Messages should be read-only in most cases to prevent accidental editing
    list_display = ('name', 'subject', 'email', 'created_at')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    search_fields = ('name', 'email', 'subject')
    list_per_page = 20
