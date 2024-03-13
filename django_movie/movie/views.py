from django.shortcuts import render
from rest_framework import mixins, status, viewsets, filters
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from django.db.models import Q

import requests
import logging

from .serializers import CreateByOMDbMovieSerializer, MovieSerializer
from .models import Movie
from .permissions import IsOwnerOfMovieOrStaffPermission
from .filters import MovieFilter, CustomSearchFilter
# Create your views here.


logger = logging.getLogger(__name__)


class OMDbMovieViewSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):

    lookup_field = 'title'

    serializer_class = CreateByOMDbMovieSerializer

    permission_classes = (IsAuthenticated, IsAdminUser,)

    permission_classes_by_action = {
        'create': [],
        'update': [IsOwnerOfMovieOrStaffPermission]
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [])]

    def get_queryset(self):
        # Возвращаем QuerySet всех фильмов
        return Movie.objects.all()

    @classmethod
    def make_url(cls, title_movie: str, year_movie: str, apikey: str):
        try:
            if year_movie == "":
                url = f"https://www.omdbapi.com/?t={title_movie}&apikey={apikey}"
            else:
                url = f"http://www.omdbapi.com/?t={title_movie}&y={year_movie}&apikey={apikey}"
            response = requests.get(url)
            response.raise_for_status()  # Вызываем исключение, если статус ответа не 200
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch data from OMDB API: {e}")
            return None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.movie_data = None

    def get_serializer_context(self):
        context = super().get_serializer_context()

        if self.movie_data is not None:
            context["user"] = self.request.user
            context["title"] = self.movie_data.get("Title", "")
            context["year"] = self.movie_data.get("Year", "")
            context["release"] = self.movie_data.get("Released", "")
            context["poster_url"] = self.movie_data.get("Poster", "")
            context["directors"] = self.movie_data.get("Director", "").split(", ")
            context["genres"] = self.movie_data.get("Genre", "").split(", ")
            context["actors"] = self.movie_data.get("Actors", "").split(", ")

        return context

    def create(self, request, *args, **kwargs):
        title_movie = request.data.get("title_movie", "")
        year_movie = request.data.get("year_movie", "")
        apikey = request.data.get("apikey", "")

        self.movie_data = self.make_url(title_movie, year_movie, apikey)

        return super().create(request, *args, **kwargs)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Получаем название фильма из параметров запроса
        title = self.kwargs.get('title')  # предполагается, что вы используете аргумент в URL

        try:
            # Поиск объекта Movie по названию
            obj = queryset.get(title=title)
            self.check_object_permissions(self.request, obj)

            return obj
        except Movie.DoesNotExist:
            raise NotFound("Movie not found")

    def update(self, request, *args, **kwargs):
        title_movie = request.data.get("title_movie", "")
        year_movie = request.data.get("year_movie", "")
        apikey = request.data.get("apikey", "")

        self.movie_data = self.make_url(title_movie, year_movie, apikey)

        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class MovieStrViewSet(mixins.CreateModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.RetrieveModelMixin,
                      GenericViewSet):

    serializer_class = MovieSerializer

    lookup_field = 'title'

    permission_classes = (IsAuthenticated, IsAdminUser,)

    permission_classes_by_action = {
        'update': [IsOwnerOfMovieOrStaffPermission],
        'destroy': [IsOwnerOfMovieOrStaffPermission]
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [])]

    def get_queryset(self):
        # Возвращаем QuerySet всех фильмов
        return Movie.objects.all()

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        # Получаем название фильма из параметров запроса
        title = self.kwargs.get('title')  # предполагается, что вы используете аргумент в URL

        try:
            # Поиск объекта Movie по названию
            obj = queryset.get(Q(title__iexact=title))
            self.check_object_permissions(self.request, obj)

            return obj
        except Movie.DoesNotExist:
            raise NotFound("Movie not found")


class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer

    queryset = Movie.objects.all()

    filterset_class = MovieFilter

    # filter_backends = [CustomSearchFilter]
    #
    # search_fields = ['title', 'year']

    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser,)

    permission_classes_by_action = {
        'update': [IsOwnerOfMovieOrStaffPermission],
        'destroy': [IsOwnerOfMovieOrStaffPermission]
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action.get(self.action, [])]

    def get_queryset(self):
        # Возвращаем QuerySet всех фильмов
        return Movie.objects.all()
