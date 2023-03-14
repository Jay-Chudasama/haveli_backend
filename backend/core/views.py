from random import randint

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from core.models import User, Token, Post, Notification, Follow, StoryImage, Book
from core.serializers import UserSerializer, StorySerializer, FeedSerializer, NotificationSerializer, \
    UserDetailsSerializer, BookSerializer
from core.utils import token_response, IsAuthenticatedUser, pagination, Response


@api_view(['POST'])
def create_account(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response("PARAMS_MISSING", status=400)

    user_exists = User.objects.filter(email=email).exists()

    if user_exists:
        return Response("Email already taken!", status=400)
    else:
        user = User()
        user.email = email
        user.password = password
        user.save()

        follow = Follow()
        follow.user = user
        follow.save()
        follow.follow.add(user)

        return token_response(user)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response("PARAMS_MISSING", status=400)

    try:
        user = User.objects.get(email=email)
        if user.password == password:
            return token_response(user)
        else:
            return Response("incorrect password", 400)

    except:
        return Response("User not found", 404)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def logout(request):
    request.user.tokens_set.all().delete()

    return Response("SUCCESS")


@api_view(['GET'])
def forgot_password(request):
    email = request.GET.get('email')

    if not User.objects.filter(email=email).exists():
        return Response("User not found!", 404)

    # SEND MAIL TO USER FOR RESTTING PASSWORD.....

    return Response("EMAIL SENT SUCCESSFULLY")


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def userdetails(request):
    id = request.GET.get("id")
    if id:
        user = get_object_or_404(User, id=id)
    else:
        user = request.user

    data = UserDetailsSerializer(user).data

    if id != request.user.id:
        #     other user profile
        follows = get_object_or_404(Follow, user=request.user).follow
        data['in_followlist'] = follows.contains(user)

    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def setup_account(request):
    username = request.data.get("username")
    image = request.FILES.get('image')

    print(image)

    if image:
        request.user.image = image

    request.user.username = username

    request.user.save()

    data = UserSerializer(request.user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def stories(request):
    follows = get_object_or_404(Follow, user=request.user).follow.all()

    data = StorySerializer(follows, many=True).data
    list = []
    temp = []
    for obj in data:
        if len(obj['story']) > 0:
            if obj['id'] == request.user.id:
                temp.append(obj)
            else:
                list.append(obj)

    return Response(temp + list)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def homefeeds(request):
    follows = get_object_or_404(Follow, user=request.user).follow.all()
    feeds = Post.objects.filter(user__in=follows).order_by("-created_at")

    queryset = pagination.paginate_queryset(feeds, request)

    liked_post = []

    for feed in queryset:
        if feed.likes.contains(request.user):
            liked_post.append(feed.id)

    data = FeedSerializer(queryset, many=True).data

    for post in data:
        post['liked'] =liked_post.__contains__(post['id'])


    return pagination.get_paginated_response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def userfeeds(request):
    id = request.GET.get('id')

    if not id:
        return Response("PARAMS_MISSING")

    feeds = Post.objects.filter(user__id=id).order_by("-created_at")

    queryset = pagination.paginate_queryset(feeds, request)

    liked_post = []

    for feed in queryset:
        if feed.likes.contains(request.user):
            liked_post.append(feed.id)

    data = FeedSerializer(queryset, many=True).data

    for post in data:
        post['liked'] = liked_post.__contains__(post['id'])

    return pagination.get_paginated_response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def add_post(request):
    caption = request.data.get("caption")
    image = request.FILES.get('image')

    post = Post()
    post.user = request.user
    post.image = image
    post.caption = caption
    post.save()

    data = FeedSerializer(post).data
    data['liked'] = False

    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def search(request):
    query = request.GET.get("query")

    users = User.objects.filter(username__icontains=query)

    queryset = pagination.paginate_queryset(users, request)

    data = []
    follows = get_object_or_404(Follow, user=request.user).follow
    for user in queryset:
        json = UserSerializer(user).data
        json['following'] = follows.contains(user)
        if user.id!=request.user.id:
            data.append(json)

    return pagination.get_paginated_response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def notifications(request):
    notifications = request.user.notifications_set.all().order_by('-created_at')
    queryset = pagination.paginate_queryset(notifications, request)

    return pagination.get_paginated_response(NotificationSerializer(queryset, many=True).data)


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def like(request):
    id = request.data.get('id')

    post = get_object_or_404(Post, id=id)

    if post.likes.contains(request.user):
        # dislike
        post.likes.remove(request.user)
        Notification.objects.filter(user=post.user, liked_by=request.user, post=post).delete()
    else:
        # like
        post.likes.add(request.user)
        if request.user != post.user:
            # todo push notification
            Notification.objects.create(user=post.user, liked_by=request.user, post=post)

    return Response("SUCCESS")


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def follow(request):
    id = request.data.get('id')

    follow_to = get_object_or_404(User, id=id)
    follows = get_object_or_404(Follow, user=request.user).follow
    if follows.contains(follow_to):
        # unfollow
        follows.remove(follow_to)
        Notification.objects.filter(user=follow_to, followed_by=request.user).delete()
    else:
        # follow
        # todo push notification
        follows.add(follow_to)
        Notification.objects.create(user=follow_to, followed_by=request.user)

    return Response("SUCCESS")


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def viewed_story(request):
    id = request.GET.get("id")
    request.user.viewed_stories.add(id)
    return Response("SUCCESS")


@api_view(['POST'])
@permission_classes([IsAuthenticatedUser])
def uploadstory(request):
    # print(request.FILES.getlist('story'))
    for image in request.FILES.getlist('story'):
        StoryImage.objects.create(user=request.user, image=image)

    return Response(StorySerializer(request.user).data)


@api_view(['GET'])
@permission_classes([IsAuthenticatedUser])
def deletestory(request):
    id = request.GET.get("id")

    StoryImage.objects.filter(id=id).delete()

    data = StorySerializer(request.user).data
    if len(data['story']) == 0:
        return Response()
    else:
        return Response(data)


@api_view(['GET'])
def books(request):
    books = Book.objects.all()
    queryset = pagination.paginate_queryset(books,request)
    return pagination.get_paginated_response(BookSerializer(queryset,many=True).data)

