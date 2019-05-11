from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from taskapp.forms import LoginForm, ProjectForm, TaskForm
from taskapp.models import Project, Task, Staff


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form['login'].value(), password=form['password'].value())
            if user is None:
                form = LoginForm()
                return render(request, 'tasks/login.html', context={'form': form, 'error_message': 'Login or password '
                                                                                                   'are incorrect'})
            else:
                login(request, user)
                return redirect('tasks:index')
    else:
        form = LoginForm()
    return render(request, 'tasks/login.html', context={'form': form})


@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return redirect('tasks:index')

@login_required(login_url='/login/')
def index(request):
    headings = Project.objects.all()
    data = {cat: Task.objects.filter(project=cat.pk) for cat in headings}
    columns = [data[heading] for heading in headings]
    columns = list(map(lambda x: list(x), columns))
    if columns:
        max_len = len(max(columns, key=len))
        for col in columns:
            col += [None, ] * (max_len - len(col))
        rows = [[col[i] for col in columns] for i in range(max_len)]
    else:
        rows = None
    return render(request, 'tasks/bootstrap-index.html', context={
        'headings': headings,
        'rows': rows,
    })


@login_required(login_url='/login/')
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            new_project = Project(name=form['name'].value())
            new_project.save()
            return HttpResponseRedirect('/')
    else:
        form = ProjectForm()
    return render(request, 'tasks/general_form.html', context={'form': form, 'string': 'New project'})


@login_required(login_url='/login/')
def project_detail(request, id):
    project = get_object_or_404(Project, pk=id)
    return render(request, 'tasks/project_detail.html', context={'project': project})


@login_required(login_url='/login/')
def project_edit(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = ProjectForm(request.POST, initial={'name': project.name})
        if form.is_valid():
            project.name = form['name'].value()
            project.save()
            return redirect('tasks:project_detail', id=project.pk)
    else:
        form = ProjectForm(initial={'name': project.name})
    return render(request, 'tasks/general_form.html', context={'form': form, 'string': 'Edit project'})


@login_required(login_url='/login/')
def project_delete(request, id):
    project = get_object_or_404(Project, pk=id)
    project.delete()
    return redirect('tasks:index')


@login_required(login_url='/login/')
def add_task(request, id):
    project = get_object_or_404(Project, pk=id)
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES)
        if form.is_valid():
            new_staff_pic = get_object_or_404(Staff, pk=form['staff_pic'].value())
            new_task = Task(name=form['name'].value(), project=project,
                            description=form['description'].value(),
                            start_date=form['start_date'].value(),
                            due_date=form['due_date'].value(),
                            deliverable=form['deliverable'].value(),
                            staff_pic=new_staff_pic,
                            status = form['status'].value()
                            )
            new_task.save()
            return HttpResponseRedirect('/')
    else:
        form = TaskForm()
    return render(request, 'tasks/general_form.html', context={'form': form, 'string': 'New task'})