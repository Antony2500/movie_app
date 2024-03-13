from django.contrib import admin
from .models import Actor, Genre, Movie, Director

# Register your models here.


class MovieModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'id', 'title', 'year', 'release', 'display_director', 'display_genres', 'display_actors',
                    'poster_url')

    def display_director(self, obj):
        return ', '.join([director.name for director in obj.directors.all()])
    display_director.short_description = "Director"

    def display_genres(self, obj):
        return ', '.join([genre.title for genre in obj.genres.all()])
    display_genres.short_description = "Genres"

    def display_actors(self, obj):
        return ', '.join([actor.name for actor in obj.actors.all()])
    display_actors.short_description = "Actors"


admin.site.register(Movie, MovieModelAdmin)


@admin.register(Director)
class DirectorModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Actor)
class ActorModelAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]


@admin.register(Genre)
class GenreModelAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]