from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Task
from .serializers import TaskSerializer
 
 
# APIView is the DRF version of Django's View class
# Instead of render() it uses Response() which returns JSON
# IsAuthenticated = only logged-in users with a valid token can access this
 
# ── TASK LIST + CREATE ──
class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get(self, request):
        # GET /api/tasks/ — return all tasks for this user
        tasks = Task.objects.filter(owner=request.user)
 
        # Optional filter: GET /api/tasks/?status=open
        status_filter = request.query_params.get("status")
        if status_filter:
            tasks = tasks.filter(status=status_filter)
 
        # many=True means "serialize a LIST of tasks, not just one"
        serializer = TaskSerializer(tasks, many=True)
 
        # Response() automatically converts to JSON
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def post(self, request):
        # POST /api/tasks/ — create a new task
        # request.data = the JSON body the client sent
        serializer = TaskSerializer(data=request.data)
 
        if serializer.is_valid():
            # Save the task and set the owner automatically
            serializer.save(owner=request.user)
            # 201 CREATED — not 200, because we made something new
            return Response(serializer.data, status=status.HTTP_201_CREATED)
 
        # If validation failed, return the errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
 
# ── SINGLE TASK: GET, UPDATE, DELETE ──
class TaskDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
 
    def get_object(self, pk, user):
        # Helper method — get the task or return 404
        # We check owner=user so users can't access each other's tasks
        return get_object_or_404(Task, pk=pk, owner=user)
 
    def get(self, request, pk):
        # GET /api/tasks/1/ — return one task
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
 
    def put(self, request, pk):
        # PUT /api/tasks/1/ — replace the whole task
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def patch(self, request, pk):
        # PATCH /api/tasks/1/ — update only some fields
        # partial=True means not all fields are required
        task = self.get_object(pk, request.user)
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def delete(self, request, pk):
        # DELETE /api/tasks/1/ — delete a task
        task = self.get_object(pk, request.user)
        task.delete()
        # 204 NO CONTENT — deleted successfully, nothing to return
        return Response(status=status.HTTP_204_NO_CONTENT)