from rest_framework import generics, status
from .serializers import LoginSerializer, RegisterSerializer
from rest_framework.response import Response
from user.models import User
from user.serializers import DetailUserSerializer
from knox.models import AuthToken

class Login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Authenticate through username or email and password
        Returns current user and token
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        context = {
            "user": DetailUserSerializer(user, many=False, context={'request': request}).data,
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(context, status=status.HTTP_200_OK)

class Register(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        """
        Register with email, username and password.
        Adding profile picture is optional.
        Returns authenticated user with token if form is correct.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        context = {
            "user": DetailUserSerializer(user, many=False, context={'request': request}).data,
            "token": AuthToken.objects.create(user)[1]
        }
        return Response(context, status=status.HTTP_200_OK)