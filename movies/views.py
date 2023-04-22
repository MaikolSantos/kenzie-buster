from rest_framework.views import APIView, Request, Response, status
from .serializers import MovieSerializer
from .models import Movie
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from users.models import User
from users.serializers import UserSerializer

from django.shortcuts import get_object_or_404


class IsAllowed(permissions.BasePermission):
    def has_permission(self, request: Request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_superuser and request.user.is_authenticated


class MovieView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAllowed]

    def get(self, request: Request) -> Response:
        movies = Movie.objects.all()

        serializer = MovieSerializer(movies, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = MovieSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = get_object_or_404(User, username=request.user)

        serializer_user = UserSerializer(user)

        user_email = {"added_by": serializer_user["email"].value}

        data = {**serializer.data, **user_email}

        return Response(data=data, status=status.HTTP_201_CREATED)


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
