from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User, Follow
from user.serializers import UserSerializer, DetailUserSerializer, UpdateUserSerializer
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector, TrigramSimilarity

class CurrentUser(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DetailUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except:
            return Response({"Status": "User does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        user_serializer = DetailUserSerializer(user, many=False, context={'request': request})
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, username):
        """
        Create and delete follow 
        """
        user_from = request.user
        user_to = User.objects.get(username=username)
        if user_from != user_to:
            if user_from not in user_to.followers.all():
                Follow.objects.create(user_from=user_from, user_to=user_to)
                return Response({"Status": "{} followed {}".format(user_from.username, user_to.username)}, status=status.HTTP_200_OK)
            else:
                Follow.objects.get(user_from=user_from, user_to=user_to).delete()
                return Response({"Status": "{} unfollowed {}".format(user_from.username, user_to.username)}, status=status.HTTP_200_OK)
        return Response({"Status": "Cant follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

class EditProfile(generics.UpdateAPIView):
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user

class SearchUser(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def list(self, request, **kwargs):
        """
        Trigram based search on usernames by query passed in the url
        Returns list of ordered user by the largest similarity
        HTTP_204 if no results
        """
        search_query = kwargs["query"]
        if search_query:
            results = User.objects.annotate(
                similarity=TrigramSimilarity('username', search_query)
            ).filter(similarity__gt=0.1).order_by('-similarity')
        if len(results):
            page = self.paginate_queryset(results)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "Can't find any users."}, status=status.HTTP_204_NO_CONTENT)