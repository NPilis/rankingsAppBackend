# Ranking App
from django.contrib.auth.decorators import (permission_required,
                                            user_passes_test)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from ranking.models import Comment, DisLike, Like, Ranking, RankingPosition
from ranking.serializers import (CommentSerializer, RankingCreateSerializer,
                                 RankingDetailSerializer,
                                 RankingEditSerializer,
                                 RankingPositionSerializer,
                                 TopThreeRankingSerializer,
                                 PositionEditSerializer)
# REST FRAMEWORK
from rest_framework import generics, mixins, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from . import filters
from .permissions import IsAccesableForCurrentUser, IsOwnerOfPosition, IsOwnerOrReadOnly, IsOwnerOfRanking


class PrivateRankings(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopThreeRankingSerializer
    queryset = ''

    def list(self, request, *args, **kwargs):
        private_rankings = Ranking.objects.filter(
            author=request.user
        )
        if len(private_rankings):
            page = self.paginate_queryset(private_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
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
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class UserRankings(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = TopThreeRankingSerializer
    queryset = ''

    def list(self, request, uuid, **kwargs):
        user = filters.get_user(uuid)
        user_rankings = Ranking.objects.filter(
            status="public",
            author=user)
        if len(user_rankings):
            page = self.paginate_queryset(user_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class FollowedUsersRankings(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TopThreeRankingSerializer
    queryset = ''

    def list(self, request, **kwargs):
        followed_users = request.user.following.all()
        followed_users_rankings = Ranking.objects.filter(
            status="public",
            author__in=followed_users).order_by('-created_at')
        if len(followed_users_rankings):
            page = self.paginate_queryset(followed_users_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class RankingDetail(generics.RetrieveAPIView):
    permission_classes = [IsAccesableForCurrentUser]
    serializer_class = RankingDetailSerializer

    def get_object(self):
        ranking = filters.get_ranking(self.kwargs['uuid'])
        self.check_object_permissions(self.request, ranking)
        return ranking


class CreateRanking(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RankingCreateSerializer

    def perform_create(self, serializer):
        new_ranking = serializer.save(author=self.request.user)


class DeleteRanking(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOfRanking]

    def get_object(self):
        ranking = filters.get_ranking(self.kwargs['uuid'])
        self.check_object_permissions(self.request, ranking)
        return ranking


class EditRanking(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOfRanking]
    serializer_class = RankingEditSerializer

    def get_object(self):
        ranking = filters.get_ranking(self.kwargs['uuid'])
        self.check_object_permissions(self.request, ranking)
        return ranking

# Needs improvement on permissions


class RankingPositionsCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RankingPositionSerializer
    queryset = ''

    def dispatch(self, request, *args, **kwargs):
        self.ranking = filters.get_ranking(kwargs['uuid'])
        self.ranking_positions = self.ranking.ranking_positions.all()
        return super().dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.ranking_positions, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(ranking=self.ranking)

# Needs improvement in dispatch and get_object methods


class RankingPositionDelete(generics.DestroyAPIView):
    permission_classes = [IsOwnerOfRanking]
    queryset = ''
    serializer_class = RankingPositionSerializer

    def dispatch(self, request, *args, **kwargs):
        self.ranking = filters.get_ranking(kwargs['uuid'])
        self.ranking_positions = self.ranking.ranking_positions.all()
        self.ranking_position = filters.get_ranking_position(
            self.ranking_positions, kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        obj = self.ranking
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        instance = self.ranking_position
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def perform_destroy(self, instance, position):
    #     positions_to_update = self.ranking_positions[position-1:]
    #     for pos in positions_to_update:
    #         pos.position -= 1
    #         pos.save()
    #     instance.delete()


class RankingPositionUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOfPosition]
    serializer_class = PositionEditSerializer

    def get_object(self):
        ranking_obj = filters.get_ranking(self.kwargs['uuid'])
        position_obj = filters.get_ranking_position(
            ranking_obj.ranking_positions.all(), self.kwargs['id'])
        self.check_object_permissions(self.request, position_obj)
        return position_obj


class ChangePositions(APIView):

    def put(self, request, *args, **kwargs):
        ranking_obj = filters.get_ranking(self.kwargs['uuid'])
        ranking_positions = ranking_obj.ranking_positions.all()
        print(request.data)
        serializer = RankingEditSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RankingComments(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ''
    serializer_class = CommentSerializer

    def dispatch(self, request, *args, **kwargs):
        self.ranking = filters.get_ranking(kwargs['uuid'])
        return super(RankingComments, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        ranking_comments = self.ranking.ranking_comments.all()
        if len(ranking_comments) > 0:
            page = self.paginate_queryset(ranking_comments)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No comments at this moment"}, status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, ranking=self.ranking)


class RankingLike(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ranking = filters.get_ranking(kwargs['uuid'])
        curr_like = filters.get_like_if_exist(ranking, request.user)
        curr_dislike = filters.get_dislike_if_exist(ranking, request.user)
        if curr_like:
            curr_like.delete()
            return Response({"STATUS": "Ranking unliked"}, status=status.HTTP_200_OK)
        else:
            if curr_dislike:
                curr_dislike.delete()
            Like.objects.create(user=request.user, ranking=ranking)
            return Response({"STATUS": "Ranking liked"}, status=status.HTTP_200_OK)


class RankingDisLike(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        ranking = filters.get_ranking(kwargs['uuid'])
        curr_like = filters.get_like_if_exist(ranking, request.user)
        curr_dislike = filters.get_dislike_if_exist(ranking, request.user)
        if curr_dislike:
            curr_dislike.delete()
            return Response({"STATUS": "Ranking dislike removed"}, status=status.HTTP_200_OK)
        else:
            if curr_like:
                curr_like.delete()
            DisLike.objects.create(user=request.user, ranking=ranking)
            return Response({"STATUS": "Ranking disliked"}, status=status.HTTP_200_OK)
