import django_filters
from rest_framework import filters

from .models import Movie, Director, Actor, Genre


class MovieFilter(django_filters.FilterSet):
    year = django_filters.NumberFilter(field_name='year')
    year_min = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    year_max = django_filters.NumberFilter(field_name='year', lookup_expr='lte')

    directors = django_filters.CharFilter(method='filter_directors')
    actors = django_filters.CharFilter(method='filter_actors')
    genres = django_filters.CharFilter(method='filter_genres')

    class Meta:
        model = Movie
        fields = ['year', 'directors', 'actors']
        ordering_fields = ['year']

    def filter_directors(self, queryset, name, value):
        director_names = value.split(',')
        directors = Director.objects.filter(name__in=director_names)
        return queryset.filter(directors__in=directors)

    def filter_actors(self, queryset, name, value):
        actor_names = value.split(',')
        actors = Actor.objects.filter(name__in=actor_names)
        return queryset.filter(actors__in=actors)

    def filter_genres(self, queryset, name, value):
        genre_title = value.split(',')
        genres = Genre.objects.filter(title__in=genre_title)
        return queryset.filter(genres__in=genres)


class CustomSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        if request.query_params.get('title_only'):
            return ['title']
        return super().get_search_fields(view, request)