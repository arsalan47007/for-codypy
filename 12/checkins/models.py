from django.db import models
from django.contrib.auth.models import User


class MoodEntry(models.Model):
    score = models.IntegerField()
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.CharField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.score} - {self.created_at}"
