from django.urls import path
from . import views
from . import api_views
 
urlpatterns = [
    # ── Django HTML views (Week 7) ──
    path("",                 views.TaskListView.as_view(),   name="task_list"),
    path("<int:pk>/",        views.TaskDetailView.as_view(), name="task_detail"),
    path("create/",          views.TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/edit/",   views.TaskUpdateView.as_view(), name="task_edit"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
 
    # ── DRF API views (Week 9) ──
    path("api/tasks/",          api_views.TaskListAPIView.as_view(),   name="api_task_list"),
    path("api/tasks/<int:pk>/", api_views.TaskDetailAPIView.as_view(), name="api_task_detail"),
]