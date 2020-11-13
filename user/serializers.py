from user.models import User
from rest_framework import serializers
from ranking.models import Comment, Ranking

class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:user-detail',
                                               lookup_field='username')

    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'image', 'is_active', 'uuid']


class DetailUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:user-detail',
                                               lookup_field='username')
    followers = serializers.StringRelatedField(many=True)
    following = serializers.StringRelatedField(many=True)
    num_of_rankings = serializers.SerializerMethodField()
    num_of_comments = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'image', 'is_active',
                  'following', 'followers', 'uuid', 'date_joined', 'num_of_comments', 'num_of_rankings']

    def get_num_of_rankings(self, obj):
        return Ranking.objects.filter(author=obj).count()
    
    def get_num_of_comments(self, obj):
        return Comment.objects.filter(user=obj).count()

class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['image']
