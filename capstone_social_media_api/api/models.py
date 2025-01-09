from django.db import models
from django.contrib.auth.models import AbstractUser
import re

# Create your models here.

# This class definition creates a custom user model in Django, inheriting from the built-in AbstractUser model
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    cover_photo = models.ImageField(upload_to='cover_photos/', blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)

class Hashtag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return self.name
    


class Post(models.Model):  
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    tagged_users = models.ManyToManyField(CustomUser, blank=True, related_name='tagged_posts')
    hashtags = models.ManyToManyField('Hashtag', blank=True, related_name='posts')
    timestamp = models.DateTimeField(auto_now_add=True)
    media = models.FileField(upload_to='media/', blank=True, null=True) 

    #The save method is overridden to include the extraction and assignment of hashtags and tagged users. 
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        self._extract_and_assign_hashtags()
        self._extract_and_assign_tagged_users()

    def _extract_and_assign_hashtags(self):
        hashtags = re.findall(r"#(\w+)", self.content) 
        hashtag_obj = [Hashtag.objects.get_or_create(name=hashtag.lower())[0] for hashtag in hashtags]
        self.hashtags.add(*hashtag_obj) 

    def _extract_and_assign_tagged_users(self):
        tagged_usernames = re.findall(r"@(\w+)", self.content)
        tagged_users = CustomUser.objects.filter(username__in=tagged_usernames)
        self.tagged_users.add(*tagged_users)



    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"
    


class Follow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='followers')
    followed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='following')    
    
    
    # Ensures that a user cannot follow the same user twice 
    class Meta:
        unique_together = ('user', 'followed_user')

    def __str__(self):
        return f"{self.user.username} follows {self.followed_user.username}"


class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    is_repost = models.BooleanField(default=False)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} liked {self.post.user.username}'s post"
    

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} commented on {self.post.user.username}'s post"


class Notification(models.Model):
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sender')
    type = models.CharField(max_length=50)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.recipient.username} received a {self.type} notification from {self.sender.username}"


class Message(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    recipient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.sender.username} sent a message to {self.recipient.username}"
    

class SharedPost(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.user.username} shared {self.post.user.username}'s post"


