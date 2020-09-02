from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User, Follow
from user.serializers import UserSerializer, DetailUserSerializer
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)

class CurrentUser(APIView):
    def get(self, request, format=None):
        """
        Return serialized current user.
        """
        if request.user:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, uuid):
        try:
            user = User.objects.get(uuid=uuid)
        except:
            return Response({"Status": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = DetailUserSerializer(user, many=False, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, uuid):
        user_from = request.user
        user_to = User.objects.get(uuid=uuid)
        if user_from != user_to:
            if user_from not in user_to.followers.all():
                Follow.objects.create(user_from=user_from, user_to=user_to)
                return Response({"Status": "{} followed {}".format(user_from.username, user_to.username)}, status=status.HTTP_200_OK)
            else:
                Follow.objects.get(user_from=user_from, user_to=user_to).delete()
                return Response({"Status": "{} unfollowed {}".format(user_from.username, user_to.username)}, status=status.HTTP_200_OK)
        return Response({"Status": "Cant follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# # @permission_classes([IsAuthenticated])
# def follow_user(request, uuid):
#     if request.method == "POST":
#         user_from = request.user
#         user_to = User.objects.get(uuid=uuid)
#         if user_from != user_to:
#             Follow.objects.create(user_from=user_from, user_to=user_to)
#             return Response({"Status": "{} followed {}".format(user_from.username, user_to.username)}, status=status.HTTP_200_OK)
#         return Response({"Status": "Cant follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

