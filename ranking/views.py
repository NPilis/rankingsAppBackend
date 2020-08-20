# Ranking App
from ranking.models import Ranking, RankingPosition, Comment, Like, DisLike
from ranking.serializers import (
    RankingPositionSerializer,
    RankingListSerializer,
    TopThreeRankingSerializer,
    RankingCreateUpdateSerializer,
    CommentSerializer
    )

from django.shortcuts import get_object_or_404

# REST FRAMEWORK
from rest_framework import generics, status
from rest_framework.generics import RetrieveAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.decorators import permission_classes, api_view
from .permissions import IsOwnerOrReadOnly

from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import user_passes_test

class CurrentRanking(APIView):
    def get(self, request, pk):
        try: 
            ranking = Ranking.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        serializer = RankingListSerializer(ranking)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateRanking(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data.update({"author": request.user.pk})
        serializer = RankingCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RankingPrivateList(APIView):
    permission_classes = [IsAuthenticated]

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        return super(RankingPrivateList, self).dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        ranks = Ranking.objects.filter(
            author=self.user,
            status="private"
            )
        rank_serializer = TopThreeRankingSerializer(ranks, many=True)
        return Response(rank_serializer.data, status=status.HTTP_200_OK)
        

class RankingPublicList(APIView):
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        ranks = Ranking.objects.filter(status="public")
        rank_serializer = TopThreeRankingSerializer(ranks, many=True)
        return Response(rank_serializer.data, status=status.HTTP_200_OK)

class RankingDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def dispatch(self, request, *args, **kwargs):
        self.viewAccess = False
        self.isOwner = False
        self.user = request.user
        self.ranking = get_object_or_404(Ranking, uuid=kwargs.get('uuid'))
        if self.ranking.status == 'public':
            self.viewAccess = True
        if self.ranking.author == self.user:
            self.isOwner = True
        
        return super(RankingDetail, self).dispatch(request, *args, **kwargs)
    
    def get(self, request, uuid, *args, **kwargs):
        if self.viewAccess or self.isOwner:
            serializer = RankingListSerializer(self.ranking)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'No access'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uuid, *args, **kwargs):
        if self.isOwner:
            serializer = RankingCreateUpdateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Not an owner'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        if self.isOwner:
            serializer = RankingCreateUpdateSerializer(self.ranking, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': 'Not an owner'}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        if self.isOwner:
            self.ranking.delete()
            return Response(status=status.HTTP_200_OK)
        return Response({'error': 'Not an owner'}, status=status.HTTP_400_BAD_REQUEST)


class CommentRanking(APIView):

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.ranking = get_object_or_404(Ranking, uuid=kwargs.get('uuid'))
        return super(CommentRanking, self).dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        request.data.update({"user": self.user.pk, "ranking": self.ranking.pk})
        serializer = CommentSerializer(data=request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            print(serializer.errors)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        comments = Comment.objects.filter(ranking=self.ranking)
        if comments:
            comment_serializer = CommentSerializer(comments, many=True)
            return Response(comment_serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def ranking_like(request, uuid, action):
    if request.method == 'POST':
        ranking = get_object_or_404(Ranking, uuid=uuid)
        user = request.user
        data_ = {'data': 'test'}
        if action == 'like':
            if user in ranking.likes.all():
                ranking.likes.remove(user)
                Like.objects.get(user=user, ranking=ranking).delete()
                return Response({"status": "liked"}, status=status.HTTP_200_OK)
            else:
                ranking.likes.add(user)
                Like.objects.create(user=user, ranking=ranking)
            return Response(data_, status=status.HTTP_200_OK)
        if action == 'dislike':
            if user in ranking.dislikes.all():
                ranking.dislikes.remove(user)
                DisLike.objects.get(user=user, ranking=ranking).delete()
            else:
                ranking.dislikes.add(user)
                DisLike.objects.create(user=user, ranking=ranking)
            return Response(data_, status=status.HTTP_200_OK)