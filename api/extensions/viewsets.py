from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS


class SafeMethodNoAuthViewset(viewsets.ModelViewSet):
    """
    'GET', 'HEAD', 'OPTIONS'
    允许以上请求访问，跳过Auth
    """
    def get_authenticators(self):
        if self.request.method in SAFE_METHODS:
            self.authentication_classes = []
            self.permission_classes = []
        return [auth() for auth in self.authentication_classes]
