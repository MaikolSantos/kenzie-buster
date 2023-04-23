from rest_framework.views import APIView, Request, Response, status
from .serializers import MovieSerializer, MovieOrderSerializer
from .models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination


class IsAllowed(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser and request.user.is_authenticated


class MovieView(APIView, PageNumberPagination):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowed]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        result_page = self.paginate_queryset(movies, request)

        serializer = MovieSerializer(result_page, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class MovieDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowed]

    def get(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        serializer = MovieSerializer(movie)

        return Response(serializer.data, status.HTTP_200_OK)

    def delete(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        movie.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, movie_id: int) -> Response:
        movie = get_object_or_404(Movie, id=movie_id)

        user = request.user

        serializer = MovieOrderSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(movie=movie, user=user)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
