from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Link(models.Model):
    url = models.URLField(unique=True)
    short_url = models.CharField(max_length=30, unique=True, db_index=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.short_url} -> {self.full_url}, {self.clicks} clicks'