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
        serializer = UserSerializer(q, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(APIView):
    def get(self, request, uuid):
        try:
            user = User.objects.get(uuid=uuid)
        except:
            return Response({"Status": "User does not exist"}, status=HTTP_400_BAD_REQUEST)
        user_serializer = UserSerializer(user, many=False, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)