from rest_framework.serializers import  ModelSerializer

from core.models import User, News


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id','phone','name','image']


class NewsSerializer(ModelSerializer):

    class Meta:
        model = News
        fields = ['id','details','title','image']