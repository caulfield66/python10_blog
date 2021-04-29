from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, primary_key=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(primary_key=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, primary_key=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(upload_to='posts/')

    def __str__(self):
        return self.title
