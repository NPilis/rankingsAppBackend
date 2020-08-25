# Ranking App
from django.contrib.auth.decorators import (permission_required,
                                            user_passes_test)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ranking.models import Comment, DisLike, Like, Ranking, RankingPosition
from ranking.serializers import (CommentSerializer,
                                 RankingCreateUpdateSerializer,
                                 RankingListSerializer,
                                 RankingPositionSerializer,
                                 TopThreeRankingSerializer)
# REST FRAMEWORK
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from .permissions import IsOwnerOrReadOnly


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

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ranking_like(request, uuid, action):
    if request.method == 'POST':
        ranking = get_object_or_404(Ranking, uuid=uuid)
        user = request.user
        if action == 'like':
            if user in ranking.likes.all():
                Like.objects.get(user=user, ranking=ranking).delete()
                return Response({"status": "Like removed"}, status=status.HTTP_200_OK)
            else:
                Like.objects.create(user=user, ranking=ranking)
                return Response({"status": "Ranking Liked"}, status=status.HTTP_200_OK)
        elif action == 'dislike':
            if user in ranking.dislikes.all():
                DisLike.objects.get(user=user, ranking=ranking).delete()
                return Response({"status": "Dislike removed"}, status=status.HTTP_200_OK)
            else:
                DisLike.objects.create(user=user, ranking=ranking)
                return Response({"status": "Ranking Disliked"}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST','GET'])
@permission_classes([IsOwnerOrReadOnly, IsAuthenticated])
def add_position(request, uuid):
    if request.method == "POST":
        ranking = get_object_or_404(Ranking, uuid=uuid)
        user = request.user
        if ranking.author == user:
            # request.data.update({"ranking": ranking.pk})
            rp_serializer = RankingPositionSerializer(data=request.data)
            if rp_serializer.is_valid():
                rp_serializer.save()
                return Response({"done": "done"})
            return Response(rp_serializer.errors)
    if request.method == "GET":
        return Response({"done": "done"})