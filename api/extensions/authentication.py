from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from jwt import exceptions
from django.conf import settings
from api.extensions import return_code
from api.models import User


class JwtHeadersAuthentication(BaseAuthentication):

    def authenticate(self, request):
        """
        自定义JWT请求头认证方法
        :param request:
        :return: (request.user,request.auth)
        """
        # 获取请求头认证信息
        http_authorization = request.META.get('HTTP_AUTHORIZATION')
        salt = settings.SECRET_KEY

        # 请求头不含认证信息，抛出请求异常
        if not http_authorization:
            raise AuthenticationFailed({'code': return_code.INVALID_REQUEST, 'error': '非法请求'})

        # 拆分Bearer和Token主体
        method, token = http_authorization.split(' ')
        try:
            # Token解密
            payload = jwt.decode(jwt=token, key=salt, algorithms="HS256")
        except exceptions.ExpiredSignatureError:
            # Token过期
            raise AuthenticationFailed({'code': return_code.EXPIRED_TOKEN, 'error': "Token已失效"})
        except jwt.DecodeError:
            # Token解密失败
            raise AuthenticationFailed({'code': return_code.DECODE_FAILED_TOKEN, 'error': "Token不存在"})
        except jwt.InvalidTokenError:
            # JWT格式错误
            raise AuthenticationFailed({'code': return_code.INVALID_TOKEN, 'error': "非法Token"})

        # 根据payload用户信息获取User对象
        user_obj = User.objects.filter(id=payload['id']).first()

        return (user_obj, token)

    def authenticate_header(self, request):
        return 'Bearer Token'
