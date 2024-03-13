from django.urls import path
from .views import OMDbMovieViewSet, MovieStrViewSet, MovieViewSet
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'movie_by_str', MovieStrViewSet, basename='movie_by_str')
router.register(r'movie', MovieViewSet, basename='movie')

urlpatterns = [
    path('omdb/create/', OMDbMovieViewSet.as_view({'post': 'create'}), name='omdb_movie-create'),
    path('omdb/update/<str:title>/', OMDbMovieViewSet.as_view({'put': 'update'}), name='update_omdb_movie_by_title'),
]

urlpatterns += router.urls
# urlpatterns = [
#     path('create/', OMDbMovieViewSet.as_view({'post': 'create'}), name='movie-create'),
#     path('update/<str:title>/', OMDbMovieViewSet.as_view({'put': 'update'}), name='update_movie_by_title'),
#
#     path('create2/', CUDMovieStrViewSet.as_view({'post': 'create'}), name='movie-create2'),
#     path('update2/<str:title>/', CUDMovieStrViewSet.as_view({'put': 'update'}), name='update_movie_by_title2'),
#     path('delete2/<str:title>/', CUDMovieStrViewSet.as_view({'delete': 'destroy'}, name='delete_movie_by_title2'))
#
#
# ]
