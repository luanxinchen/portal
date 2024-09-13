from django.db.models import Q
from rest_framework import viewsets
from rest_framework import serializers
from api.models import User
from api.extensions import pagination, permission
from api.utils import encrypt
from rest_framework import filters


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = encrypt.md5(validated_data['password'])
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = encrypt.md5(validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('username', 'email')
    permission_classes = [permission.SuperUserPermission]
    pagination_class = pagination.CustomPagination
    ordering_fields = ['id', 'username', 'email', 'status']
