from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="owner_for_projects"
    )
    participants = models.ManyToManyField(
        User,
        related_name="part_of_projects"
    )
    created_at = models.DateTimeField(auto_now_add=True)



class Task(models.Model):
    title = models.CharField(max_length=100)
    project = models.ForeignKey(
        Project,
        on_delete=models.PROTECT,
        related_name="tasks"
    )
    description = models.TextField(blank=True)
    priority = models.IntegerField(choices=[
        (1, "Критический"),
        (2, "Высокий"),
        (3, "Средний"),
        (4, "Низкий"),
    ], default=3)
    status = models.CharField(
        max_length=15,
        choices=[
        ("new", "Новая"),
        ("in_progress", "В разработке"),
        ("done", "Выполнена"),
    ],
        default="new")
    creator = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="announced_tasks"
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="executable_tasks"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)



class Comment(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="comments"
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        author_name = self.author.username if self.author else "Удалённый пользователь"
        return f"Comment by {author_name} on {self.task.title}"

