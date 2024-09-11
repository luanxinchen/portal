from rest_framework import viewsets
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin
from api.utils.jwt_auth import create_token
from api.utils.encrypt import md5
from api.extensions import return_code
from api.models import User

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    def validate_username(self, username):
        if not User.objects.filter(username=username).first():
            raise serializers.ValidationError('账号不存在！')
        return username


class SuperuserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

    def validate_username(self, username):
        user = User.objects.filter(username=username).first()
        if not user:
            raise serializers.ValidationError('账号不存在！')
        # 判断是否为管理用户
        elif not user.is_superuser:
            raise serializers.ValidationError('无权登录！')
        return username


class LoginViewSet(CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    authentication_classes = []
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        if not serializer.is_valid():
            return Response({'code': return_code.USR_NOT_FOUND, 'error': serializer.errors})

        username, clean_password = serializer.validated_data.values()
        password = md5(clean_password)

        user_obj = User.objects.filter(username=username,password=password).first()

        if not user_obj:
            return Response({'code': return_code.AUTH_FAILED, 'error': '认证失败,请检查账号密码是否正确。'})
        # 创建token，传入userid和username作为载荷，设置token有效期1天
        token = create_token(payload={'id': user_obj.id, 'name': user_obj.username}, timeout=60 * 24 * 7)
        print(token)
        return Response(
            {'code': return_code.SUCCESS,
             'results': {'id': user_obj.id, 'name': user_obj.username, 'token': token}})
