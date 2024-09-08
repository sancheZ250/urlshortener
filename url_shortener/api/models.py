import hashlib
from django.db import models, IntegrityError, transaction
from django.contrib.auth.models import User

from django.db.models import F
import random

from url_shortener import settings

class LinkManager(models.Manager):

    def create_short_url(self, url, user):
        max_attempts = 5
        characters = settings.CHARACTERS
        base_length = settings.TOKEN_LENGTH

        for attempt in range(max_attempts):
            # Генерация случайной короткой ссылки
            short_url = ''.join(random.choices(characters, k=base_length + attempt))

            try:
                with transaction.atomic():
                    # Создание новой записи с уникальной короткой ссылкой
                    link = self.create(
                        url=url,
                        short_url=short_url,
                        user=user
                    )
                    return link
            except IntegrityError:
                # Если IntegrityError возникает, значит короткая ссылка не уникальна
                continue

        raise ValueError(f"Не удалось сгенерировать уникальную короткую ссылку для {url} после {max_attempts} попыток")
    
    def increment_clicks(self, short_url):
        self.filter(short_url=short_url).update(clicks=F('clicks') + 1)

# Models
class Link(models.Model):
    url = models.URLField(unique=True)
    short_url = models.CharField(max_length=20, unique=True, db_index=True, blank=True)
    clicks = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    objects = LinkManager()

    def __str__(self) -> str:
        return f'{self.url} -> {self.short_url}, {self.clicks} clicks'