from .models import UserProfile


def get_avatar(backend, strategy, details, response, user=None, *args, **kwargs):
    url = None
    if backend.name == "google-oauth2":
        url = response.get("picture")
    if url:
        profile, was_created = UserProfile.objects.get_or_create(user=user)
        profile.avatar = url
        profile.save()
