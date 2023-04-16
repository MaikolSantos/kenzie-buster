from rest_framework.views import APIView, Request, Response, status
from .serializers import UserSerializer
from .models import User


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
    ...
