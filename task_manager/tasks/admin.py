from django.contrib import admin
from .models import Task
 
 
# Registering the model means it shows up in the Django admin panel at /admin
# The TaskAdmin class controls how it looks and what you can do there
 
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
 
    # Columns shown in the task list view
    list_display = ["title", "status", "owner", "created_at"]
 
    # Clickable filters on the right sidebar
    list_filter = ["status", "owner"]
 
    # Search box — searches these fields
    search_fields = ["title", "description"]
 
    # Makes status editable directly in the list without opening each task
    list_editable = ["status"]
 
    # Fields shown when you open a task to edit it
    fields = ["title", "description", "status", "owner"]