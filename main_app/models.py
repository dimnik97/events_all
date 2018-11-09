from django.contrib.auth.models import User
from django.db import models


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, max_length=1500)
    rating = models.IntegerField(null=True, blank=True, default=None)

    def __str__(self):
        return str(self.description) + " " + str(self.user.id)

    class Meta:
        verbose_name = 'Форма обратной связи'
        verbose_name_plural = 'Форма обратной связи'
