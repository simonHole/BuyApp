from unittest import result
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from .utils import search_projects, pagination_projects

# Create your views here.


def project(request, pk):
    project = Project.objects.get(id=pk)
    owner_full_name = project.owner.user.first_name + \
        ' ' + project.owner.user.last_name

    context = {
        'project': project,
        'tags': project.tags.all(),
        'owner_full_name': owner_full_name,
    }
    return render(request, 'projects/single-project.html', context)


def projects(request):

    projects, find_projects = search_projects(request)
    pages_range, projects = pagination_projects(request, projects, 6)

    context = {
        'projects': projects,
        'find_projects': find_projects,
        'pages_range': pages_range
    }
    return render(request, 'projects/projects.html', context)

# @login_required check if user is logged in, if not redirect to login page


@login_required(login_url="login")
# Create and add new project to database
def create_project(request):
    profile = request.user.profile
    method = 'create'
    form = ProjectForm()

    if request.method == 'POST':
        # request.POST -> send data by POST method and request.FILES allow send the files by POST method, remember about
        # enctype

        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            messages.success(
                request, f"Nowy projekt o nazwie '{project.title}' utworzono pomyślnie.")
            project.save()
            return redirect('account')

    context = {'form': form, 'method': method}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
# Update exist project
def update_project(request, pk):
    profile = request.user.profile
    method = 'update'
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Edycja projektu {project.title} przebiegła pomyślnie.")
            return redirect('projects')

    context = {'form': form, 'method': method}
    return render(request, 'projects/project_form.html', context)


@login_required(login_url="login")
# Delete known technology from profile
def delete_project(request, pk):
    delete_type = "Projekt"
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Usuwanie projektu przebiegło pomyślnie.')
        return redirect('account')
    context = {'object': project, 'delete_type': delete_type}
    return render(request, 'delete-template.html', context)
