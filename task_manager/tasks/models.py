from django.db import models
from django.contrib.auth.models import User
from .managers import TaskManager
# This is our Task from Week 3 — but now Django manages it as a database table.
# Every field here becomes a column in the database.
# We don't need __init__ anymore — Django handles that automatically.
 
class Task(models.Model):
 
    # Status choices — instead of hardcoding strings everywhere,
    # we define them here once and reuse them.
    # Format is: (value stored in DB, human-readable label)
    STATUS_CHOICES = [
        ("open",        "Open"),
        ("in-progress", "In Progress"),
        ("done",        "Done"),
    ]
 
    # The actual fields (columns in the database table)
    title       = models.CharField(max_length=200)           # short text
    description = models.TextField(blank=True)               # long text, optional
    status      = models.CharField(
                      max_length=20,
                      choices=STATUS_CHOICES,
                      default="open"
                  )
    # ForeignKey = "each task belongs to one user, one user can have many tasks"
    # on_delete=CASCADE means: if the user is deleted, delete their tasks too
    owner       = models.ForeignKey(
                      User,
                      on_delete=models.CASCADE,
                      related_name="tasks"
                  )
    created_at  = models.DateTimeField(auto_now_add=True)    # set once when created
    updated_at  = models.DateTimeField(auto_now=True)        # updated every save
 
    # Custom manager — lets us do Task.objects.open() instead of
    # Task.objects.filter(status="open") every time
    objects = TaskManager()
 
    def __str__(self):
        # This is what shows up in the Django admin and shell
        # e.g.  "Fix login bug (open)"
        return f"{self.title} ({self.status})"
 
    def assign(self, user):
        # Assign this task to a different user and save immediately
        self.owner = user
        self.save()
 
    def complete(self):
        # Mark task as done and save
        self.status = "done"
        self.save()
 
    class Meta:
        # Default ordering: newest tasks first
        ordering = ["-created_at"]
        # Human-readable names in the Django admin
        verbose_name = "Task"
        verbose_name_plural = "Tasks"