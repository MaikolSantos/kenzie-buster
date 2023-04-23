from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404


class IsNotUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True


class UserView(APIView):
    def get(self, request: Request) -> Response:
        users = User.objects.all()

        serializer = UserSerializer(users, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        serializer = UserSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class UserDetailView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsNotUser | IsAdminUser]

    def get(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request=request, obj=user)

        serializer = UserSerializer(user)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request: Request, user_id: int) -> Response:
        user = get_object_or_404(User, id=user_id)

        self.check_object_permissions(request=request, obj=user)

        serializer = UserSerializer(user, request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(data=serializer.data, status=status.HTTP_200_OK)
