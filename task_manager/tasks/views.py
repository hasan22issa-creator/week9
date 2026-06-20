from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import TaskForm
 
 
# Every view here has @login_required
# If the user is not logged in, Django sends them to /accounts/login/
# request.user = the person who is currently logged in
 
 
# ── TASK LIST ──
@login_required
def task_list(request):
    # Only show tasks that belong to the logged-in user
    tasks = Task.objects.filter(owner=request.user)
 
    # You can also filter by status using a URL parameter
    # e.g. /tasks/?status=open
    status_filter = request.GET.get("status")
    if status_filter:
        tasks = tasks.filter(status=status_filter)
 
    # render() takes 3 things:
    # 1. the request
    # 2. the template to use
    # 3. a dictionary of data to pass to the template (context)
    return render(request, "tasks/task_list.html", {
        "tasks": tasks,
        "status_filter": status_filter,
    })
 
 
# ── TASK DETAIL ──
@login_required
def task_detail(request, pk):
    # get_object_or_404 = get the task, or show a 404 page if it doesn't exist
    # We also check owner=request.user so users can't see each other's tasks
    task = get_object_or_404(Task, pk=pk, owner=request.user)
 
    return render(request, "tasks/task_detail.html", {
        "task": task,
    })
 
 
# ── CREATE TASK ──
@login_required
def task_create(request):
    # When the user visits /tasks/create/ for the first time = GET request
    # Show them an empty form
 
    # When they fill it in and click submit = POST request
    # Save the task and redirect to the list
 
    if request.method == "POST":
        # request.POST contains all the form data the user submitted
        form = TaskForm(request.POST)
        if form.is_valid():
            # Don't save to DB yet — we need to set the owner first
            task = form.save(commit=False)
            task.owner = request.user  # set the owner to the logged-in user
            task.save()
            return redirect("task_list")  # go back to the list after saving
    else:
        # GET request — show an empty form
        form = TaskForm()
 
    return render(request, "tasks/task_form.html", {
        "form": form,
        "action": "Create",  # used in the template to say "Create Task"
    })
 
 
# ── EDIT TASK ──
@login_required
def task_edit(request, pk):
    # Same idea as create, but we pre-fill the form with existing data
    task = get_object_or_404(Task, pk=pk, owner=request.user)
 
    if request.method == "POST":
        # instance=task tells Django which task to update
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail", pk=task.pk)
    else:
        # Pre-fill form with the task's current data
        form = TaskForm(instance=task)
 
    return render(request, "tasks/task_form.html", {
        "form": form,
        "action": "Edit",
        "task": task,
    })
 
 
# ── DELETE TASK ──
@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, owner=request.user)
 
    if request.method == "POST":
        # Only actually delete when the user confirms (POST)
        task.delete()
        return redirect("task_list")
 
    # GET request — show a confirmation page first
    return render(request, "tasks/task_confirm_delete.html", {
        "task": task,
    })