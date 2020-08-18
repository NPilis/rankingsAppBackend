from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserSerializer
from rest_framework import status, generics
from rest_framework.permissions import AllowAny

class CurrentUser(APIView):
    def get(self, request, format=None):
        """
        Return serialized current user.
        """
        if request.user:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UsersList(APIView):
    def get(self, request, *args, **kwargs):
        q = User.objects.all()
        serializer = UserSerializer(q, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer