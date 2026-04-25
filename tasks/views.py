from rest_framework import viewsets
from .models import Project, Task, Comment
from .serializers import ProjectSerializer, TaskSerializer, CommentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import ProjectOwnerOrReadOnly, TaskPermission, CommentPermission
from django.db import models



class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [ProjectOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Project.objects.filter(participants=user)
        return Project.objects.none()



class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [TaskPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["project", "status", "priority", "executor", "deadline"]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Task.objects.none()
        return Task.objects.filter(
            models.Q(project__created_by=user) |
            models.Q(creator=user) |
            models.Q(executor=user)
        ).distinct()



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Comment.objects.none()
        return Comment.objects.filter(
            models.Q(task_project__created_by=user) |
            models.Q(task__creator=user) |
            models.Q(task__executor=user)
        ).distinct()
