from django.db import models
from accounts.models   import User

# Create your models here.


class Movie(models.Model):
    title = models.CharField(max_length=100)
    movie_id = models.TextField()
    overview = models.TextField()
    poster_path = models.TextField(null=True)
    release_date = models.DateField(null=True)
    director = models.TextField()
    trailer_key = models.TextField(null=True)
    vote_average = models.TextField()
    users = models.ManyToManyField(User)