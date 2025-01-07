from .models import Follow, Post, CustomUser, Comment, Like, Notification, Message, SharedPost, Hashtag
from rest_framework import serializers





class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'
class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = '__all__'        

        
class PostSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    media = serializers.FileField(required=False, allow_null=True)
    hashtag = HashtagSerializer(many=True, read_only=True)
    tagged_users = serializers.StringRelatedField(many=True, read_only=True)
    class Meta:
        model = Post
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


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


