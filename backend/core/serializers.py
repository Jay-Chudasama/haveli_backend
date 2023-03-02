import datetime

from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from core.models import User, StoryImage, Post, Notification, Follow


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'image']


class UserDetailsSerializer(ModelSerializer):
    followers = SerializerMethodField()
    following = SerializerMethodField()
    posts = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'image', 'bio', 'followers', 'following', 'posts']

    def get_following(self, user):
        return Follow.objects.get(user=user).follow.count()

    def get_posts(self, user):
        return Post.objects.filter(user=user).count()

    def get_followers(self, user):
        return Follow.objects.filter(follow=user).count()


class StoryImageSerializer(ModelSerializer):
    class Meta:
        model = StoryImage
        fields = ['id', 'image', 'user']


class StorySerializer(ModelSerializer):
    story = SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'story']

    def get_story(self, user):
        today = datetime.datetime.now()
        yesturday = today - datetime.timedelta(days=1)
        user.stories_set.filter(created_at__lte=yesturday).delete()
        stories = user.stories_set.all()
        data = StoryImageSerializer(stories, many=True).data
        return data


class FeedSerializer(ModelSerializer):
    user = SerializerMethodField()
    likes = SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'user', 'image', 'caption', 'likes', 'created_at']

    def get_user(self, post):
        return UserSerializer(post.user).data

    def get_likes(self, post):
        return post.likes.count()


class NotificationSerializer(ModelSerializer):
    notification_by = SerializerMethodField()
    post = SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'notification_by', 'post', 'created_at']

    def get_post(self, notification):
        if notification.post:
            return {
                'image': notification.post.image.url,
                'caption': notification.post.caption,
            }

    def get_notification_by(self, notification):
        if notification.followed_by:
            return UserSerializer(notification.followed_by).data
        if notification.liked_by:
            return UserSerializer(notification.liked_by).data
