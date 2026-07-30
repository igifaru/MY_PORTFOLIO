import json

from django.conf import settings

from .models import Bio


def seo_schema(request):
    """Provides a valid JSON-LD Person schema string and the Google Search Console
    verification token (if set) for base.html's <head>."""
    context = {'google_site_verification': settings.GOOGLE_SITE_VERIFICATION}

    bio = Bio.objects.first()
    if not bio:
        context['person_schema_json'] = '{}'
        return context

    schema = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": bio.full_name,
        "jobTitle": bio.about_role,
        "url": request.build_absolute_uri('/'),
    }

    if bio.profile_image:
        schema["image"] = request.build_absolute_uri(bio.profile_image.url)

    same_as = [url for url in [
        bio.github_link,
        bio.linkedin_link,
        bio.twitter_link,
        bio.facebook_link,
        bio.instagram_link,
    ] if url]
    if same_as:
        schema["sameAs"] = same_as

    context['person_schema_json'] = json.dumps(schema)
    return context
