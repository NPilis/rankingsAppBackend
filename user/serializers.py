from user.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:user-detail',
                                               lookup_field='username')

    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'image', 'is_active', 'uuid']

class DetailUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:user-detail',
                                               lookup_field='username')
    # followers = serializers.HyperlinkedIdentityField(many=True,
    #                                                  view_name='users:user-detail',
    #                                                  lookup_field='uuid')
    # following = serializers.HyperlinkedIdentityField(many=True,
    #                                                  view_name='users:user-detail',
    #                                                  lookup_field='uuid')
    followers = serializers.StringRelatedField(many=True)
    following = serializers.StringRelatedField(many=True)

    class Meta:
        model = User
        fields = ['url','email', 'username', 'image', 'is_active', 'following', 'followers', 'uuid', 'date_joined']

class UpdateUserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['image']