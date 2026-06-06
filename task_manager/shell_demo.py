#Task1
from tasks.models import Task
 
 
Task.objects.filter(title__icontains="bug")
 
 
from django.utils import timezone
import datetime
one_week_ago = timezone.now() - datetime.timedelta(days=7)
Task.objects.filter(created_at__gte=one_week_ago)
 
 
Task.objects.filter(status__in=["open", "in-progress"])
 
 
Task.objects.filter(description__isnull=False)
 
#Task2
from django.db.models import Q
 
 
# Q objects let you do OR and NOT too
 
 
Task.objects.filter(Q(status="open") | Q(status="in-progress"))
 
Task.objects.filter(Q(status="open") & Q(title__icontains="bug"))
 
Task.objects.filter(~Q(status="done"))
 
#Task3
from django.db.models import Count
 
 
Task.objects.aggregate(total=Count("id"))
 
Task.objects.aggregate(
    open_count=Count("id", filter=Q(status="open")),
    done_count=Count("id", filter=Q(status="done")),
)
 
 
from django.contrib.auth.models import User
users = User.objects.annotate(task_count=Count("tasks"))
for u in users:
    print(f"{u.username} has {u.task_count} tasks")
 
 
#Task4
from django.db import connection
 
# First reset the query log
from django.test.utils import reset_queries
import django
django.test.utils.setup_test_environment()
 
 
tasks = Task.objects.all()
for task in tasks:
    print(f"{task.title} — owner: {task.owner.username}")
 
print("Queries so far:", len(connection.queries))
 
 
tasks = Task.objects.select_related("owner").all()
for task in tasks:
    print(f"{task.title} — owner: {task.owner.username}")
 
print("Queries so far:", len(connection.queries))