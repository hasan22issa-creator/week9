from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views
from . import viewsets
 
# The Router automatically creates all URL patterns for a ViewSet
# One line replaces 5 separate URL definitions
 
router = DefaultRouter()
router.register(r"api/tasks", viewsets.TaskViewSet, basename="task")
 
urlpatterns = [
    # ── Django HTML views (Week 7) ──
    path("",                 views.TaskListView.as_view(),   name="task_list"),
    path("<int:pk>/",        views.TaskDetailView.as_view(), name="task_detail"),
    path("create/",          views.TaskCreateView.as_view(), name="task_create"),
    path("<int:pk>/edit/",   views.TaskUpdateView.as_view(), name="task_edit"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task_delete"),
 
    # ── ViewSet API (Week 10) — router generates these automatically ──
    # GET    /tasks/api/tasks/           → list
    # POST   /tasks/api/tasks/           → create
    # GET    /tasks/api/tasks/1/         → retrieve
    # PUT    /tasks/api/tasks/1/         → update
    # PATCH  /tasks/api/tasks/1/         → partial update
    # DELETE /tasks/api/tasks/1/         → destroy
    # POST   /tasks/api/tasks/1/complete/ → custom complete action
    # GET    /tasks/api/tasks/open/       → custom open tasks action
    path("", include(router.urls)),
]