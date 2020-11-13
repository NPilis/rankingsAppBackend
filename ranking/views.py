from django.contrib.auth.decorators import (permission_required,
                                            user_passes_test)
from django.contrib.postgres.search import (SearchQuery, SearchRank,
                                            SearchVector, TrigramSimilarity)
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# REST FRAMEWORK
from rest_framework import filters, generics, mixins, permissions, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView

from ranking.models import Comment, DisLike, Like, Ranking, RankingPosition
from ranking import serializers

from . import filters as f
from .permissions import (IsAccesableForCurrentUser, IsOwnerOfPosition,
                          IsOwnerOfRanking, IsOwnerOrReadOnly)
from .search import RankingSearch


class PrivateRankings(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TopThreeRankingSerializer
    queryset = ''

    def list(self, request, *args, **kwargs):
        """
        Returns list of current user rankings
        both private and public
        HTTP_204 if no results
        """
        private_rankings = Ranking.objects.filter(
            author=request.user
        )
        if len(private_rankings) > 0:
            page = self.paginate_queryset(private_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class PublicRankings(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TopThreeRankingSerializer
    queryset = ''

    def list(self, request, **kwargs):
        """
        Returns list of all rankings with public status
        HTTP_204 if no results
        """
        public_rankings = Ranking.objects.filter(status="public")
        if len(public_rankings) > 0:
            page = self.paginate_queryset(public_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class UserRankings(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TopThreeRankingSerializer
    queryset = ''

    def list(self, request, uuid, **kwargs):
        """
        Finds user by passed UUID
        Returns user's rankings with public status
        HTTP_204 if no results  
        """
        user = f.get_user(uuid)
        user_rankings = Ranking.objects.filter(
            status="public",
            author=user)
        if len(user_rankings) > 0:
            page = self.paginate_queryset(user_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class FollowedUsersRankings(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.TopThreeRankingSerializer
    queryset = ''

    def list(self, request, **kwargs):
        """
        Returns ranking list of followed users
        HTTP_204 if no results
        """
        followed_users = request.user.following.all()
        followed_users_rankings = Ranking.objects.filter(
            status="public",
            author__in=followed_users).order_by('-created_at')
        if len(followed_users_rankings) > 0:
            page = self.paginate_queryset(followed_users_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class RankingDetail(generics.RetrieveAPIView):
    permission_classes = [IsAccesableForCurrentUser]
    serializer_class = serializers.RankingDetailSerializer

    def get_object(self):
        """
        Finds ranking by passed UUID
        Returns ranking if user is allowed
        """
        ranking = f.get_ranking(self.kwargs['uuid'])
        self.check_object_permissions(self.request, ranking)
        return ranking


class CreateRanking(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RankingCreateSerializer

    def perform_create(self, serializer):
        """
        Creates ranking if user is authenticated
        """
        new_ranking = serializer.save(author=self.request.user)


class DeleteRanking(generics.DestroyAPIView):
    permission_classes = [IsOwnerOfRanking]

    def get_object(self):
        """
        Get ranking and check for permissions to delete
        """
        ranking = f.get_ranking(self.kwargs['uuid'])
        self.check_object_permissions(self.request, ranking)
        return ranking


class EditRanking(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOfRanking]
    serializer_class = serializers.RankingEditSerializer

    def get_object(self):
        """
        Get ranking and check for permissions to update
        """
        ranking = f.get_ranking(self.kwargs['uuid'])
        self.check_object_permissions(self.request, ranking)
        return ranking


class RankingPositionsCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.RankingPositionSerializer
    queryset = ''

    def dispatch(self, request, *args, **kwargs):
        self.ranking = f.get_ranking(kwargs['uuid'])
        self.ranking_positions = self.ranking.ranking_positions.all()
        return super().dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Returns list of all positions of ranking got by passed UUID
        """
        serializer = self.get_serializer(self.ranking_positions, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(ranking=self.ranking)


class RankingPositionDelete(generics.DestroyAPIView):
    permission_classes = [IsOwnerOfRanking]
    queryset = ''
    serializer_class = serializers.RankingPositionSerializer

    def dispatch(self, request, *args, **kwargs):
        self.ranking = f.get_ranking(kwargs['uuid'])
        self.ranking_positions = self.ranking.ranking_positions.all()
        self.ranking_position = f.get_ranking_position(
            self.ranking_positions, kwargs['id'])
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        """
        Get ranking position and check for permissions to delete
        """
        obj = self.ranking
        self.check_object_permissions(self.request, obj)
        return obj

    def destroy(self, request, *args, **kwargs):
        """
        Deletes ranking position if current user is allowed
        """
        instance = self.ranking_position
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RankingPositionUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsOwnerOfPosition]
    serializer_class = serializers.PositionEditSerializer

    def get_object(self):
        """
        Get ranking position and check for permissions to update
        """
        ranking_obj = f.get_ranking(self.kwargs['uuid'])
        position_obj = f.get_ranking_position(
            ranking_obj.ranking_positions.all(), self.kwargs['id'])
        self.check_object_permissions(self.request, position_obj)
        return position_obj


class RankingComments(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ''
    serializer_class = serializers.CommentSerializer

    def dispatch(self, request, *args, **kwargs):
        self.ranking = f.get_ranking(kwargs['uuid'])
        return super(RankingComments, self).dispatch(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        """
        Returns list of paginated comments
        HTTP_204 if no results
        """
        ranking_comments = self.ranking.ranking_comments.all()
        if len(ranking_comments) > 0:
            page = self.paginate_queryset(ranking_comments)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No comments at this moment"}, status=status.HTTP_204_NO_CONTENT)

    def perform_create(self, serializer):
        """
        Create new comment if user is allowed
        """
        serializer.save(user=self.request.user, ranking=self.ranking)


class RankingLike(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Create/Delete ranking like by checking if it exist.
        Also look if given ranking is disliked by current user.
        If it is, then delete this dislike
        """
        ranking = f.get_ranking(kwargs['uuid'])
        curr_like = f.get_like_if_exist(ranking, request.user)
        curr_dislike = f.get_dislike_if_exist(ranking, request.user)
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
        """
        Create/Delete ranking dislike by checking if it exist.
        Also look if given ranking is liked by current user.
        If it is, then delete this like
        """
        ranking = f.get_ranking(kwargs['uuid'])
        curr_like = f.get_like_if_exist(ranking, request.user)
        curr_dislike = f.get_dislike_if_exist(ranking, request.user)
        if curr_dislike:
            curr_dislike.delete()
            return Response({"STATUS": "Ranking dislike removed"}, status=status.HTTP_200_OK)
        else:
            if curr_like:
                curr_like.delete()
            DisLike.objects.create(user=request.user, ranking=ranking)
            return Response({"STATUS": "Ranking disliked"}, status=status.HTTP_200_OK)


class HottestRankings(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TopThreeRankingSerializer
    queryset = ''

    def list(self, request, **kwargs):
        """
        Returns list of hottest public rankings
        Filters recently created rankings
        by number of days passed in the url
        """
        timestamp = f.set_time_range(kwargs['days'])
        hottest_rankings = Ranking.objects.filter(
            status="public",
            created_at__gt=timestamp
        )
        if len(hottest_rankings):
            page = self.paginate_queryset(hottest_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class NewestRankings(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = serializers.TopThreeRankingSerializer
    queryset = ''

    def list(self, request, **kwargs):
        """
        Returns list of newest rankings with public status
        Filters recently created rankings by number of days passed in the url
        """
        timestamp = f.set_time_range(kwargs['days'])
        newest_rankings = Ranking.objects.filter(
            status="public", created_at__gt=timestamp).order_by('-created_at')
        if len(newest_rankings):
            page = self.paginate_queryset(newest_rankings)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)


class SearchRanking(generics.ListAPIView):
    serializer_class = serializers.TopThreeRankingSerializer
    queryset = ''

    def get_queryset(self):
        queryset = Ranking.objects.filter(status='public')
        return queryset

    def list(self, request, **kwargs):
        """
        Custom search on ranking title by query passed in the url
        Filters public rankings with each term in query
        Searching completely ignores words of length < 3
        HTTP_204 if no results
        """
        search_query = kwargs["query"]
        if search_query:
            Filter = RankingSearch(search_query)
            results = Filter.get_results()
        if results:
            page = self.paginate_queryset(results)
            serializer = self.get_serializer(
                page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        return Response({"STATUS": "No rankings at this moment"}, status=status.HTTP_204_NO_CONTENT)
