from django import forms
from .models import Task
 
 
# A ModelForm automatically creates form fields from our model
# This is the same Task model we built — Django reads its fields
# and creates matching HTML inputs for us
 
class TaskForm(forms.ModelForm):
 
    class Meta:
        model = Task
        # Which fields to show in the form
        # We don't include owner — we set that automatically in the view
        fields = ["title", "description", "status"]
 
        # Make the form inputs look nicer with CSS classes
        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-input",
                "placeholder": "Enter task title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-input",
                "rows": 4,
                "placeholder": "Describe the task (optional)"
            }),
            "status": forms.Select(attrs={
                "class": "form-input"
            }),
        }