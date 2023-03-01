from rest_framework.serializers import  ModelSerializer

from core.models import User, News


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['id','email','username','image']


