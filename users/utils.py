from .models import Profile, Technology
from django.db.models import Q


def search_profiles(request):
    # Show all profiles
    find_profile = ''

    # After search
    if request.GET.get('find_profile'):
        find_profile = request.GET.get('find_profile')
    print('Find user:', find_profile)

    technologies = Technology.objects.filter(name__icontains=find_profile)

    # Global filter
    # distinct() avoid duplicate objects in technology__in=technologies because if find one of all technologies, render new object in profiles.
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=find_profile) |
        Q(surname__icontains=find_profile) |
        Q(status__icontains=find_profile) |
        Q(technology__in=technologies))

    return profiles, find_profile
