# Ranking App
from django.contrib.auth.decorators import (permission_required,
                                            user_passes_test)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ranking.models import Comment, DisLike, Like, Ranking, RankingPosition
from ranking.serializers import (CommentSerializer,
                                 RankingSerializer,
                                 RankingDetailSerializer,
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
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly, IsOwner
from . import filters

class PrivateRankings(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopThreeRankingSerializer
    queryset = ''

    def list(self, request, *args, **kwargs):
        private_rankings = Ranking.objects.filter(
            author=request.user,
            status="private"
        )
        if len(private_rankings):
            page = self.paginate_queryset(private_rankings)
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)
        

class PublicRankings(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TopThreeRankingSerializer
    queryset = ''

    def list(self, request, **kwargs):
        public_rankings = Ranking.objects.filter(status="public")
        if len(public_rankings):
            page = self.paginate_queryset(public_rankings)
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class RankingDetail(generics.RetrieveAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = 'uuid'
    serializer_class = RankingDetailSerializer

    def get(self, request, *args, **kwargs):
        ranking = filters.get_ranking(kwargs['uuid'])
        serializer = self.get_serializer(ranking, 
                                         many=False,
                                         context={'request':request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateRanking(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RankingSerializer
    queryset = ''

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        new_ranking = serializer.save(author=self.request.user)

class DeleteRanking(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'uuid'
    queryset = Ranking.objects.all()

class RankingComments(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ''
    serializer_class = CommentSerializer

    def dispatch(self, request, *args, **kwargs):
        self.ranking = filters.get_ranking(kwargs['uuid'])
        return super(RankingComments, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        ranking_comments = self.ranking.ranking_comments.all()
        # ranking_comments = Comment.objects.filter(ranking=self.ranking)
        if len(ranking_comments) > 0:
            page = self.paginate_queryset(ranking_comments)
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No comments at this moment"}, status=status.HTTP_204_NO_CONTENT)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, ranking=self.ranking)

class RankingLike(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    def dispatch(self, request, *args, **kwargs):
        self.ranking = filters.get_ranking(kwargs['uuid'])
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        curr_like = filters.get_like_if_exist(self.ranking, self.user)
        curr_dislike = filters.get_dislike_if_exist(self.ranking, self.user)
        if curr_like:
            curr_like.delete()
            return Response({"STATUS": "Ranking unliked"}, status=status.HTTP_200_OK)
        else:
            if curr_dislike:
                curr_dislike.delete()
            Like.objects.create(user=self.user, ranking=self.ranking)
            return Response({"STATUS": "Ranking liked"}, status=status.HTTP_200_OK)

class RankingDisLike(APIView):
    permission_classes = [permissions.IsAuthenticated,]
    
    def dispatch(self, request, *args, **kwargs):
        self.ranking = filters.get_ranking(kwargs['uuid'])
        self.user = request.user
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        curr_like = filters.get_like_if_exist(self.ranking, self.user)
        curr_dislike = filters.get_dislike_if_exist(self.ranking, self.user)
        if curr_dislike:
            curr_dislike.delete()
            return Response({"STATUS": "Ranking dislike removed"}, status=status.HTTP_200_OK)
        else:
            if curr_like:
                curr_like.delete()
            DisLike.objects.create(user=self.user, ranking=self.ranking)
            return Response({"STATUS": "Ranking disliked"}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsOwnerOrReadOnly, IsAuthenticated])
def add_position(request, uuid):
    if request.method == "POST":
        ranking = get_object_or_404(Ranking, uuid=uuid)
        user = request.user
        if ranking.author == user:
            rp_serializer = RankingPositionSerializer(data=request.data)
            if rp_serializer.is_valid():
                rp_serializer.save(ranking=ranking)
                return Response({"Status": "Position added"})
        return Response({"Error": "Not an owner"})

# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def ranking_like(request, uuid, action):
#     if request.method == 'POST':
#         ranking = get_object_or_404(Ranking, uuid=uuid)
#         user = request.user
#         if action == 'like':
#             if user in ranking.likes.all():
#                 Like.objects.get(user=user, ranking=ranking).delete()
#                 return Response({"status": "Like removed"}, status=status.HTTP_200_OK)
#             else:
#                 Like.objects.create(user=user, ranking=ranking)
#                 return Response({"status": "Ranking Liked"}, status=status.HTTP_200_OK)
#         elif action == 'dislike':
#             if user in ranking.dislikes.all():
#                 DisLike.objects.get(user=user, ranking=ranking).delete()
#                 return Response({"status": "Dislike removed"}, status=status.HTTP_200_OK)
#             else:
#                 DisLike.objects.create(user=user, ranking=ranking)
#                 return Response({"status": "Ranking Disliked"}, status=status.HTTP_200_OK)
#         else:
#             return Response({"status": "bad request"}, status=status.HTTP_400_BAD_REQUEST)

# class RankingDetail(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

#     def dispatch(self, request, *args, **kwargs):
#         self.viewAccess = False
#         self.isOwner = False
#         self.user = request.user
#         self.ranking = get_object_or_404(Ranking, uuid=kwargs.get('uuid'))
#         if self.ranking.status == 'public':
#             self.viewAccess = True
#         if self.ranking.author == self.user:
#             self.isOwner = True
        
#         return super(RankingDetail, self).dispatch(request, *args, **kwargs)
    
#     def get(self, request, uuid, *args, **kwargs):
#         if self.viewAccess or self.isOwner:
#             serializer = RankingDetailSerializer(self.ranking, context={'request':request})
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'No access'}, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request, uuid, *args, **kwargs):
#         if self.isOwner:
#             serializer = RankingSerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({'error': 'Not an owner'}, status=status.HTTP_400_BAD_REQUEST)

#     def put(self, request, *args, **kwargs):
#         if self.isOwner:
#             serializer = RankingSerializer(self.ranking, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response({'error': 'Not an owner'}, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, *args, **kwargs):
#         if self.isOwner:
#             self.ranking.delete()
#             return Response(status=status.HTTP_200_OK)
#         return Response({'error': 'Not an owner'}, status=status.HTTP_400_BAD_REQUEST)

