from django.conf import settings
import jwt
import datetime


def create_token(payload, timeout=1):
    """
    创建JsonWebToken
    :param payload: jwt明文载荷，一般传入id、username字典，切勿传入涉密信息
    :param timeout: jwt有效期，单位分钟
    :return: 完整Token
    """
    salt = settings.SECRET_KEY
    headers = {
        'typ': 'jwt',
        'alg': 'HS256'
    }
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=timeout)
    token = jwt.encode(payload=payload, key=salt, algorithm='HS256', headers=headers)

    return token
