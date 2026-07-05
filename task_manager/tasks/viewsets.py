from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwner
 
 
# A ViewSet combines List, Create, Retrieve, Update, Delete into ONE class
# Instead of writing 5 separate views, you write one ViewSet
# The Router (in urls.py) automatically creates all the URL patterns
 
# Without ViewSet (Week 9 style):
#   TaskListAPIView   → GET /api/tasks/     POST /api/tasks/
#   TaskDetailAPIView → GET /api/tasks/1/   PUT  /api/tasks/1/   DELETE /api/tasks/1/
 
# With ViewSet (Week 10 style):
#   TaskViewSet → handles ALL of the above automatically
 
class TaskViewSet(viewsets.ModelViewSet):
 
    serializer_class = TaskSerializer
 
    # IsAuthenticated = must be logged in with a valid JWT token
    # IsOwner = must own the specific task being accessed
    permission_classes = [IsAuthenticated, IsOwner]
 
    # filter_backends allows searching/ordering via query params
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at", "status", "title"]
    ordering = ["-created_at"]  # default: newest first
 
    def get_queryset(self):
        # Always filter by the logged-in user first
        queryset = Task.objects.filter(owner=self.request.user)
 
        # Optional filter: GET /api/tasks/?status=open
        status_filter = self.request.query_params.get("status")
        if status_filter:
            queryset = queryset.filter(status=status_filter)
 
        return queryset
 
    def perform_create(self, serializer):
        # Called when POST /api/tasks/ is made
        # Automatically set the owner to the logged-in user
        serializer.save(owner=self.request.user)
 
    # ── CUSTOM ACTION ──
    # @action lets you add extra endpoints beyond the standard CRUD
    # This creates: POST /api/tasks/1/complete/
    @action(detail=True, methods=["post"], url_path="complete")
    def complete(self, request, pk=None):
        task = self.get_object()  # gets task and checks IsOwner automatically
        task.complete()           # our model method from Week 4
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    # This creates: GET /api/tasks/open/
    @action(detail=False, methods=["get"], url_path="open")
    def open_tasks(self, request):
        tasks = self.get_queryset().filter(status="open")
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)