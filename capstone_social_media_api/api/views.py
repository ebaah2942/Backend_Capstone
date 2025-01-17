from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
import re
from django.db import models
from django.utils.timezone import now, timedelta 
from rest_framework.views import APIView
from .serializers import( CustomUserSerializer, PostSerializer, FollowSerializer, 
                         CommentSerializer, LikeSerializer, 
                         NotificationSerializer, MessageSerializer, SharedPostSerializer, HashtagSerializer)
from .models import CustomUser, Post, Follow, Comment, Like, Notification, Message, SharedPost, Hashtag
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.http import Http404
from django.utils.decorators import method_decorator
# Create your views here.


# It uses regular expressions to find all hashtags in the post.content
def extract_and_save_hashtag(post, text):
    hashtags = re.findall(r'#(\w+)', post.content)
    for tags in hashtags:
        hashtag, created = Hashtag.objects.get_or_create(name=tags.lower())
        post.Hashtags.add(hashtag)

    #This function generates and returns a dictionary containing a refresh token and an access token for a given user    
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }    
# This class definition defines a view for handling user registration
# Note that the permission_classes attribute allows any user to access this view, regardless of their authentication status
@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not username or not email or not password:
            return Response({'error': 'Username, email, and password are required.'}, status=400)
        
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=400)
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=400)
        
        user = CustomUser.objects.create_user(username=username, email=email, password=password)
        token = get_tokens_for_user(user)
        return Response({
            "message": "User registered successfully.",
            "username": user.username,
            "tokens": token
        }, status=status.HTTP_201_CREATED)
      
# This class definition defines a view for handling user login
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        # Validate username and password
        if not username or not password:
            return Response({'error': 'Username and password are required.'}, status=400)
        # Check if user exists
        user = CustomUser.objects.filter(username=username).first()
        if user is not None:
            token = get_tokens_for_user(user)
            return Response({
                "message": "User logged in successfully.",
                "username": user.username,
                "tokens": token
            }, status.HTTP_200_OK)
        return Response({'error': 'Invalid username or password.'}, status=401)

# This class definition defines a view for handling user logout requests
# Note that the permission_classes = [IsAuthenticated] line ensures that only authenticated users can access this view
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid refresh token.'}, status=status.HTTP_400_BAD_REQUEST)

# This class definition defines a view for handling user profile updates
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    # Updates a user's profile information with the data provided in the request.
    # Returns the updated user data if the update is successful, or an error message if the update fails.
    def put(self, request):
        user = request.user
        serializer = CustomUserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)               


# This class definition, PostPagination, is used to paginate a list of posts in an API. Here's what each attribute does
class PostPagination(PageNumberPagination):
    page_size = 10  # Number of posts per page
    page_size_query_param = 'page_size'  # Allow clients to set custom page size
    max_page_size = 50  #


# This class definition, FeedView, is used to retrieve a list of posts in an API
class FeedView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PostPagination
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['timestamp', 'likes', 'comments']  # Allow sorting by date, likes, or comments
    ordering = ['-timestamp']  # Default sorting: most recent posts first


