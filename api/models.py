from django.db import models

from .validators import validate_price


class Book(models.Model):
    name = models.CharField(max_length=20)
    title = models.CharField(max_length=30, blank=True, null=True)
    author = models.CharField(max_length=30)
    description = models.TextField(max_length=512, blank=True, null=True)
    price = models.IntegerField(validators=[validate_price])

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return self.name


class Profile(models.Model):
    column_name = models.CharField(unique=True, editable=False, max_length=20)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ["column_name"]

    def __str__(self):
        return self.column_name
