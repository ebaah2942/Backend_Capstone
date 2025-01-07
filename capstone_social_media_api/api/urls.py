from .views import (FollowViewSet, PostViewSet, FeedView, 
                    LoginView, RegisterView, LogoutView, 
                    ProfileView,
                    MessageViewSet, 
                    SharedPostViewSet, HashtagViewSet, 
                    LikeViewset, CommentViewSet, NotificationViewSet)
from rest_framework.routers import DefaultRouter
from django.urls import path, include

router = DefaultRouter()
router.register('posts', PostViewSet, basename='post')
router.register('sharedposts', SharedPostViewSet, basename='sharedpost')
router.register('hashtags', HashtagViewSet)
router.register('likes', LikeViewset, basename='like')
router.register('comments', CommentViewSet, basename='comment')
router.register('notifications', NotificationViewSet, basename='notification')
router.register('messages', MessageViewSet, basename='message')
# router.register('users', CustomUserViewSet)
router.register('follows', FollowViewSet, basename='follow')


urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('feed/', FeedView.as_view(), name='feed'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

