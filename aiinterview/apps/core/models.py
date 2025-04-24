from django.db import models
from django.utils.text import slugify


class Timestampable(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Slugable(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=300, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SlugableUnique(models.Model):
    name = models.CharField(max_length=250, unique=True)
    slug = models.SlugField(max_length=300, blank=True, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
