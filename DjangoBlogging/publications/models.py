from django.db import models
from django.contrib.auth.models import User


# Clase categoria de una publicacion del blog
class Category(models.Model):

    name = models.CharField(max_length=150)

    def __str__(self):
        return '{0}'.format(self.name)


# Clase publicacion del blog
class Publication(models.Model):

    publisher = models.ForeignKey(User, on_delete=models.CASCADE, related_name='publications')
    title = models.CharField(max_length=150)
    introductory_text = models.CharField(max_length=300)
    body = models.TextField()
    image = models.FileField(null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, related_name='publications')
    published = models.BooleanField(default=True)

    def __str__(self):
        return '{0}'.format(self.title)