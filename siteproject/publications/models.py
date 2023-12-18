from django.db import models
from django.utils import timezone


class Publication(models.Model):
    title = models.CharField(max_length=50)
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    publication_date = models.DateField(default=timezone.now)
    photo = models.ImageField(upload_to='publication_photos/', null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def get_absolute_url(self):
        return f'/publications/{self.id}/'
