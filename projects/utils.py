from .models import Project, Review, Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import Profile
from django.db.models import Q


def pagination_projects(request, projects, results):

    page = request.GET.get('page')
    paginator = Paginator(projects, results)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

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

    if request.GET.get('find_projects'):
        find_projects = request.GET.get('find_projects')
    print(f'Find project: {find_projects}')

    tags = Tag.objects.filter(name__icontains=find_projects)
    profile = Profile.objects.filter(full_name__icontains=find_projects)
    print(profile)

    projects = Project.objects.distinct().filter(
        Q(title__icontains=find_projects) |
        Q(description__icontains=find_projects) |
        Q(tags__in=tags) |
        Q(owner__in=profile),
    )

    return projects, find_projects
