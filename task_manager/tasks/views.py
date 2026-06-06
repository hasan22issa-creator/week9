from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .models import Task
 
 
# @login_required means:

# "if the user is not logged in, send them to the login page"

# "if they are logged in, let them through"

# It's the same @log_call decorator idea from Week 3 — wraps the function
 
@login_required

def task_list(request):

    # request.user = the person who is currently logged in

    # We only show tasks that belong to THIS user — not everyone's tasks

    tasks = Task.objects.filter(owner=request.user)
 
    # For now just print to confirm it works

    # In Week 7 we'll render a real HTML page

    print(f"Logged in as: {request.user.username}")

    print(f"Their tasks: {tasks}")
 
    # render() takes the request, a template, and data to pass to it

    return render(request, "tasks/task_list.html", {

        "tasks": tasks,

        "user": request.user,

    })
 