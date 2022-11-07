from django.shortcuts import render
# from models import *

# Create your views here.

# 重构token登录验证返回
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_200_OK
from rest_framework.response import Response


# UserProfile

# 登录接口
class Login(ObtainAuthToken):
    """修改登录返回格式"""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        # user_data = UserInformation.objects.get(username=user.username)
        # return Response({'token': token.key, 'status': HTTP_200_OK, 'ID': user.id, '用户名': user.username, 'img': user.avatar})
        return Response({'token': token.key, 'status': HTTP_200_OK, 'ID': user.id, '用户名': user.username})
