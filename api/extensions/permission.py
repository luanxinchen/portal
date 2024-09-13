from rest_framework import permissions
from django.contrib.auth import get_user_model
from api.extensions import return_code
from api.models import User


class SuperUserPermission(permissions.BasePermission):
    """
    仅超级用户读写
    """
    message = {'code': return_code.PERMISSION_ERROR, 'error': '请求无权限'}

    def has_permission(self, request, view):
        return bool(request.user.role == 1)


class SuperUserEditAndGuestReadOnly(permissions.BasePermission):
    """
    超级用户可写，其他用户可读
    """
    message = {'code': return_code.PERMISSION_ERROR, 'error': '请求无权限'}

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.user.role == 1
        )


class SuperUserListAndUserObjectOnly(permissions.BasePermission):
    """
    超级用户可遍历列表，非超级用户仅可获取当前用户ID对象
    """
    message = {'code': return_code.PERMISSION_ERROR, 'error': '请求无权限'}

    def has_permission(self, request, view):
        # 只有 superuser 能够获取列表
        if view.action == 'list' and not request.user.role == 1:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        # 非 superuser 只能获取与自己id一致的对象
        if not request.user.role == 1 and request.user.id != obj.id:
            return False
        return True
