from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ["name"]


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ["title"]


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ["name"]


class CreateByOMDbMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["user", "title", "year", "release", "poster_url", "directors", "genres", "actors"]
        read_only_fields = ("user", "title", "year", "release", "poster_url", "directors", "genres", "actors")

    def validate(self, attrs):
        attrs = super().validate(attrs)
        attrs["user"] = self.context["user"]
        attrs["title"] = self.context["title"]
        attrs["year"] = self.context["year"]
        attrs["release"] = self.context["release"]
        attrs["poster_url"] = self.context["poster_url"]
        attrs["directors"] = self.context["directors"]
        attrs["genres"] = self.context["genres"]
        attrs["actors"] = self.context["actors"]
        return attrs

    def create(self, validated_data):
        title = self.context.get("title", "").lower()

        existing_movie = Movie.objects.filter(
            title__iexact=title,
            year=self.context.get("year", ""),
        ).first()

        if existing_movie:
            return existing_movie
        else:
            directors_data = self.context.get("directors", [])
            genres_data = self.context.get("genres", [])
            actors_data = self.context.get("actors", [])

            movie = Movie.objects.create(
                user=self.context.get("user", ""),
                title=self.context.get("title", ""),
                year=self.context.get("year", ""),
                release=self.context.get("release", ""),
                poster_url=self.context.get("poster_url", "")
            )

            for director_data in directors_data:
                director, _ = Director.objects.get_or_create(name=director_data)
                movie.directors.add(director)

            for genre_data in genres_data:
                genre, _ = Genre.objects.get_or_create(title=genre_data)
                movie.genres.add(genre)

            for actor_data in actors_data:
                actor, _ = Actor.objects.get_or_create(name=actor_data)
                movie.actors.add(actor)

            return movie

    def update(self, instance, validated_data):
        instance.user = instance.user
        instance.title = self.context.get("title", "")
        instance.year = self.context.get("year", "")
        instance.release = self.context.get("release", "")
        instance.poster_url = self.context.get("poster_url", "")

        directors_data = self.context.pop("directors", [])
        genres_data = self.context.pop("genres", [])
        actors_data = self.context.pop("actors", [])

        instance.directors.clear()
        instance.genres.clear()
        instance.actors.clear()

        for director_data in directors_data:
            director, _ = Director.objects.get_or_create(name=director_data)
            instance.directors.add(director)

        for genre_data in genres_data:
            genre, _ = Genre.objects.get_or_create(title=genre_data)
            instance.genres.add(genre)

        for actor_data in actors_data:
            actor, _ = Actor.objects.get_or_create(name=actor_data)
            instance.actors.add(actor)

        instance.save()
        return instance


class MovieSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    directors = DirectorSerializer(many=True)
    genres = GenreSerializer(many=True)
    actors = ActorSerializer(many=True)

    class Meta:
        model = Movie
        fields = "__all__"

    def create(self, validated_data):
        title = validated_data.get("title", "").lower()

        existing_movie = Movie.objects.filter(
            title__iexact=title,
            year=validated_data.get("year", ""),
        ).first()

        if existing_movie:
            return existing_movie
        else:
            directors_data = validated_data.pop('directors')
            genres_data = validated_data.pop('genres')
            actors_data = validated_data.pop('actors')

            movie = Movie.objects.create(**validated_data)

            for director_data in directors_data:
                director_name = director_data.get('name')  # Получаем имя режиссера из словаря
                director, _ = Director.objects.get_or_create(name=director_name)
                movie.directors.add(director)

            for genre_data in genres_data:
                genre_name = genre_data.get('title')
                genre, _ = Genre.objects.get_or_create(title=genre_name)
                movie.genres.add(genre)

            for actor_data in actors_data:
                actor_name = actor_data.get('name')
                actor, _ = Actor.objects.get_or_create(name=actor_name)
                movie.actors.add(actor)

            return movie

    def update(self, instance, validated_data):
        # Проверяем, если текущий пользователь не является суперпользователем
        # и пользователь в поле `user` не совпадает с текущим пользователем,
        # то мы не обновляем поле `user`
        if instance.user != self.context['request'].user:
            validated_data.pop('user', None)

        instance.user = instance.user
        instance.title = self.validated_data.get("title", "")
        instance.year = self.validated_data.get("year", "")
        instance.release = self.validated_data.get("release", "")
        instance.poster_url = self.validated_data.get("poster_url", "")

        directors_data = self.validated_data.pop("directors", [])
        genres_data = self.validated_data.pop("genres", [])
        actors_data = self.validated_data.pop("actors", [])

        instance.directors.clear()
        instance.genres.clear()
        instance.actors.clear()

        for director_data in directors_data:
            director_name = director_data.get('name')
            director, _ = Director.objects.get_or_create(name=director_name)
            instance.directors.add(director)

        for genre_data in genres_data:
            genre_name = genre_data.get('title')
            genre, _ = Genre.objects.get_or_create(title=genre_name)
            instance.genres.add(genre)

        for actor_data in actors_data:
            actor_name = actor_data.get('name')
            actor, _ = Actor.objects.get_or_create(name=actor_name)
            instance.actors.add(actor)

        instance.save()
        return instance


