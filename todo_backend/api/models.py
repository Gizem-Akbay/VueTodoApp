from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="todo_user")
    title = models.CharField(max_length=256)
    content = models.TextField()
    status = models.BooleanField(default = False)
    image = models.ImageField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)
    assigned_users = models.ManyToManyField(User, related_name="todo_users")

class Label(models.Model):
    todo = models.ForeignKey(Todo, on_delete = models.CASCADE, related_name="label_todo")
    name = models.CharField(max_length=256)
    color = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name="label_user")
