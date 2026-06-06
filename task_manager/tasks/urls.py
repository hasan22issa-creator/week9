from django.urls import path
from . import views
 
urlpatterns = [
    # We'll add real task pages in Week 7
    # For now just one simple protected page to test login
    path("", views.task_list, name="task_list"),
]