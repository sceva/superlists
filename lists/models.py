from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models


class List(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id])


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List)

    class Meta:
        ordering = ('id',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text