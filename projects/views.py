from unittest import result
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib import messages
from .models import *
from .forms import *
from .utils import search_projects, pagination_projects

from payments import get_payment_model

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded


def project(request, pk):
    project = Project.objects.get(id=pk)
    owner_full_name = project.owner.user.first_name + \
        ' ' + project.owner.user.last_name
    review_form = ReviewForm

    if request.method == 'POST':
        review_form = ReviewForm(request.POST)
        review = review_form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()

        project.get_vote_total

        messages.success(request, 'Twój komentarz został dodany pomyślnie')
        return redirect('project', pk=project.id)

    context = {
        'project': project,
        'tags': project.tags.all(),
        'owner_full_name': owner_full_name,
        'review_form': review_form
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


@login_required(login_url="login")
def create_project(request):
    profile = request.user.profile
    method = 'create'
    form = ProjectForm()

    if request.method == 'POST':
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


@login_required(login_url="login")
def buy_project(request, pk):
    project = Project.objects.get(id=pk)
    get_payment = get_payment_model()

    first_name, last_name = request.user.profile.full_name.split()

    payment = get_payment.objects.create(
        variant='dotpay',  # this is the variant from PAYMENT_VARIANTS
        description='Paypal purchase',
        total=Decimal(project.price),
        tax=Decimal(20),
        currency='PLN',
        delivery=Decimal(0),
        billing_first_name=request.user.first_name,
        billing_last_name=request.user.last_name,
        billing_address_1='aleja Tysiąclecia Państwa Polskiego 4',
        billing_address_2='',
        billing_city='Kielce',
        billing_postcode='25-001',
        billing_country_code='PL',
        billing_country_area='swietokrzyskie',
        customer_ip_address='127.0.0.1',
    )
    print(payment)

    payment.save()

    context = {
        'project': project,
        'id': payment.id,
    }

    return render(request, 'projects/buy-project.html', context)


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment}
    )
