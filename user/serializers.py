from user.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:user-detail',
                                            lookup_field='uuid')

    class Meta:
        model = User
        fields = ['url', 'email', 'username', 'image', 'is_active']

class DetailUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='users:user-detail',
                                            lookup_field='uuid')
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
        fields = ['url','email', 'username', 'image', 'is_active', 'following', 'followers']