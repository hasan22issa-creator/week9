from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm
 
 
# LoginRequiredMixin = the class-based version of @login_required
# It must always be the FIRST thing in the class definition
 
# ── TASK LIST ──
class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "tasks/task_list.html"
    context_object_name = "tasks"  # what the template calls the list
 
    def get_queryset(self):
        # Only return tasks owned by the logged-in user
        # This method replaces Task.objects.filter(owner=request.user)
        queryset = Task.objects.filter(owner=self.request.user)
 
        # Optional status filter from URL: /tasks/?status=open
        status = self.request.GET.get("status")
        if status:
            queryset = queryset.filter(status=status)
        return queryset
 
    def get_context_data(self, **kwargs):
        # Add extra data to the template context
        context = super().get_context_data(**kwargs)
        context["status_filter"] = self.request.GET.get("status")
        return context
 
 
# ── TASK DETAIL ──
class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
 
    def get_queryset(self):
        # Only allow users to see their own tasks
        return Task.objects.filter(owner=self.request.user)
 
 
# ── CREATE TASK ──
class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
    success_url = reverse_lazy("task_list")  # where to go after saving
 
    def form_valid(self, form):
        # Set the owner before saving — same as commit=False from Week 7
        form.instance.owner = self.request.user
        return super().form_valid(form)
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Create"
        return context
 
 
# ── EDIT TASK ──
class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = "tasks/task_form.html"
 
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)
 
    def get_success_url(self):
        return reverse_lazy("task_detail", kwargs={"pk": self.object.pk})
 
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action"] = "Edit"
        return context
 
 
# ── DELETE TASK ──
class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "tasks/task_confirm_delete.html"
    success_url = reverse_lazy("task_list")
 
    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)