from .models import Project, Review, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import Profile
from django.db.models import Q


def pagination_projects(request, projects, results):

    page = request.GET.get('page')

    # Show specific projects
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    # First visit on site
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    # Out of range or not existing site
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # Count of sites on menu
    left_side = (int(page) - 4)
    if left_side < 1:
        left_side = 1

    right_side = (int(page) + 5)
    if right_side > paginator.num_pages:
        right_side = paginator.num_pages

    pages_range = range(left_side, right_side+1)

    return pages_range, projects


def search_projects(request):
    find_projects = ''

    # After search
    if request.GET.get('find_projects'):
        find_projects = request.GET.get('find_projects')
    print(f'Find project: {find_projects}')

    tags = Tag.objects.filter(name__icontains=find_projects)
    profile = Profile.objects.filter(full_name__icontains=find_projects)
    print(profile)

    # Global filter
    # distinct() avoid duplicate objects in technology__in=tags because if find one of all tags, render new object in projects.
    projects = Project.objects.distinct().filter(
        Q(title__icontains=find_projects) |
        Q(description__icontains=find_projects) |
        Q(tags__in=tags) |
        Q(owner__in=profile),
    )

    return projects, find_projects
