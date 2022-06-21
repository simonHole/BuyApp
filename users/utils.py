from turtle import right
from .models import Profile, Technology
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagination_profiles(request, profiles, results):

    page = request.GET.get('page')

    # Show specific profiles
    paginator = Paginator(profiles, results)

    try:
        profiles = paginator.page(page)
    # First visit on site
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    # Out of range or not existing site
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # Count of sites on menu
    left_side = (int(page) - 1)
    if left_side < 1:
        left_side = 1

    right_side = (int(page) + 1)
    if right_side > paginator.num_pages:
        right_side = paginator.num_pages

    pages_range = range(left_side, right_side+1)

    return pages_range, profiles


def search_profiles(request):
    # Show all profiles
    find_profile = ''

    # After search
    if request.GET.get('find_profile'):
        find_profile = request.GET.get('find_profile')
    print('Find user:', find_profile)

    technologies = Technology.objects.filter(name__icontains=find_profile)

    off_superuser = Profile.objects.filter(user__is_superuser=False)

    # Global filter
    # distinct() avoid duplicate objects in technology__in=technologies because if find one of all technologies, render new object in profiles.
    profiles = off_superuser.distinct().filter(
        Q(full_name__icontains=find_profile) |
        Q(status__icontains=find_profile) |
        Q(technology__in=technologies))

    print(len(profiles))

    return profiles, find_profile
