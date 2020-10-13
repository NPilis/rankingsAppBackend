from .models import Ranking, RankingPosition, Comment, Like
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from user.serializers import UserSerializer

class RankingPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RankingPosition
        fields = ['title', 'ranking', 'description', 'position', 'image']
        read_only_fields = ['ranking']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Comment
        fields = ['created_at', 'edited_at', 'ranking', 'user', 'active', 'text']
        read_only_fields = ['created_at', 'edited_at', 'ranking', 'user', 'active']

class RankingCreateSerializer(serializers.ModelSerializer):
    ranking_positions = RankingPositionSerializer(many=True, required=False)

    class Meta:
        model = Ranking
        fields = ['uuid', 'title', 'content', 'status', 'image', 'ranking_positions']
        read_only_fields = ['author', 'uuid']

    #Needs improvement
    def create(self, validated_data):
        try:
            ranking_positions = validated_data.pop('ranking_positions')
        except KeyError:
            ranking = Ranking.objects.create(**validated_data)
            return ranking
        ranking = Ranking.objects.create(**validated_data)
        for rp in ranking_positions:
            RankingPosition.objects.create(ranking=ranking, **rp)
        return ranking

class RankingEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ranking
        fields = ['title', 'content', 'status', 'image']

class RankingDetailSerializer(serializers.ModelSerializer):
    ranking_positions = RankingPositionSerializer(many=True, read_only=True)
    author = UserSerializer(many=False)
    likes = serializers.StringRelatedField(many=True)
    dislikes = serializers.StringRelatedField(many=True)
    shares = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Ranking
        fields = ['title', 'content', 'author', 'likes', 'dislikes', 'ranking_comments', 'shares', 'total_difference', 'ranking_positions', 'status', 'image', 'created_at', 'uuid']
        read_only_fields = ['author','ranking_comments', 'created_at', 'edited_at', 'likes', 'dislikes', 'total_difference', 'ranking_positions', 'image', 'uuid']

class TopThreeRankingSerializer(serializers.ModelSerializer):
    """
        Used for list views when only top three ranking posisions are needed.
    """
    top_three_rp = serializers.SerializerMethodField()
    author = UserSerializer(many=False)
    url = serializers.HyperlinkedIdentityField(view_name='rankings:ranking-detail',
                                               lookup_field='uuid')
    likes = serializers.StringRelatedField(many=True)
    dislikes = serializers.StringRelatedField(many=True)
    shares = serializers.StringRelatedField(many=True)
    comments = serializers.StringRelatedField(many=True)

    class Meta:
        model = Ranking
        fields = ['title', 'url', 'author', 'top_three_rp', 'created_at', 'likes', 'dislikes', 'total_difference', 'uuid', 'status', 'shares', 'comments', 'image']
        read_only_fields = ['author', 'created_at', 'edited_at', 'likes', 'dislikes', 'total_difference', 'top_three_rp', 'url', 'uuid', 'status', 'shares', 'comments', 'image']

    def get_top_three_rp(self, obj):
        top_three = RankingPosition.objects.filter(ranking=obj)[:3]
        return RankingPositionSerializer(top_three, many=True, read_only=True).data