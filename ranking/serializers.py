from .models import Ranking, RankingPosition, Comment, Like
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from user.serializers import UserSerializer

class RankingPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RankingPosition
        fields = ['title', 'ranking', 'description', 'position', 'image']
        read_only_fields = ['ranking', 'position']

class RankingCreateSerializer(serializers.ModelSerializer):
    ranking_positions = RankingPositionSerializer(many=True, required=False)

    class Meta:
        model = Ranking
        fields = ['title', 'content', 'status', 'image', 'ranking_positions']
        read_only_fields = ['author']

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
    
    class Meta:
        model = Ranking
        fields = ['title', 'content', 'author', 'likes', 'dislikes', 'comments', 'shares', 'total_difference', 'ranking_positions', 'status']
        read_only_fields = ['author', 'created_at', 'edited_at', 'likes', 'dislikes', 'total_difference', 'ranking_positions']


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
        fields = ['title', 'url', 'author', 'top_three_rp', 'created_at', 'likes', 'dislikes', 'total_difference', 'uuid', 'status', 'shares', 'comments']
        read_only_fields = ['author', 'created_at', 'edited_at', 'likes', 'dislikes', 'total_difference', 'top_three_rp', 'url', 'uuid', 'status', 'shares', 'comments']

    def get_top_three_rp(self, obj):
        top_three = RankingPosition.objects.filter(ranking=obj)[:3]
        return RankingPositionSerializer(top_three, many=True, read_only=True).data

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    ranking = serializers.HyperlinkedRelatedField(
        many=False,
        read_only=True,
        view_name='rankings:ranking-detail',
        lookup_field = 'uuid'
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['created_at', 'edited_at', 'ranking', 'user', 'active']