# This class definition, PostViewSet, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on posts.
# Note that the update and destroy methods override the default behavior of the ModelViewSet to enforce ownership-based permissions.
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # This method is used to filter the queryset based on the 'hashtag' and 'tagged_users' query parameters
    def get_queryset(self):
        hashtag = self.request.query_params.get('hashtag')
        tagged_user = self.request.query_params.get('tagged_users')


        if hashtag:
            return Post.objects.filter(Hashtags__name=hashtag).order_by('-timestamp')
        elif tagged_user:
            return Post.objects.filter(tagged__users__username__=tagged_user.split(',')).order_by('-timestamp')
        
        elif self.action == 'list':
            following_ids = self.request.user.following.values_list('followed_user', flat=True)
            return Post.objects.filter(user__id__in=following_ids).order_by('-timestamp')
        
        return super().get_queryset()
    
    # This method is used to retrieve the top 10 most liked posts in the last 24 hours
    @action(detail=True, methods=['get'])
    def trending(self, request):
        hourly = now() - timedelta(hours=24)
        trending = Post.objects.filter(timestamp__gte=hourly).annotate(total_likes=models.Count('likes') + models.Count('shared_post__likes')) .order_by('-total_likes')[:10]
        serializer = PostSerializer(trending, many=True)
        return Response(serializer.data)

        
    # This method overrides the default update method to enforce ownership-based permissions
    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({"error": "You can only update your own posts."}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)
    
    # This method overrides the default destroy method to enforce ownership-based permissions
    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({"error": "You can only delete your own posts."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
        return Response({"message": "Post deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
    

# This class definition, FollowViewSet, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on follows.
class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        followed_user_id = request.data.get('followed_user')
        if followed_user_id is None:
            return Response({"error": "Followed user ID is required."}, status=status.HTTP_400_BAD_REQUEST)
       # Prevent self-follow
        if request.user.id == request.data.get('followed_user'):
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        # Ensure that the followed_user exists
        try:
            followed_user = CustomUser.objects.get(id=request.data.get('followed_user'))
        except CustomUser.DoesNotExist:
            return Response({"error": "Followed user does not exist."}, status=status.HTTP_400_BAD_REQUEST)
        # Check if already following
        if Follow.objects.filter(user=request.user, followed_user=followed_user).exists():
            return Response({"error": "You are already following this user."}, status=status.HTTP_400_BAD_REQUEST)
        # Create follower relationship
        follower = Follow.objects.create(user=request.user, followed_user=followed_user)
        serializer = self.get_serializer(follower)
        if serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else :
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # This method overrides the default destroy method to enforce ownership-based permissions
    def destroy (self, request, *args, **kwargs):
        try:
            follow = self.get_object()
        except Http404:
            return Response({"error": "Follow does not exist."}, status=status.HTTP_404_NOT_FOUND)
        if follow.user != request.user:
            return Response({"error": "You can only unfollow user you are following."}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)    

    # This class definition, LikeViewset, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on likes
class LikeViewset(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = LikeSerializer
    
    #  This is a custom action method. It is triggered when a POST request is made to the toggle_like endpoint
    @action(detail=True, methods=['post'])
    def toggle_like(self, request, pk=None):
        post = Post.objects.get(id=pk)
        like, created = Like.objects.get_or_create(post=post, user=request.user)
        if not created:
            like.delete()
            return Response({"message": "Unliked successfully."}, status=status.HTTP_200_OK)
        return Response({"message": "Liked successfully."}, status=status.HTTP_200_OK)

    
# This class definition, CommentViewset, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on comments
# Note that this class definition does not explicitly define any methods, which means it will inherit the default CRUD methods. 
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]


# This class definition, NotificationViewset, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on notifications
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    # This method overrides the default get_queryset method to filter notifications based on the current user
    def get_queryset(self):
        return self.get_queryset.filter(recipient=self.request.user)
    
    # This is a custom action method. It is triggered when a POST request is made to the mark_as_read endpoint
    @action(detail=True, methods=['post'])
    def mark_as_read(self, request,):
        notifications = self.queryset.filter(receiver=request.user, is_read=False)
        notifications.update(is_read=True)
        return Response({'message': 'All notifications marked as read.'})
    




# This class definition, MessageViewset, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on messages 
class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]


# This class definition, SharedPostViewset, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on shared posts
class SharedPostViewSet(viewsets.ModelViewSet):
    queryset = SharedPost.objects.all()
    serializer_class = SharedPostSerializer
    permission_classes = [IsAuthenticated]

# This class definition, HashtagViewset, is a viewset for handling CRUD (Create, Read, Update, Delete) operations on hashtags
class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
    permission_classes = [IsAuthenticated]    


class SharedPostViewSet(viewsets.ModelViewSet):
    queryset = SharedPost.objects.all()
    serializer_class = SharedPostSerializer
    permission_classes = [IsAuthenticated]    