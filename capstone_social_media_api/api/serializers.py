from .models import Follow, Post, CustomUser, Comment, Like, Notification, Message, SharedPost, Hashtag
from rest_framework import serializers




# This class definition, CustomUserSerializer,
#  is a Django Rest Framework (DRF) serializer that converts a CustomUser model instance into a JSON representation.
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

# This class definition, HashtagSerializer, is a Django Rest Framework (DRF) serializer that converts a Hashtag model instance into a JSON representation
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'        

# This class definition, PostSerializer, is a Django Rest Framework (DRF) serializer that converts a Post model instance into a JSON representation
class PostSerializer(serializers.ModelSerializer):
    # Represents the user associated with the post, using the CustomUserSerializer to serialize the user data
    user = CustomUserSerializer()
    media = serializers.FileField(required=False, allow_null=True)
    hashtag = HashtagSerializer(many=True, read_only=True)
    tagged_users = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'

# This class definition, FollowSerializer, 
# is a Django Rest Framework (DRF) serializer that converts a Follow model instance into a JSON representation. 
class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

# This class definition, CommentSerializer,
#  is a Django Rest Framework (DRF) serializer that converts a Comment model instance into a JSON representation
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'        



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'        


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'     


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'   


class SharedPostSerializer(serializers.ModelSerializer):
    class Meta: 
        model = SharedPost
        fields = '__all__'        


