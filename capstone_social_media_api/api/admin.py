from django.contrib import admin
from .models import CustomUser, Post, Follow, Comment, Like, Notification, Message, SharedPost, Hashtag



# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'bio', 'profile_picture', 'website', 'cover_photo', 'location')
    search_fields = ('username', 'email')
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'timestamp', 'media')
    search_fields = ('user__username', 'content')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)
@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'followed_user')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'timestamp')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ( 'post', 'timestamp')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'content', 'timestamp')

@admin.register(SharedPost)
class SharedPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'timestamp')


@admin.register(Hashtag)
class HashtagAdmin(admin.ModelAdmin):
    list_display = ('name', 'timestamp')                        