from rest_framework import serializers, filters
from api.models import Contact, ContactCategory
from api.extensions import permission
from api.extensions import viewsets


class ContactSerializer(serializers.ModelSerializer):
    category_cn = serializers.ReadOnlyField(source='category.title')
    contact_type_cn = serializers.ReadOnlyField(source='get_contact_type_display')

    class Meta:
        model = Contact
        fields = '__all__'


class ContactCategorySerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(many=True, read_only=True)

    class Meta:
        model = ContactCategory
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        contacts_sorted = sorted(representation['contacts'], key=lambda contact: contact['sort'])
        representation['contacts'] = contacts_sorted
        return representation


class ContactCateGoryViewSet(viewsets.SafeMethodNoAuthViewset):
    queryset = ContactCategory.objects.all().order_by('sort').prefetch_related('contacts')
    serializer_class = ContactCategorySerializer
    permission_classes = [permission.SuperUserEditAndGuestReadOnly, ]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['title', 'sort', 'id']


class ContactFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        category_query = request.query_params.get("category_id")
        if category_query:
            queryset = queryset.filter(category=category_query)
        return queryset


class ContactViewSet(viewsets.SafeMethodNoAuthViewset):
    queryset = Contact.objects.all().order_by('sort')
    serializer_class = ContactSerializer
    permission_classes = [permission.SuperUserEditAndGuestReadOnly, ]
    filter_backends = [ContactFilter, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['person', 'location', 'description', 'contact_key', 'category__title']
    ordering_fields = ['person', 'category', 'sort']
