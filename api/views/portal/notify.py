from rest_framework import serializers, filters
from api.models import Notification
from api.extensions import permission
from api.extensions import viewsets


class NotificationSerializer(serializers.ModelSerializer):
    type_text = serializers.ReadOnlyField(source='get_type_display')

    class Meta:
        model = Notification
        fields = '__all__'


class NotificationViewSet(viewsets.SafeMethodNoAuthViewset):
    queryset = Notification.objects.all().order_by('id')
    serializer_class = NotificationSerializer
    permission_classes = [permission.SuperUserEditAndGuestReadOnly, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['id', 'title', 'content', 'start_time', 'end_time', 'is_active', 'type']
