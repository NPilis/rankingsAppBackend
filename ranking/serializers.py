from .models import Ranking, RankingPosition, Comment
from rest_framework import serializers


class RankingPositionSerializer(serializers.ModelSerializer):

    class Meta:
        model = RankingPosition
        fields = ['title', 'ranking', 'description', 'position', 'image']
        read_only_fields = ['ranking']
    
    def create(self, validated_data):
        ranking_position = RankingPosition.objects.create(ranking=ranking, **validated_data)
        return ranking_position

class RankingCreateUpdateSerializer(serializers.ModelSerializer):
    ranking_positions = RankingPositionSerializer(many=True)

    class Meta:
        model = Ranking
        fields = ['author', 'title', 'content', 'status', 'image', 'ranking_positions']
    
    def create(self, validated_data):
        ranking_positions = validated_data.pop('ranking_positions')
        ranking = Ranking.objects.create(**validated_data)
        for rp in ranking_positions:
            RankingPosition.objects.create(ranking=ranking, **rp)
        return ranking


class RankingListSerializer(serializers.ModelSerializer):
    ranking_positions = RankingPositionSerializer(many=True, read_only=True)

    class Meta:
        model = Ranking
        fields = '__all__'
        read_only_fields = ['author', 'created_at', 'edited_at', 'likes', 'dislikes', 'total_difference', 'ranking_positions']

class TopThreeRankingSerializer(serializers.ModelSerializer):
    top_three_rp = serializers.SerializerMethodField()

    class Meta:
        model = Ranking
        fields = ['author', 'title', 'created_at', 'likes', 'dislikes', 'total_difference', 'top_three_rp', 'uuid']
        read_only_fields = ['author', 'created_at', 'edited_at', 'likes', 'dislikes', 'total_difference', 'top_three_rp']

    def get_top_three_rp(self, obj):
        top_three = RankingPosition.objects.filter(ranking=obj)[:3]
        return RankingPositionSerializer(top_three, many=True, read_only=True).data


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['reply_to', 'created_at', 'edited_at']

    def create(self, validated_data):
        ranking = validated_data.pop('ranking')
        user = validated_data.pop('user')
        comment = Comment.objects.create(user=user, ranking=ranking, **validated_data)
        return comment