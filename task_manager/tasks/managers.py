from django.db import models
 
 
# A custom manager adds extra query shortcuts to our model.
# Instead of writing Task.objects.filter(status="open") every time,
# we can just write Task.objects.open()
 
class TaskManager(models.Manager):
 
    def open(self):
        # Returns all tasks with status "open"
        return self.filter(status="open")
 
    def in_progress(self):
        # Returns all tasks currently being worked on
        return self.filter(status="in-progress")
 
    def done(self):
        # Returns all completed tasks
        return self.filter(status="done")
 
    def for_user(self, user):
        # Returns all tasks belonging to a specific user
        return self.filter(owner=user)