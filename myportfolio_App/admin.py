from django.contrib import admin
from django.utils.html import format_html
from .models import Project, Skill, Category, ContactMessage, Bio, Certificate

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('title', 'institution', 'order')
    list_editable = ('order',)
    search_fields = ('title', 'institution')

    class Media:
        css = {
            'all': ('myportfolio_App/css/admin_custom.css',)
        }

# --- Admin Customization (Branding) ---
admin.site.site_header = "Portfolio CMS"
admin.site.site_title = "David's Portfolio Admin"
admin.site.index_title = "Welcome to your Website Manager"

# --- 1. Skills Inline for Categories ---
class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1 # Allow adding new skills directly
    min_num = 0

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'skill_count')
    list_editable = ('order',)
    search_fields = ('name',)
    inlines = [SkillInline]

    def skill_count(self, obj):
        return obj.skills.count()
    skill_count.short_description = "Skills count"

    class Media:
        css = {
            'all': ('myportfolio_App/css/admin_custom.css',)
        }

# --- 2. Skills ---
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

    class Media:
        css = {
            'all': ('myportfolio_App/css/admin_custom.css',)
        }

# --- 3. Projects ---
@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'technology', 'display_image', 'link_exists')
    list_filter = ('technology',)
    search_fields = ('title', 'technology', 'description')

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'long_description', 'technology'),
        }),
        ('Media & Links', {
            'fields': ('image', 'github_link', 'live_link'),
            'description': 'Upload your project preview and provide a GitHub repository link and/or a live/deployed site link.'
        }),
    )

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height:auto; border-radius:5px; border: 1px solid #ddd;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Preview'

    def link_exists(self, obj):
        return bool(obj.github_link or obj.live_link)
    link_exists.boolean = True
    link_exists.short_description = 'Has Link'

    class Media:
        css = {
            'all': ('myportfolio_App/css/admin_custom.css',)
        }

# --- 4. Contact Messages (Read-Only) ---
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'subject', 'email', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    class Media:
        css = {
            'all': ('myportfolio_App/css/admin_custom.css',)
        }
    
# --- 5. Bio / About Section ---
@admin.register(Bio)
class BioAdmin(admin.ModelAdmin):
    list_display = ('title', 'has_image')
    
    fieldsets = (
        ('Hero Section (Home Page)', {
            'fields': ('full_name', 'roles_list', 'hero_title', 'hero_subtitle'),
        }),
        ('About Section (About Page)', {
            'fields': ('about_title_main', 'about_title_accent', 'about_role', 'bio_text', 'extra_bio_text'),
            'classes': ('wide',),
        }),
        ('Visuals & Experience', {
            'fields': ('profile_image', 'cv'),
            'description': 'This image and CV will be accessible from your about and home sections.'
        }),
        ('Social Connections', {
            'fields': ('github_link', 'linkedin_link', 'facebook_link', 'twitter_link', 'instagram_link', 'whatsapp_link'),
            'description': 'Links to your professional and social profiles.'
        }),
    )

    def has_image(self, obj):
        return bool(obj.profile_image)
    has_image.boolean = True
    has_image.short_description = "Photo Uploaded"

    # Singleton-style: allow only one record to be created
    def has_add_permission(self, request):
        return not Bio.objects.exists()

    class Media:
        css = {
            'all': ('myportfolio_App/css/admin_custom.css',)
        }
