from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Actor(models.Model):
    name = models.CharField(max_length=100, db_index=True)


class Genre(models.Model):
    title = models.CharField(max_length=100, db_index=True)


class Director(models.Model):
    name = models.CharField(max_length=100, db_index=True)


class Movie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)
    year = models.SmallIntegerField()
    release = models.CharField(max_length=100)
    directors = models.ManyToManyField(Director)
    genres = models.ManyToManyField(Genre)
    actors = models.ManyToManyField(Actor)
    poster_url = models.TextField()
